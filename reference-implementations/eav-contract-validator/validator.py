#!/usr/bin/env python3
"""Public reference validator for AX-PUB-SPEC-002.

Educational, non-production reference implementation.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

ALLOWED_EVIDENCE_CLASSIFICATIONS = {
    "FACT",
    "SOURCE_DATA",
    "ASSUMPTION",
    "ESTIMATE",
    "HYPOTHESIS",
    "INFERENCE",
    "FORECAST",
    "SCENARIO",
    "PROFESSIONAL_OPINION",
    "RECOMMENDATION",
    "DECISION",
    "VERIFIED_OUTCOME",
    "UNKNOWN",
    "SUPERSEDED",
}

ALLOWED_AUTHORITY_STATES = {"ACTIVE", "REVOKED", "EXPIRED"}
ALLOWED_VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str
    severity: str = "ERROR"


class ContractValidationError(ValueError):
    pass


def _items(bundle: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = bundle.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ContractValidationError(f"{key} must be a list")
    if not all(isinstance(item, dict) for item in value):
        raise ContractValidationError(f"{key} must contain JSON objects")
    return value


def _index(
    records: Iterable[dict[str, Any]], id_field: str, collection: str
) -> tuple[dict[str, dict[str, Any]], list[Finding]]:
    result: dict[str, dict[str, Any]] = {}
    findings: list[Finding] = []
    for i, record in enumerate(records):
        record_id = record.get(id_field)
        path = f"{collection}[{i}].{id_field}"
        if not isinstance(record_id, str) or not record_id.strip():
            findings.append(
                Finding("AX-REF-ID-MISSING", path, f"{id_field} must be a non-empty string")
            )
            continue
        if record_id in result:
            findings.append(
                Finding("AX-REF-ID-DUPLICATE", path, f"duplicate identifier: {record_id}")
            )
            continue
        result[record_id] = record
    return result, findings


def _require(
    record: dict[str, Any], fields: Iterable[str], base_path: str
) -> list[Finding]:
    findings: list[Finding] = []
    for field in fields:
        value = record.get(field)
        if value is None or value == "" or value == [] or value == {}:
            findings.append(
                Finding(
                    "AX-REF-REQUIRED",
                    f"{base_path}.{field}",
                    f"required field missing: {field}",
                )
            )
    return findings


def _parse_iso(value: Any, path: str) -> tuple[datetime | None, list[Finding]]:
    if value in (None, ""):
        return None, []
    if not isinstance(value, str):
        return None, [
            Finding("AX-REF-TIME-TYPE", path, "timestamp must be an ISO-8601 string")
        ]
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(candidate), []
    except ValueError:
        return None, [
            Finding(
                "AX-REF-TIME-FORMAT",
                path,
                f"invalid ISO-8601 timestamp: {value}",
            )
        ]


def validate_bundle(bundle: dict[str, Any]) -> list[Finding]:
    if not isinstance(bundle, dict):
        raise ContractValidationError("top-level JSON value must be an object")

    evidence = _items(bundle, "evidence_records")
    decisions = _items(bundle, "decision_records")
    authorities = _items(bundle, "authority_grants")
    executions = _items(bundle, "execution_records")
    verifications = _items(bundle, "verification_records")
    outcomes = _items(bundle, "verified_outcomes")

    evidence_by_id, findings = _index(evidence, "evidence_id", "evidence_records")
    decision_by_id, more = _index(decisions, "decision_id", "decision_records")
    findings.extend(more)
    authority_by_id, more = _index(authorities, "authority_id", "authority_grants")
    findings.extend(more)
    execution_by_id, more = _index(executions, "execution_id", "execution_records")
    findings.extend(more)
    verification_by_id, more = _index(
        verifications, "verification_id", "verification_records"
    )
    findings.extend(more)
    _, more = _index(outcomes, "outcome_id", "verified_outcomes")
    findings.extend(more)

    for i, record in enumerate(evidence):
        base = f"evidence_records[{i}]"
        findings.extend(
            _require(
                record,
                ("evidence_id", "classification", "source_identity", "observed_at"),
                base,
            )
        )
        classification = record.get("classification")
        if classification and classification not in ALLOWED_EVIDENCE_CLASSIFICATIONS:
            findings.append(
                Finding(
                    "AX-EAV-CLASSIFICATION",
                    f"{base}.classification",
                    f"unsupported classification: {classification}",
                )
            )
        _, time_findings = _parse_iso(
            record.get("observed_at"), f"{base}.observed_at"
        )
        findings.extend(time_findings)

    for i, record in enumerate(decisions):
        base = f"decision_records[{i}]"
        findings.extend(
            _require(
                record,
                (
                    "decision_id",
                    "decision_question",
                    "decision_owner",
                    "evidence_refs",
                    "decided_at",
                ),
                base,
            )
        )
        refs = record.get("evidence_refs", [])
        if isinstance(refs, list):
            for j, ref in enumerate(refs):
                if ref not in evidence_by_id:
                    findings.append(
                        Finding(
                            "AX-EAV-EVIDENCE-REF",
                            f"{base}.evidence_refs[{j}]",
                            f"unknown evidence reference: {ref}",
                        )
                    )
        else:
            findings.append(
                Finding(
                    "AX-EAV-EVIDENCE-REF-TYPE",
                    f"{base}.evidence_refs",
                    "evidence_refs must be a list",
                )
            )
        _, time_findings = _parse_iso(record.get("decided_at"), f"{base}.decided_at")
        findings.extend(time_findings)

    for i, record in enumerate(authorities):
        base = f"authority_grants[{i}]"
        findings.extend(
            _require(
                record,
                (
                    "authority_id",
                    "decision_id",
                    "principal",
                    "permitted_action",
                    "resource_scope",
                    "status",
                    "granted_at",
                ),
                base,
            )
        )
        decision_id = record.get("decision_id")
        if decision_id and decision_id not in decision_by_id:
            findings.append(
                Finding(
                    "AX-EAV-DECISION-REF",
                    f"{base}.decision_id",
                    f"unknown decision reference: {decision_id}",
                )
            )
        state = record.get("status")
        if state and state not in ALLOWED_AUTHORITY_STATES:
            findings.append(
                Finding(
                    "AX-EAV-AUTHORITY-STATE",
                    f"{base}.status",
                    f"unsupported authority state: {state}",
                )
            )
        granted_at, time_findings = _parse_iso(
            record.get("granted_at"), f"{base}.granted_at"
        )
        findings.extend(time_findings)
        expires_at, time_findings = _parse_iso(
            record.get("expires_at"), f"{base}.expires_at"
        )
        findings.extend(time_findings)
        if granted_at and expires_at and expires_at <= granted_at:
            findings.append(
                Finding(
                    "AX-EAV-AUTHORITY-WINDOW",
                    f"{base}.expires_at",
                    "expires_at must be later than granted_at",
                )
            )

    for i, record in enumerate(executions):
        base = f"execution_records[{i}]"
        findings.extend(
            _require(
                record,
                (
                    "execution_id",
                    "decision_id",
                    "authority_id",
                    "actor",
                    "action",
                    "resource",
                    "started_at",
                    "status",
                ),
                base,
            )
        )
        decision_id = record.get("decision_id")
        authority_id = record.get("authority_id")
        if decision_id and decision_id not in decision_by_id:
            findings.append(
                Finding(
                    "AX-EAV-EXEC-DECISION",
                    f"{base}.decision_id",
                    f"unknown decision reference: {decision_id}",
                )
            )
        authority = authority_by_id.get(authority_id)
        if authority is None and authority_id:
            findings.append(
                Finding(
                    "AX-EAV-EXEC-AUTHORITY",
                    f"{base}.authority_id",
                    f"unknown authority reference: {authority_id}",
                )
            )
        elif authority:
            if authority.get("status") != "ACTIVE":
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-AUTHORITY-INACTIVE",
                        f"{base}.authority_id",
                        "execution references non-active authority",
                    )
                )
            if decision_id and authority.get("decision_id") != decision_id:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-DECISION-MISMATCH",
                        f"{base}.decision_id",
                        "execution decision does not match authority decision",
                    )
                )
            actor = record.get("actor")
            if actor and authority.get("principal") != actor:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-PRINCIPAL",
                        f"{base}.actor",
                        "execution actor does not match authority principal",
                    )
                )
            action = record.get("action")
            if action and authority.get("permitted_action") != action:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-ACTION",
                        f"{base}.action",
                        "execution action is outside the authority grant",
                    )
                )
            scope = authority.get("resource_scope")
            resource = record.get("resource")
            if isinstance(scope, list) and resource and resource not in scope:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-SCOPE",
                        f"{base}.resource",
                        "execution resource is outside the authority grant",
                    )
                )
            elif isinstance(scope, str) and resource and scope != "*" and resource != scope:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-SCOPE",
                        f"{base}.resource",
                        "execution resource is outside the authority grant",
                    )
                )
        started_at, time_findings = _parse_iso(
            record.get("started_at"), f"{base}.started_at"
        )
        findings.extend(time_findings)
        if authority:
            granted_at, _ = _parse_iso(
                authority.get("granted_at"), f"{base}.authority.granted_at"
            )
            expires_at, _ = _parse_iso(
                authority.get("expires_at"), f"{base}.authority.expires_at"
            )
            if started_at and granted_at and started_at < granted_at:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-BEFORE-GRANT",
                        f"{base}.started_at",
                        "execution started before authority was granted",
                    )
                )
            if started_at and expires_at and started_at >= expires_at:
                findings.append(
                    Finding(
                        "AX-EAV-EXEC-AFTER-EXPIRY",
                        f"{base}.started_at",
                        "execution started after authority expired",
                    )
                )

    for i, record in enumerate(verifications):
        base = f"verification_records[{i}]"
        findings.extend(
            _require(
                record,
                ("verification_id", "execution_id", "verifier", "verdict", "verified_at"),
                base,
            )
        )
        execution_id = record.get("execution_id")
        execution = execution_by_id.get(execution_id)
        if execution is None and execution_id:
            findings.append(
                Finding(
                    "AX-EAV-VERIFY-EXEC",
                    f"{base}.execution_id",
                    f"unknown execution reference: {execution_id}",
                )
            )
        verdict = record.get("verdict")
        if verdict and verdict not in ALLOWED_VERDICTS:
            findings.append(
                Finding(
                    "AX-EAV-VERDICT",
                    f"{base}.verdict",
                    f"unsupported verification verdict: {verdict}",
                )
            )
        if record.get("requires_independent_verifier") is True and execution:
            if record.get("verifier") == execution.get("actor"):
                findings.append(
                    Finding(
                        "AX-EAV-VERIFY-INDEPENDENCE",
                        f"{base}.verifier",
                        "independent verification required but verifier equals execution actor",
                    )
                )
        _, time_findings = _parse_iso(
            record.get("verified_at"), f"{base}.verified_at"
        )
        findings.extend(time_findings)

    for i, record in enumerate(outcomes):
        base = f"verified_outcomes[{i}]"
        findings.extend(
            _require(
                record,
                ("outcome_id", "verification_id", "outcome_state", "accepted_at"),
                base,
            )
        )
        verification_id = record.get("verification_id")
        verification = verification_by_id.get(verification_id)
        if verification is None and verification_id:
            findings.append(
                Finding(
                    "AX-EAV-OUTCOME-VERIFY",
                    f"{base}.verification_id",
                    f"unknown verification reference: {verification_id}",
                )
            )
        elif verification and verification.get("verdict") != "PASS":
            findings.append(
                Finding(
                    "AX-EAV-OUTCOME-NOT-PASSED",
                    f"{base}.verification_id",
                    "VERIFIED OUTCOME requires a PASS verification",
                )
            )
        if record.get("outcome_state") != "VERIFIED":
            findings.append(
                Finding(
                    "AX-EAV-OUTCOME-STATE",
                    f"{base}.outcome_state",
                    "verified_outcome record must use outcome_state=VERIFIED",
                )
            )
        _, time_findings = _parse_iso(
            record.get("accepted_at"), f"{base}.accepted_at"
        )
        findings.extend(time_findings)

    return findings


def validate_file(path: Path) -> list[Finding]:
    with path.open("r", encoding="utf-8") as handle:
        bundle = json.load(handle)
    return validate_bundle(bundle)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an AX-PUB-SPEC-002 reference contract bundle."
    )
    parser.add_argument("bundle", type=Path, help="Path to a JSON contract bundle.")
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Emit findings as JSON."
    )
    args = parser.parse_args()

    try:
        findings = validate_file(args.bundle)
    except (OSError, json.JSONDecodeError, ContractValidationError) as exc:
        print(f"VALIDATION_INPUT_ERROR: {exc}")
        return 2

    if args.json_output:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    elif findings:
        for finding in findings:
            print(
                f"{finding.severity} {finding.code} {finding.path}: {finding.message}"
            )
    else:
        print("AX_EAV_REFERENCE_VALIDATION_PASS")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
