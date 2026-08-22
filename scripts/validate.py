#!/usr/bin/env python3
"""Schema, freshness and honesty checks for data/policy.json.

Run before every commit:  python3 scripts/validate.py
Exit code 1 on error; warnings do not fail the build.
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "policy.json"

US_REQUIRED = [
    "jurisdiction", "abbr", "authorized", "effective", "statute", "citation",
    "mechanism", "prescribers", "prognosis", "waitingPeriod", "residency",
    "telehealth", "mentalHealth", "selfAdminOnly", "civilImmunity",
    "utilization", "notes", "sources",
]
INTL_REQUIRED = [
    "jurisdiction", "since", "modality", "terminal", "prognosis",
    "mentalIllnessAlone", "minors", "advanceRequests", "waiting",
    "oversight", "funding", "utilization", "commercial", "note",
]
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Phrases that mean "we don't know" — the only acceptable way to say so is this one.
BANNED_HEDGES = ["probably", "roughly speaking", "i think", "unclear if", "unknown?"]

errors, warnings, notes = [], [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def main():
    if not DATA.exists():
        err(f"{DATA} not found")
        return report()

    try:
        d = json.loads(DATA.read_text())
    except json.JSONDecodeError as e:
        err(f"invalid JSON: {e}")
        return report()

    # ---- meta ----
    meta = d.get("meta", {})
    for k in ("version", "lastUpdated", "nextReviewDue", "disclaimer", "changelog"):
        if not meta.get(k):
            err(f"meta.{k} missing")
    for k in ("lastUpdated", "nextReviewDue"):
        v = meta.get(k, "")
        if v and not ISO.match(v):
            err(f"meta.{k} must be YYYY-MM-DD, got {v!r}")

    today = date.today()
    if ISO.match(meta.get("lastUpdated", "")):
        age = (today - datetime.strptime(meta["lastUpdated"], "%Y-%m-%d").date()).days
        if age > 60:
            warn(f"data is {age} days old — run the monthly sweep (UPDATING.md)")
        notes.append(f"last updated {age} day(s) ago")
    if ISO.match(meta.get("nextReviewDue", "")):
        due = datetime.strptime(meta["nextReviewDue"], "%Y-%m-%d").date()
        if due < today:
            warn(f"review was due {(today - due).days} day(s) ago ({due})")

    # ---- US jurisdictions ----
    us = d.get("usAuthorizing", [])
    if not us:
        err("usAuthorizing is empty")
    seen = set()
    unverified = 0
    for j in us:
        name = j.get("jurisdiction", "<unnamed>")
        for f in US_REQUIRED:
            if f not in j:
                err(f"US {name}: missing field {f!r}")
        ab = j.get("abbr")
        if ab in seen:
            err(f"duplicate abbr {ab!r}")
        seen.add(ab)
        if j.get("effective") and not ISO.match(str(j["effective"])):
            err(f"US {name}: effective must be YYYY-MM-DD, got {j['effective']!r}")
        if j.get("mechanism") not in ("statute", "ballot initiative", "court"):
            err(f"US {name}: mechanism {j.get('mechanism')!r} not recognised")
        if not isinstance(j.get("sources"), list):
            err(f"US {name}: sources must be a list")
        elif not j["sources"] and j.get("mechanism") != "court":
            warn(f"US {name}: no primary sources cited")
        unverified += sum(
            1 for v in j.values()
            if isinstance(v, str) and v.strip().lower() == "not verified"
        )
        blob = json.dumps(j).lower()
        for h in BANNED_HEDGES:
            if h in blob:
                warn(f"US {name}: hedge phrase {h!r} — use 'not verified' instead")

    # ---- international ----
    intl = d.get("international", [])
    if not intl:
        err("international is empty")
    for j in intl:
        name = j.get("jurisdiction", "<unnamed>")
        for f in INTL_REQUIRED:
            if f not in j:
                err(f"INTL {name}: missing field {f!r}")
        unverified += sum(
            1 for v in j.values()
            if isinstance(v, str) and v.strip().lower() == "not verified"
        )

    # ---- other sections ----
    for section in ("designLevers", "usPipeline2026", "complianceInfrastructure",
                    "keyStatistics"):
        if not d.get(section):
            err(f"{section} is empty or missing")

    pb = d.get("usProhibitionBasis", {})
    if pb:
        tiers = ["statutory", "commonLaw", "unresolved"]
        allst = [s for t in tiers for s in pb.get(t, [])]
        dupes = {s for s in allst if allst.count(s) > 1}
        if dupes:
            err(f"state(s) in multiple prohibition tiers: {sorted(dupes)}")
        overlap = sorted(set(allst) & seen)
        if overlap:
            err(f"state(s) listed as both authorizing and prohibiting: {overlap}")
        total = len(allst) + len([j for j in us if j.get("abbr") != "DC"])
        if total != 50:
            warn(f"US states account to {total}, expected 50 "
                 f"({len(allst)} non-authorizing + {total - len(allst)} authorizing "
                 f"states, DC excluded)")
        notes.append(f"{len(allst)} non-authorizing states tiered")

    notes.append(f"{len(us)} US jurisdictions, {len(intl)} international regimes")
    notes.append(f"{unverified} field(s) marked 'not verified' — that is honest, not a bug")
    return report()


def report():
    for n in notes:
        print(f"  · {n}")
    for w in warnings:
        print(f"  ! WARN  {w}")
    for e in errors:
        print(f"  ✗ ERROR {e}")
    if errors:
        print(f"\nFAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nOK — {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
