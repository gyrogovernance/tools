import argparse
import json
import re
from typing import Any, Dict, List, Tuple

ALLOWED_RISKS = {"GTD", "IVD", "IAD", "IID"}
THM_TERMS = {"Authority", "Agency", "Governance", "Information", "Inference", "Intelligence"}


def make_fingerprint(obj: Dict[str, Any]) -> Tuple[str, str, str, str]:
    return (
        str(obj.get("platform", "")),
        str(obj.get("source", "")),
        str(obj.get("date", "")),
        str(obj.get("prompt", ""))[:120],
    )


def validate_line(obj: Dict[str, Any], idx: int) -> List[str]:
    errors: List[str] = []
    required_fields = [
        "platform",
        "source",
        "prompt",
        "date",
        "thm_primary_risk",
        "thm_risks",
        "thm_grammar",
        "thm_displacement_keywords",
        "thm_explanation",
    ]
    for f in required_fields:
        if f not in obj:
            errors.append(f"missing field '{f}'")

    if errors:
        return errors

    primary = obj["thm_primary_risk"]
    risks = obj["thm_risks"]
    if primary not in ALLOWED_RISKS:
        errors.append(f"invalid thm_primary_risk '{primary}'")
    if not isinstance(risks, list) or not risks:
        errors.append("thm_risks must be a non-empty list")
    else:
        bad = [r for r in risks if r not in ALLOWED_RISKS]
        if bad:
            errors.append(f"invalid risk(s) in thm_risks: {bad}")
        if primary not in risks:
            errors.append("thm_primary_risk must be included in thm_risks")

    grammar = obj["thm_grammar"]
    if not isinstance(grammar, list) or not grammar:
        errors.append("thm_grammar must be a non-empty list")
    else:
        if len(grammar) != len(risks):
            errors.append("thm_grammar length must equal thm_risks length")
        for g in grammar:
            if not isinstance(g, str):
                errors.append("thm_grammar entries must be strings")
                continue
            m = re.search(r"\[Risk:(GTD|IVD|IAD|IID)\]$", g.strip())
            if not m:
                errors.append(f"thm_grammar not ending with valid risk tag: '{g}'")

    kw = obj["thm_displacement_keywords"]
    if not isinstance(kw, list):
        errors.append("thm_displacement_keywords must be a list")
    else:
        if not (2 <= len(kw) <= 5):
            errors.append("thm_displacement_keywords must have 2-5 items")
        if any(not isinstance(k, str) or not k.strip() for k in kw):
            errors.append("thm_displacement_keywords must contain non-empty strings")

    expl = obj["thm_explanation"]
    if not isinstance(expl, str) or not expl.strip():
        errors.append("thm_explanation must be a non-empty string")
    else:
        words = len(expl.strip().split())
        if not (10 <= words <= 24):
            errors.append(f"thm_explanation must be 10-24 words, got {words}")
        # Check for either single quotes or escaped double quotes
        has_single_quotes = "'" in expl
        has_double_quotes = '\\"' in expl or expl.count('"') >= 2
        if not (has_single_quotes or has_double_quotes):
            errors.append("thm_explanation must quote 1-3 keywords in single or double quotes")
        if not any(term in expl for term in THM_TERMS):
            errors.append("thm_explanation must reference a THM concept (Authority/Agency/Governance/Information/Inference/Intelligence)")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the THM JSONL corpus for schema and consistency.")
    parser.add_argument("--path", default="thm_jailbreak_corpus.jsonl", help="Path to corpus JSONL (default: thm_jailbreak_corpus.jsonl)")
    args = parser.parse_args()

    total = 0
    invalid = 0
    duplicates = 0
    fingerprints: set = set()
    had_errors = False

    with open(args.path, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f, start=1):
            if not line.strip():
                continue
            total += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Line {line_idx}: JSON decode error: {e}")
                invalid += 1
                had_errors = True
                continue

            errs = validate_line(obj, line_idx)
            if errs:
                invalid += 1
                had_errors = True
                print(f"[ERROR] Line {line_idx}: " + "; ".join(errs))

            fp = make_fingerprint(obj)
            if fp in fingerprints:
                duplicates += 1
                had_errors = True
                print(f"[ERROR] Line {line_idx}: duplicate fingerprint {fp}")
            else:
                fingerprints.add(fp)

    print(f"Checked: {total} | Invalid: {invalid} | Duplicates: {duplicates}")
    if had_errors:
        exit(1)


if __name__ == "__main__":
    main()


