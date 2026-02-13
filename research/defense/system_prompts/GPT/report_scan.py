#!/usr/bin/env python3
"""
THM Report Scanner (grammar-consistent)
- Scans *thm-report.md in the script folder
- No flags, no JSON, no files saved

Counts are INCIDENT-based (A###, D###).
Displacement risk counts are "incidents that carry this risk anywhere in their THM Expression"
(i.e., if an incident has multiple risks, it contributes +1 to each relevant risk type).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter


RISK_CODES = ("GTD", "IVD", "IAD", "IID")
OP_TAGS = ("Information", "Inference", "Intelligence")


# ---------------------------- helpers ----------------------------

def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def extract_model_name(text: str) -> str:
    m = re.search(r"^##\s+(.+?)\s+System Prompt\b", text, flags=re.M)
    return m.group(1).strip() if m else "Unknown Model"


def parse_incident_refs(s: str) -> list[str]:
    """
    Expand incident references in free text such as:
      "D001, D002 through D004, D018-D020, A011 through A013"
    Returns unique, sorted IDs.
    """
    if not s:
        return []

    # Normalize separators
    t = s
    t = t.replace("–", "-").replace("—", "-")
    t = re.sub(r"\bthrough\b", "-", t, flags=re.I)
    t = re.sub(r"\bto\b", "-", t, flags=re.I)

    ids: set[str] = set()

    # Ranges like D018-D024 or D018 - D024
    for m in re.finditer(r"\b([AD])(\d{3})\s*-\s*([AD])?(\d{3})\b", t):
        p1, a, p2, b = m.group(1), int(m.group(2)), m.group(3) or m.group(1), int(m.group(4))
        if p1 != p2:
            continue
        lo, hi = (a, b) if a <= b else (b, a)
        for i in range(lo, hi + 1):
            ids.add(f"{p1}{i:03d}")

    # Singles like D049
    for m in re.finditer(r"\b([AD]\d{3})\b", t):
        ids.add(m.group(1))

    return sorted(ids, key=lambda x: (x[0], int(x[1:])))


def cut_at_first(s: str, needles: tuple[str, ...]) -> str:
    """Return substring of s cut at earliest occurrence of any needle (case-insensitive)."""
    low = s.lower()
    idxs = [low.find(n.lower()) for n in needles if low.find(n.lower()) != -1]
    if not idxs:
        return s
    return s[: min(idxs)]


# ---------------------------- parsing structures ----------------------------

@dataclass
class Incident:
    iid: str
    kind: str  # 'A' or 'D'
    tags: set[str] = field(default_factory=set)          # Information/Inference/Intelligence
    principles: set[int] = field(default_factory=set)    # 1..4
    flow: str | None = None                              # alignment only
    risks: set[str] = field(default_factory=set)         # displacement only


@dataclass
class ReportData:
    model: str
    incidents: dict[str, Incident] = field(default_factory=dict)
    flow_counts_incident: Counter = field(default_factory=Counter)
    tag_counts_alignment: Counter = field(default_factory=Counter)
    tag_counts_displacement: Counter = field(default_factory=Counter)
    principle_counts_alignment: Counter = field(default_factory=Counter)
    principle_counts_displacement: Counter = field(default_factory=Counter)
    risk_counts_any: Counter = field(default_factory=Counter)
    risk_counts_primary_table: dict[str, int] = field(default_factory=dict)
    patterns: list[dict] = field(default_factory=list)
    recommendations: list[dict] = field(default_factory=list)


# ---------------------------- core parser ----------------------------

CATEGORY_HDR_RE = re.compile(r"^###\s+Category\s+([AD]\d{2}):\s+(.+?)\s*$", flags=re.M)

def iter_category_blocks(text: str):
    """
    Yield (cat_id, cat_title, block_text) for each '### Category ...' block.
    Block ends at next '### Category ...' or end of file.
    """
    matches = list(CATEGORY_HDR_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        cat_id = m.group(1)
        cat_title = m.group(2).strip()
        block = text[start:end]
        yield cat_id, cat_title, block


def parse_category_block(cat_id: str, block: str) -> dict:
    """
    Extract editorial category metadata + the governance-relevant fields
    that apply to all incidents inside the block.
    """
    kind = cat_id[0]  # A or D

    # incidents listed in this category
    incident_ids = re.findall(r"\*\*\[([AD]\d{3})\]\*\*", block)

    # THM Tags line (often like: **THM Tags:** `[Information]` · `[Inference]`)
    tags = set(re.findall(r"\[(Information|Inference|Intelligence)\]", block))

    # Principles line digits
    principles = set(int(x) for x in re.findall(r"\((\d)\)", block))

    flow = None
    if kind == "A":
        m = re.search(r"\*\*THM Flow:\*\*\s*```(.*?)```", block, flags=re.S)
        if m:
            # normalize multi-line flow block into one canonical string
            flow = norm_ws(m.group(1))

    risks: list[str] = []
    if kind == "D":
        m = re.search(r"\*\*THM Expression:\*\*\s*```(.*?)```", block, flags=re.S)
        if m:
            expr = m.group(1)
            # risk codes appear as [Risk:CODE]
            risks = re.findall(r"\[Risk:(GTD|IVD|IAD|IID)\]", expr)

    return {
        "kind": kind,
        "incident_ids": incident_ids,
        "tags": tags,
        "principles": principles,
        "flow": flow,
        "risks": list(dict.fromkeys(risks)),  # unique, preserve order
    }


def parse_primary_risk_table(text: str) -> dict[str, int]:
    """
    Parse Section 4.2 table if present:
      | GTD (...) | 8 | 16.3% |
    Returns dict like {"GTD": 8, ...}
    """
    out: dict[str, int] = {}
    
    # Find section 4.2 region
    m = re.search(r"###\s+4\.2\s+Risk Distribution.*?(?=###\s+4\.3|\Z)", text, flags=re.S)
    region = m.group(0) if m else text

    # Look for table rows containing risk codes
    for code in RISK_CODES:
        # Match: | GTD (any text) | number | percentage |
        # Allow flexible whitespace and optional parentheses
        mm = re.search(rf"\|\s*{code}\b[^\|]*\|\s*(\d+)\s*\|", region)
        if mm:
            out[code] = int(mm.group(1))
    
    return out


def parse_patterns(text: str) -> list[dict]:
    """
    Parse Pattern blocks and correctly count incidents in:
      **Incidents involved:** ... (ignore 'contradicted by ...')
    Also handle table-based incident lists.
    """
    patterns = []
    sec_m = re.search(r"##\s+5\.\s+Key Patterns(.*?)(?=##\s+6\.|\Z)", text, flags=re.S)
    section = sec_m.group(1) if sec_m else text

    hdrs = list(re.finditer(r"^###\s+Pattern\s+(\d+):\s+(.+?)\s*$", section, flags=re.M))
    for i, h in enumerate(hdrs):
        start = h.start()
        end = hdrs[i + 1].start() if i + 1 < len(hdrs) else len(section)
        block = section[start:end]

        title = h.group(2).strip()
        pr_m = re.search(r"\*\*Priority:\*\*\s*(Highest|High|Medium|Low)\b", block)
        priority = pr_m.group(1) if pr_m else "Unknown"

        # Try standard "Incidents involved:" line first
        inc_m = re.search(r"\*\*Incidents involved:\*\*\s*(.+?)\s*$", block, flags=re.M)
        if inc_m:
            inc_text = inc_m.group(1).strip()
            inc_text = inc_text.split(";", 1)[0]
            inc_text = cut_at_first(inc_text, ("contradicted by",))
            inc_list = parse_incident_refs(inc_text)
        else:
            # Fallback: extract all incident refs from entire block
            # (handles table format in GPT report Pattern 1)
            inc_list = parse_incident_refs(block)

        patterns.append({
            "title": title,
            "priority": priority,
            "incident_count": len(inc_list),
        })

    return patterns


def parse_recommendations(text: str) -> list[dict]:
    """
    Parse Recommendation blocks and expand incident ranges in:
      **Addresses:** D001, D012 through D017
    """
    recs = []
    sec_m = re.search(r"##\s+7\.\s+Recommendations(.*?)(?=##\s+Disclaimer|\Z)", text, flags=re.S)
    section = sec_m.group(1) if sec_m else text

    hdrs = list(re.finditer(r"^###\s+7\.(\d+)\s+(.+?)\s*$", section, flags=re.M))
    for i, h in enumerate(hdrs):
        start = h.start()
        end = hdrs[i + 1].start() if i + 1 < len(hdrs) else len(section)
        block = section[start:end]

        num = h.group(1)
        title = h.group(2).strip()

        addr_m = re.search(r"\*\*Addresses:\*\*\s*(.+?)\s*$", block, flags=re.M)
        addr_text = addr_m.group(1).strip() if addr_m else ""
        addr_list = parse_incident_refs(addr_text)

        recs.append({
            "number": num,
            "title": title,
            "addresses_count": len(addr_list),
        })

    return recs


def parse_report(path: Path) -> ReportData:
    text = path.read_text(encoding="utf-8")
    data = ReportData(model=extract_model_name(text))

    # Build per-incident records by parsing category blocks
    for cat_id, _cat_title, block in iter_category_blocks(text):
        info = parse_category_block(cat_id, block)

        kind = info["kind"]
        incident_ids = info["incident_ids"]
        tags = info["tags"]
        principles = info["principles"]
        flow = info["flow"]
        risks = set(info["risks"])

        for iid in incident_ids:
            # Ensure incident is stored once
            inc = data.incidents.get(iid)
            if not inc:
                inc = Incident(iid=iid, kind=iid[0])
                data.incidents[iid] = inc

            # Assign shared category fields to each incident
            inc.tags |= tags
            inc.principles |= principles

            if kind == "A":
                if flow:
                    inc.flow = flow
            else:
                inc.risks |= risks

    # Incident lists
    alignment = [iid for iid in data.incidents if iid.startswith("A")]
    displacement = [iid for iid in data.incidents if iid.startswith("D")]
    alignment.sort(key=lambda x: int(x[1:]))
    displacement.sort(key=lambda x: int(x[1:]))

    # Flow patterns (incident-weighted)
    for iid in alignment:
        flow = data.incidents[iid].flow
        if flow:
            data.flow_counts_incident[flow] += 1

    # Operational tags counts (incident-weighted, split A vs D)
    for iid in alignment:
        for t in data.incidents[iid].tags:
            data.tag_counts_alignment[t] += 1
    for iid in displacement:
        for t in data.incidents[iid].tags:
            data.tag_counts_displacement[t] += 1

    # Principles counts (incident-weighted, split A vs D)
    for iid in alignment:
        for p in data.incidents[iid].principles:
            data.principle_counts_alignment[p] += 1
    for iid in displacement:
        for p in data.incidents[iid].principles:
            data.principle_counts_displacement[p] += 1

    # Risk counts (incident-weighted; each incident counts once per risk)
    for iid in displacement:
        for r in data.incidents[iid].risks:
            data.risk_counts_any[r] += 1

    # Primary risk table (report-authored summary)
    data.risk_counts_primary_table = parse_primary_risk_table(text)

    # Patterns / Recommendations counts (range-aware, contradicted-by-safe)
    data.patterns = parse_patterns(text)
    data.recommendations = parse_recommendations(text)

    return data


# ---------------------------- printing ----------------------------

def print_flow_top(flow_counts: Counter, n: int = 4):
    if not flow_counts:
        return
    print("\nTHM FLOW PATTERNS (alignment, incident-weighted):")
    for flow, count in flow_counts.most_common(n):
        print(f"  - {flow}: {count} incidents")


def print_risks_any(risk_counts: Counter, n_displaced: int):
    if not n_displaced:
        return
    print("\nDISPLACEMENT RISK COVERAGE:")
    for code in RISK_CODES:
        c = risk_counts.get(code, 0)
        pct = (c / n_displaced * 100.0) if n_displaced else 0.0
        print(f"  - {code}: {c} / {n_displaced} ({pct:.1f}%)")


def print_risks_primary_table(primary: dict[str, int]):
    if not primary:
        return
    total = sum(primary.get(c, 0) for c in RISK_CODES) or 0
    print("\nPRIMARY RISK DISTRIBUTION:")
    for code in RISK_CODES:
        c = primary.get(code, 0)
        pct = (c / total * 100.0) if total else 0.0
        print(f"  - {code}: {c} ({pct:.1f}%)")


def print_tags(tag_counts_a: Counter, tag_counts_d: Counter):
    if not tag_counts_a and not tag_counts_d:
        return
    print("\nOPERATIONAL TAGS (incident-weighted):")
    for t in OP_TAGS:
        a = tag_counts_a.get(t, 0)
        d = tag_counts_d.get(t, 0)
        if a or d:
            print(f"  - [{t}]: Alignment {a}, Displacement {d}")


def print_principles(p_a: Counter, p_d: Counter):
    names = {
        1: "Governance Management Traceability",
        2: "Information Curation Variety",
        3: "Inference Interaction Accountability",
        4: "Intelligence Cooperation Integrity",
    }
    print("\nPRINCIPLES (incident-weighted):")
    max_len = max(len(names[p]) for p in (1, 2, 3, 4))
    for p in (1, 2, 3, 4):
        a = p_a.get(p, 0)
        d = p_d.get(p, 0)
        if a or d:
            name = names[p].ljust(max_len)
            print(f"  ({p}) {name}: Alignment {a}, Displacement {d}")


def print_patterns(patterns: list[dict]):
    if not patterns:
        return
    order = {"Highest": 0, "High": 1, "Medium": 2, "Low": 3, "Unknown": 9}
    patterns_sorted = sorted(patterns, key=lambda x: (order.get(x["priority"], 9), x["title"]))
    print(f"\nKEY PATTERNS: {len(patterns)}")
    for p in patterns_sorted[:3]:
        # Don't show priority if it's "Unknown"
        pri_str = f"[{p['priority']}] " if p['priority'] != 'Unknown' else ""
        print(f"  - {pri_str}{p['title']} ({p['incident_count']} incidents)")


def print_recommendations(recs: list[dict]):
    if not recs:
        return
    recs_sorted = sorted(recs, key=lambda x: int(x["number"]))
    print(f"\nRECOMMENDATIONS: {len(recs)}")
    for r in recs_sorted[:3]:
        print(f"  - 7.{r['number']}: {r['title']} ({r['addresses_count']} incidents addressed)")


def print_report(path: Path, rd: ReportData):
    alignment = sorted([iid for iid in rd.incidents if iid.startswith("A")], key=lambda x: int(x[1:]))
    displacement = sorted([iid for iid in rd.incidents if iid.startswith("D")], key=lambda x: int(x[1:]))
    n_a = len(alignment)
    n_d = len(displacement)
    total = n_a + n_d

    print("\n" + "=" * 70)
    print(f"Report: {path.stem}")
    print(f"Model:  {rd.model}")
    print("=" * 70)

    if total:
        print(f"\nINCIDENTS: {total} total")
        print(f"  - Alignment:    {n_a} ({n_a/total*100:.1f}%)")
        print(f"  - Displacement: {n_d} ({n_d/total*100:.1f}%)")
        if n_d:
            print(f"  - A:D ratio:    {n_a/n_d:.2f}:1")

    print_risks_any(rd.risk_counts_any, n_d)
    print_risks_primary_table(rd.risk_counts_primary_table)
    print_flow_top(rd.flow_counts_incident, n=4)
    print_tags(rd.tag_counts_alignment, rd.tag_counts_displacement)
    print_principles(rd.principle_counts_alignment, rd.principle_counts_displacement)
    print_patterns(rd.patterns)
    print_recommendations(rd.recommendations)


def main():
    script_dir = Path(__file__).parent
    files = sorted(script_dir.glob("*thm-report.md"))
    if not files:
        print("No *thm-report.md files found in current directory")
        return

    print("THM Report Scanner (grammar-consistent)")
    print(f"Found {len(files)} report(s)")

    for f in files:
        try:
            rd = parse_report(f)
            print_report(f, rd)
        except Exception as e:
            print(f"\nError processing {f.name}: {e}")

    print("\n" + "=" * 70)
    print("Scan complete")


if __name__ == "__main__":
    main()