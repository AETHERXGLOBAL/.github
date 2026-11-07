"""Offline public-only activity contract: no network or credentials."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

src = Path(__file__).resolve().parents[1] / "scripts" / "render_engineering_pulse.py"
spec = importlib.util.spec_from_file_location("engineering_pulse", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PublicActivityContract(unittest.TestCase):
    def test_public_data_only_and_valid_svg(self):
        records = [{"state": "open", "merged_at": None, "updated_at": "2026-11-06T19:00:00Z"},
                   {"state": "closed", "merged_at": "2026-11-06T20:00:00Z", "updated_at": "2026-11-06T20:00:00Z"}]
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(mod, "OUTPUT", Path(tmp) / "pulse.svg"), \
             patch.object(mod, "fetch_public_repos", return_value=[{"name": "public-example", "visibility": "public"}]), \
             patch.object(mod, "fetch_repo_pulls", return_value=records) as fetch:
            self.assertEqual(mod.main(), 0)
            svg = (Path(tmp) / "pulse.svg").read_text(encoding="utf-8")
            ET.fromstring(svg)
            self.assertIn("PUBLIC-ONLY", svg)
            self.assertIn("public-example", svg)
            self.assertNotIn("private-example", svg)
            fetch.assert_called_once_with("public-example")

    def test_api_failure_does_not_create_artifact(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(mod, "OUTPUT", Path(tmp) / "pulse.svg"), \
             patch.object(mod, "fetch_public_repos", side_effect=RuntimeError("API unavailable")):
            with self.assertRaises(RuntimeError):
                mod.main()
            self.assertFalse((Path(tmp) / "pulse.svg").exists())

if __name__ == "__main__":
    unittest.main()
