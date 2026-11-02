import copy
import json
import re
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "individualizer"
SCHEMA = json.loads((SKILL / "assets/profile.schema.json").read_text())
BASE = json.loads((SKILL / "assets/profile-template.json").read_text())

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.validator = Draft202012Validator(SCHEMA)
        self.profile = copy.deepcopy(BASE)

    def assertInvalid(self):
        self.assertTrue(list(self.validator.iter_errors(self.profile)))

    def test_schema_and_unapproved_template(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.validator.validate(self.profile)
        self.assertFalse(self.profile["approved_by_user"])

    def test_original_v1_profile_still_valid(self):
        old = json.loads((ROOT / "tests/fixtures/profile-v1.json").read_text())
        self.validator.validate(old)

    def test_approved_requires_approval(self):
        self.profile["status"] = "approved"
        self.assertInvalid()

    def test_draft_cannot_claim_approval(self):
        self.profile["approved_by_user"] = True
        self.assertInvalid()

    def test_explicitly_approved_profile(self):
        self.profile.update(status="approved", approved_by_user=True)
        self.validator.validate(self.profile)

    def test_unknown_extensions_survive(self):
        self.profile["customer_extension"] = {"workflow": ["local"]}
        self.profile["voice"]["custom_trait"] = "measured"
        self.validator.validate(self.profile)
        self.assertEqual(self.profile["customer_extension"]["workflow"], ["local"])

    def test_language_extensibility(self):
        for tag in ["en-GB", "de-CH", "es-MX", "ja", "ar"]:
            self.profile["language_settings"][tag] = {"locale": tag, "address": None}
        self.validator.validate(self.profile)

    def test_invalid_palette_values(self):
        for value in ["blue", "#xyzxyz", "#123", "#1234567", 123456]:
            with self.subTest(value=value):
                self.profile["visual"]["palette"] = [{"role": "primary", "hex": value}]
                self.assertInvalid()

    def test_valid_empty_and_hex_palettes(self):
        for colors in [[], [{"role": "text", "hex": "#aA1234"}]]:
            self.profile["visual"]["palette"] = colors
            self.validator.validate(self.profile)

    def test_missing_core_field(self):
        del self.profile["voice"]
        self.assertInvalid()

    def test_invalid_profile_version(self):
        self.profile["version"] = "1.2"
        self.assertInvalid()

    def test_invalid_edit_depth(self):
        self.profile["editorial"]["edit_depth"] = "random"
        self.assertInvalid()

    def test_sample_cannot_omit_approval_state(self):
        self.profile["samples"] = [{"id": "s1", "language": "de", "kind": "generated", "context": "blog"}]
        self.assertInvalid()

    def test_generated_sample_can_remain_unapproved(self):
        self.profile["samples"] = [{"id": "s1", "language": "de", "kind": "generated", "context": "blog", "approved_by_user": False}]
        self.validator.validate(self.profile)

    def test_runtime_links_resolve(self):
        for md in SKILL.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", md.read_text()):
                if "://" not in link and not link.startswith("#"):
                    with self.subTest(file=str(md), link=link):
                        self.assertTrue((md.parent / link.split("#")[0]).exists())

if __name__ == "__main__":
    unittest.main()
