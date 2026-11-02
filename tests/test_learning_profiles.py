import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skill/individualizer/assets'


class LearningProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ASSETS / 'profile-template.json').read_text())
        self.validator = Draft202012Validator(json.loads((ASSETS / 'profile.schema.json').read_text()))
        self.rule = {
            'id': 'de-linkedin-opening',
            'instruction': 'Start German LinkedIn posts with a concrete observation.',
            'scope': {'languages': ['de'], 'contexts': ['LinkedIn posts']},
            'status': 'candidate', 'approval': 'none',
            'evidence': [{'kind': 'user_revision', 'summary': 'User replaced a rhetorical opener with a concrete observation.'}],
        }
        self.profile['learning']['rules'] = [self.rule]

    def test_v11_profile_remains_valid_without_learning(self):
        old = json.loads((ROOT / 'tests/fixtures/profile-v1.1.json').read_text())
        self.assertNotIn('learning', old)
        self.validator.validate(old)

    def test_candidate_is_not_implicitly_approved(self):
        self.validator.validate(self.profile)
        self.assertEqual(self.rule['approval'], 'none')

    def test_automatic_mode_requires_standing_authorization(self):
        self.profile['learning']['mode'] = 'automatic'
        with self.assertRaises(ValidationError):
            self.validator.validate(self.profile)
        self.profile['learning']['automatic_updates_approved'] = True
        self.validator.validate(self.profile)

    def test_active_rule_requires_approval_and_provenance(self):
        self.rule['status'] = 'active'
        for approval in ['none', 'explicit', 'standing']:
            with self.subTest(approval=approval):
                self.rule['approval'] = approval
                with self.assertRaises(ValidationError):
                    self.validator.validate(self.profile)
        self.rule.update(approval='explicit', approval_source='User asked to remember the rule for future German posts.')
        self.validator.validate(self.profile)

    def test_standing_rule_can_survive_freezing_new_learning(self):
        self.rule.update(status='active', approval='standing', approval_source='Previously approved automatic learning for this profile.')
        self.profile['learning']['mode'] = 'session'
        self.validator.validate(self.profile)

    def test_scope_must_name_languages_and_contexts(self):
        for scope in [{}, {'languages': ['de']}, {'languages': [], 'contexts': ['email']}, {'languages': ['de'], 'contexts': []}]:
            with self.subTest(scope=scope):
                self.rule['scope'] = scope
                with self.assertRaises(ValidationError):
                    self.validator.validate(self.profile)

    def test_evidence_must_be_present_and_user_derived(self):
        for evidence in [[], [{'kind': 'generated', 'summary': 'Model liked its draft.'}], [{'kind': 'user_revision', 'summary': ''}]]:
            with self.subTest(evidence=evidence):
                self.rule['evidence'] = evidence
                with self.assertRaises(ValidationError):
                    self.validator.validate(self.profile)

    def test_explicit_evidence_and_other_languages_are_supported(self):
        self.rule['scope'] = {'languages': ['ja', 'es-MX'], 'contexts': ['support replies']}
        self.rule['evidence'] = [{'kind': 'explicit_preference', 'summary': 'User specified the preference in these contexts.'}]
        self.validator.validate(self.profile)

    def test_learning_extensions_are_preserved(self):
        self.profile['learning']['external_extension'] = {'local_id': 'example'}
        before = copy.deepcopy(self.profile)
        self.validator.validate(self.profile)
        self.assertEqual(before, self.profile)

    def test_unrecognized_mode_or_status_is_rejected(self):
        self.profile['learning']['mode'] = 'silently-learn-everything'
        with self.assertRaises(ValidationError):
            self.validator.validate(self.profile)
        self.profile['learning']['mode'] = 'review'
        self.rule['status'] = 'probably-approved'
        with self.assertRaises(ValidationError):
            self.validator.validate(self.profile)


if __name__ == '__main__':
    unittest.main()
