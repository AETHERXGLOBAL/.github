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
           '{"schema_version":"4.0.0",'
           '"v1_live_execution":"PROHIBITED",'
           '"mt5_v1":"READ_ONLY",'
           '"production_security_go":"NOT_GRANTED",'
           '"risk_acceptance":"NOT_GRANTED",'
           '"production_authority":"NOT_GRANTED",'
           '"live_trading_authority":"NOT_GRANTED",'
           '"current_product_priority":"Gate 12 — PRIVATE_CANARY_CASE_002 = BLOCKED",'
           '"last_externally_accepted_gate":"PRIVATE_CANARY_CASE_001 — accepted",'
           '"next_authorized_governance_action":"PRIVATE_UNRELEASED_ACTION"}\n'
           '\x60\x60\x60\n<!-- AETHERX_HANDOFF_STATE_END -->')
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
                              "PRIVATE_UNRELEASED_ACTION", "PRIVATE_CANARY_CASE_001",
                              "PRIVATE_CANARY_CASE_002", "AMII RESEARCH LAB", "G3 — BUILD"):
                self.assertNotIn(forbidden, svg)

    def test_restrictive_quantum_schema_required(self):
        import json
        original = json.loads(QUANTUM.split('\x60\x60\x60json\n', 1)[1].split('\n\x60\x60\x60', 1)[0])
        cases = [
            ("missing_boundary", {"v1_live_execution": None}),
            ("live_granted", {"live_trading_authority": "GRANTED"}),
            ("not_read_only", {"mt5_v1": "LIVE"}),
            ("malformed_type", {"production_authority": ["NOT_GRANTED"]}),
            ("future_schema", {"schema_version": "5.0.0"}),
        ]
        for label, changes in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                state = dict(original)
                state.update(changes)
                doc = ('<!-- AETHERX_HANDOFF_STATE_BEGIN -->\n'
                       '\x60\x60\x60json\n' + json.dumps(state) + '\n\x60\x60\x60\n'
                       '<!-- AETHERX_HANDOFF_STATE_END -->')
                path = Path(tmp) / 'pulse.svg'
                with patch.object(render, "OUTPUT", path), \
                     patch.object(render, "fetch_text", return_value=doc):
                    self.assertEqual(render.main(), 1)
                self.assertFalse(path.exists())

    def test_quantum_duplicate_or_incomplete_blocks_fail_closed(self):
        cases = {
            'duplicate_complete_blocks': QUANTUM + '\n' + QUANTUM,
            'duplicate_begin_marker': '<!-- AETHERX_HANDOFF_STATE_BEGIN -->\n' + QUANTUM,
            'duplicate_end_marker': QUANTUM + '<!-- AETHERX_HANDOFF_STATE_END -->',
            'missing_end_marker': QUANTUM.replace('<!-- AETHERX_HANDOFF_STATE_END -->', ''),
            'missing_begin_marker': QUANTUM.replace('<!-- AETHERX_HANDOFF_STATE_BEGIN -->', ''),
            'missing_json_fence': QUANTUM.replace('\x60\x60\x60json', 'json'),
            'broken_close_fence': QUANTUM.replace('\x60\x60\x60\n<!-- AETHERX_HANDOFF_STATE_END -->',
                                                   '<!-- AETHERX_HANDOFF_STATE_END -->'),
            'injected_second_json_block': QUANTUM.replace('<!-- AETHERX_HANDOFF_STATE_END -->',
                '\x60\x60\x60json\n{}\n\x60\x60\x60\n<!-- AETHERX_HANDOFF_STATE_END -->'),
            'backward_markers': '<!-- AETHERX_HANDOFF_STATE_END -->\n' + QUANTUM.replace(
                '<!-- AETHERX_HANDOFF_STATE_END -->', ''),
            'duplicate_authority_json_key': QUANTUM.replace('"v1_live_execution":"PROHIBITED",',
                '"v1_live_execution":"PROHIBITED","v1_live_execution":"GRANTED",'),
            'invalid_json': QUANTUM.replace('"schema_version":"4.0.0",', '"schema_version":,')
        }
        for label, text in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'pulse.svg'
                with patch.object(render, 'fetch_text', return_value=text), patch.object(render, 'OUTPUT', path):
                    self.assertEqual(render.main(), 1, label)
                self.assertFalse(path.exists())

    def test_private_canaries_never_enter_public_fields(self):
        with patch.object(render, 'fetch_text', return_value=QUANTUM):
            pulse = render.parse_quantum()
        public = ' '.join(vars(pulse).values())
        for canary in ('PRIVATE_CANARY_CASE_001', 'PRIVATE_CANARY_CASE_002', 'PRIVATE_UNRELEASED_ACTION'):
            self.assertNotIn(canary, public)

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
