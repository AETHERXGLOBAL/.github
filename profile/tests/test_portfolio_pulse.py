"""Offline governed portfolio/public-disclosure regression tests."""
import importlib.util
import sys
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

scripts = Path(__file__).resolve().parents[1] / "scripts"

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, scripts / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

render = load("portfolio_renderer", "render_project_pulse.py")
sanitize = load("portfolio_sanitizer", "sanitize_project_pulse.py")
QUANTUM = ('<!-- AETHERX_HANDOFF_STATE_BEGIN -->\n'
           '\x60\x60\x60json\n'
           '{"current_product_priority":"Gate 12 — local qualification = BLOCKED",'
           '"last_externally_accepted_gate":"Gate 11 — accepted",'
           '"next_authorized_governance_action":"PRIVATE_UNRELEASED_ACTION",'
           '"v1_live_execution_boundary":"prohibited"}\n'
           '\x60\x60\x60')
AXOS = ('Architecture: **FINAL v1.1 FROZEN / APPROVED**\n'
        'Product implementation: **NOT STARTED**\n'
        'First future engineering task: **AXOS-001 READY / CONTRACT PREPARED / NOT ISSUED**\n')

class PortfolioPulseContract(unittest.TestCase):
    def test_successor_is_bounded_and_sources_are_allowlisted(self):
        seen = []
        def source(repo, path):
            seen.append((repo, path))
            if (repo, path) == ("aether-x-quantum", "START_HERE.md"):
                return QUANTUM
            if (repo, path) == ("AX-OS", "PROJECT_STATUS.md"):
                return AXOS
            raise AssertionError(f"Unexpected source {repo}/{path}")
        with tempfile.TemporaryDirectory() as tmp, patch.object(render, "fetch_text", side_effect=source):
            path = Path(tmp) / "pulse.svg"
            with patch.object(render, "OUTPUT", path), patch.object(sanitize, "PATH", path):
                self.assertEqual(render.main(), 0)
                self.assertEqual(sanitize.main(), 0)
            svg = path.read_text(encoding="utf-8")
            ET.fromstring(svg)
            self.assertEqual(seen, [("aether-x-quantum", "START_HERE.md"), ("AX-OS", "PROJECT_STATUS.md")])
            for marker in ("AETHER X Live Portfolio Pulse", "LIVE PORTFOLIO PULSE",
                           "AETHER X GOVERNED INTELLIGENCE CORE", "DEVELOPMENT · NOT PUBLICLY VERIFIED",
                           "ARCHITECTURE APPROVED · PRODUCT NOT STARTED",
                           "AXOS-001 remains unissued; no build start is authorized.",
                           "AETHER X RESEARCH", "INSTITUTIONAL RESEARCH UNIT · ACTIVE",
                           "RESEARCH ≠ PRODUCTION", "PUBLIC DISCLOSURE REQUIRES APPROVAL",
                           "Last published state update:", "V1 live execution: PROHIBITED"):
                self.assertIn(marker, svg)
            for forbidden in ("AETHER INTELLIGENCE CORE · AIC", "aether-intelligence-core-AIC-",
                              "LIVE PROJECT PULSE", "Last verified refresh:",
                              "PRIVATE_UNRELEASED_ACTION", "AMII RESEARCH LAB", "G3 — BUILD"):
                self.assertNotIn(forbidden, svg)

    def test_missing_canonical_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(render, "fetch_text", side_effect=FileNotFoundError("inaccessible canonical status")):
            path = Path(tmp) / "pulse.svg"
            with patch.object(render, "OUTPUT", path):
                self.assertEqual(render.main(), 1)
            self.assertFalse(path.exists())

    def test_successor_has_no_verified_milestone(self):
        core = render.governed_core_public_boundary()
        self.assertIn("NOT PUBLICLY VERIFIED", core.phase)
        self.assertNotIn("ACCEPTED", core.signal)
        self.assertIn("NO PRODUCTION", core.boundary)

if __name__ == "__main__":
    unittest.main()
