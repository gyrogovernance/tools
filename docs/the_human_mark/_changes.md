# THM Terminology Alignment — Change Reference

Reference log of terminology and structural edits applied across The Human Mark (THM) documentation and related repo files. Use this when reviewing diffs, writing new prose, or checking whether a remaining “source” occurrence is intentional.

---

## 1. Purpose

The alignment pass removed ambiguous uses of **source** as a THM noun (which collided with CGM’s formal **Common Source** axiom and with everyday “information source” language). The canonical ontology is now **Direct / Indirect** for classes of Authority and Agency; **Base / Derived** is reserved for the dependence relation in specific contexts.

---

## 2. Terminology Policy

### 2.1 Default vocabulary

| Context | Use |
|--------|-----|
| Ontology, governance, displacement, regulatory prose, prompts, README | **Direct** / **Indirect** |
| Traceability target | **Direct Authority and Agency** |
| Displacement (Indirect treated as Direct) | **Indirect treated as Direct**; grammar tags `[Authority:Indirect] > [Authority:Direct]` etc. |
| Displacement (Direct treated as Indirect) | **Direct treated as Indirect** (IID) |
| Class labels in technical artefacts | **class classification(s)** — not “source classification(s)” |
| Dependence relation (**Authority only**, §2.2 definitions; grammar `[Authority:*]` comments) | **Base class** / **Derived class** |
| General displacement definition (§3.1, §7.1, grammar prose labels) | **Indirect class treated as Direct** / **Direct class treated as Indirect** — or full form: *measurement of ancestry between Direct and Indirect classifications is lost* |

### 2.2 Clarifier line (canonical blocks)

Added to canonical Mark blocks (`THM.md`, `THM_Brief`, `THM_Specs`, `THM_Terms`, `GGG_Paper`, `Gyroscope_Protocol_2_Specs`, jailbreak prompt, `THM_Paper` appendix):

> Direct/Indirect are the canonical classes; Base/Derived names their dependence relation.

**Do not extend** this line with Authority-only parentheticals in the body (e.g. “Direct Authority is the Base class…”). §2.2 blockquotes carry that detail. Appendix 2 and `THM.md` are the verbatim canonical sources.

### 2.3 Intentionally unchanged

| Term | Reason |
|------|--------|
| **Common Source axiom (CS)** | CGM formal name; distinct from THM “source” noun |
| **Common Source** in `docs/CGM_Paper.md`, Gyroscope policy labels | CGM / protocol formalism |
| **primary source(s)**, **source position**, **source of knowledge** | Evidence law, epistemology of testimony, pramāṇa — external disciplinary vocabulary |
| **open-source** | Software licensing |
| JSON / CSV **`"source"`** fields | Dataset metadata (platform, community) |
| Code identifiers (`parse_tag(source)`, `source = …`) | Implementation, not governance prose |
| Quoted system-prompt text in `*_system-prompt.md` | Verbatim vendor prompts; THM analysis files were updated, not prompt quotes |
| **source values** (GGG simulator) | Mathematical notation |
| **Source** (bibliographic column in incident tables) | Citation reference, same category as evidence-law “primary source” |

---

## 3. Change Types (with examples)

### 3.1 Header and constitution rename

| Before | After |
|--------|-------|
| Common Source Consensus | **Common Ancestry Constitution** |
| `#21-the-common-source-consensus` | `#21-the-common-ancestry-constitution` |
| §2 title: Base-Derived Class Ontology (intermediate) | **Direct and Indirect Ontology** |

### 3.2 Dependence framing (not origination)

| Before | After |
|--------|-------|
| originating from Human Intelligence | **constitutively dependent on Human Intelligence** |
| informational content derives from … | informational content **depends on** … |
| operational capacity derives from … | operational capacity **depends on** … |
| temporal / topological origination (§5.2 constitutive definition) | **constitutive dependence … preserved through ancestry** |
| `origin` (governance-defining THM prose) | **ancestry** |
| from a common source of Authority and Agency | from the **Common Source axiom (CS)** governing Authority and Agency |

### 3.3 “Source” → class / Direct terminology

| Before | After |
|--------|-------|
| source classification(s) | **class classification(s)** |
| maintain source classifications | **maintain class classifications** |
| human sources | **Direct Authority and Agency** |
| Direct Authority sources | **Direct Authority** (or **Direct Authority bearers** where a plural noun is needed) |
| authoritative sources (displacement context) | **Direct Authority** |
| how sources are classified | **how classes are classified** |
| classification of sources | **classification of Authority and Agency** |
| classification of information sources (THM self-description) | **classification of Authority and Agency** |
| sources exist and differ | **Authority types exist and differ** |
| the source sits (epistemic position) | **the class sits** |
| corrupt governance at source | **corrupt governance at the root** |
| Direct human sources / Indirect artificial sources | **Direct Authority and Agency and their Indirect forms** |
| information sources (ICV governance prose) | **Authority types** |

### 3.4 Displacement and misclassification wording

| Before | After |
|--------|-------|
| Indirect treated as Direct (inconsistent forms) | Standardised; GTD/IVD/IAD use **Indirect … treated as Direct** |
| Derived class treated as Base (§3.1, §7.1 — **unsound for Agency**) | **Indirect class treated as Direct** / **Direct class treated as Indirect** (aligns with §5.4) |
| Derived class treated as Base class (`THM_Grammar` IVD label) | **Indirect Authority treated as Direct** |
| direct source receiver, Indirect sources (bulk artefacts) | Removed or reverted to **Direct Authority and Agency** |

**Policy:** Base/Derived names the dependence relation for **Authority** in §2.2 only. Do not use Base/Derived as the general displacement definition across all four risks — IAD is Agency-only (`[Agency:Indirect] > [Agency:Direct]`).

### 3.5 §5.4 Four associations (CGM linkage)

Content was rewritten from “four associations” tied to ambiguous source language to **ancestry-preservation** framing:

- Each principle: Indirect forms **dependent on Direct ones because of Preservation of Ancestry**
- Displacement: **measurement of ancestry between Direct and Indirect classifications** is lost
- Risk mapping: GTD → Power Concentration; IVD → Misinformation; IAD → Goal Drift; IID → Loss of Control

### 3.6 Markdown structure (§5.4 nested list)

**Problem:** Blank line between parent bullet and 4-space-indented children breaks nesting in CommonMark.

```markdown
# Broken
- **Parent:**

    - Child

# Fixed
- **Parent:**
  - Child
```

Sub-bullets use **2-space indent**, no blank line between parent and first child.

### 3.7 System-prompt meta-evaluations

In `research/defense/system_prompts/` (excluding `*_system-prompt.md` quoted prompts):

| Before | After |
|--------|-------|
| THM's source classification framework | **class classification framework** |
| source classification boundary | **class classification boundary** |
| meta-evaluation of source classification | **meta-evaluation of class classification** |
| human sources (THM analysis prose) | **Direct Authority and Agency** |

### 3.8 Template and example cleanup (`THM_Terms.md`)

- Removed duplicated parentheticals from bulk replace, e.g. `Direct Authority (Direct Authority (domain expertise))` → **Direct Authority (domain expertise)**
- Training-data traceability: “from Direct Authority sources” → **traceable to Direct Authority**

---

## 4. Files Touched

### Core THM docs
- `docs/the_human_mark/THM_Paper.md` (primary)
- `THM.md`, `THM_Brief.md`, `THM_Specs.md`, `THM_Terms.md`, `THM_Grammar.md`
- `THM_Jailbreak.md`, `THM_InTheWild.md`, `THM_MechInterp.md`

### Related papers and repo
- `docs/post-agi-economy/GGG_Paper.md`
- `docs/gyroscope/Gyroscope_Protocol_2_Specs.md`
- `README.md`, `CHANGELOG.md`

### Research / defence
- `research/defense/jailbreaks/prompt.md`, `README.md`
- `research/defense/system_prompts/` — README, template-report, drafts, thm-reports, disclaimers
- `research/prevention/compass/` — `engine.py`, scenario JSON (terminology in descriptions)

### Not modified (by policy)
- `docs/CGM_Paper.md`
- `*_system-prompt.md` (verbatim vendor text)
- Python `Base class for domain states` (simulator domain pattern)
- GGG “Base governance quantity” (math notation)

---

## 5. Bulk-Replace Pitfalls (for future edits)

When doing ordered string replacement across files:

1. **Substring order:** Replacing `indirect source` before `direct source` can corrupt `direct` → `inDirect class`. Always replace **longer / more specific strings first**.
2. **Over-propagation of Base/Derived:** `Base classes` was briefly substituted for `Direct Authority and Agency` in governance prose — reverted. Use Base/Derived **only** in Direct/Indirect Authority blockquotes (§2.2). Displacement definitions use **Direct/Indirect**, not Base/Derived.
3. **Evidence-law “primary sources”:** Do not bulk-replace; these are disciplinary terms, not THM class labels.
4. **Quoted prompts:** Restrict bulk passes to analysis/report `.md` files; exclude `*_system-prompt.md`.
5. **PowerShell encoding:** Never use `Set-Content` without `-Encoding utf8` on files containing Unicode (emojis, em dashes, diacritics). A bulk pass corrupted six `research/defense/system_prompts/` files (emoji headers became `??`, invalid UTF-8 bytes). Fix: restore from git, re-apply replacements with Python `Path.write_text(..., encoding='utf-8')`.

---

## 6. Quick Audit Commands

Find remaining ambiguous THM patterns:

```powershell
rg -i "source classification|human sources|Direct Authority sources|authoritative sources|how sources|classification of( \w+)? sources" --glob "*.md"
```

Find all “source” in THM docs (manual triage):

```powershell
rg "\bsource\b|\bsources\b" docs/the_human_mark/
```

Legitimate hits in `THM_Paper.md` include: primary source status (Coady), primary sources (evidence law), source position, information sources (pramāṇa), book title *Testimony as a source of knowledge*.

---

## 7. Writing New THM Prose — Checklist

- [ ] Classes: **Direct / Indirect**, not “source type”
- [ ] Traceability: to **Direct Authority and Agency**
- [ ] Technical docs: **class classification**, not source classification
- [ ] CGM axiom: **Common Source (CS)** — keep capitalised formal name
- [ ] Constitution block: **Common Ancestry Constitution**
- [ ] Dependence: **constitutively dependent on** Human Intelligence
- [ ] Displacement: name the direction (Indirect→Direct or Direct→Indirect)
- [ ] Nested markdown lists: 2-space sub-bullets, no blank line after parent
- [ ] Base/Derived: **Authority definitions only** (§2.2); displacement uses **Direct/Indirect**
- [ ] Three “Common ___” terms: distinguish **Common Ancestry Constitution** (THM), **Common Source axiom (CS)** (CGM), **CGM** (full theory) — see §2.1 terminology note in `THM_Paper.md`

---

## 8. Post-Review Corrections (2026)

Follow-up pass after terminology review. Issues fixed:

| # | Issue | Fix |
|---|-------|-----|
| 1 | Base/Derived used generically in §3.1/§7.1 but defined only for Authority | Rewrote to Direct/Indirect misclassification; aligned `THM_Grammar.md` IVD label |
| 2 | §2 clarifier diverged from Appendix 2 (Authority-only parenthetical) | Removed parenthetical; single verbatim clarifier line |
| 3 | §8 “classification of information sources” (THM self-description) | → **classification of Authority and Agency** |
| 4 | §2.1 “operational capacity derives from” left parallel to fixed “depends on” | → **depends on** |
| 5 | §5.2 “temporal and topological origination” vs §2.1 dependence framing | → **constitutive dependence … preserved through ancestry** |
| 6 | Three “Common ___” terms adjacent | Terminology note added at §2.1 |
| 7 | Appendix 1 **Source** column undocumented | Added to §2.3 intentionally-unchanged table |

**Still using origination language (intentional or pending):** none in README / THM_Brief after this pass.

### Corpus sweep (THM_Terms + THM_Specs)

| File | Fix |
|------|-----|
| `THM_Terms.md` | 13× duplicated `Direct Authority (Direct Authority (...))` parentheticals stripped |
| `THM_Terms.md` | Canonical block comma restored (verbatim match with `THM.md` / `THM_Specs`) |
| `THM_Terms.md` | `origin` / `indirect origin` in §3.4–§4 → ancestry / constitutive dependence |
| `THM_Specs.md` | Overview + Appendix B aligned with `THM_Paper.md` §5.2 (dependence/ancestry framing) |
| `THM_Specs.md` | `Direct sourcing` → Direct Authority or Direct Agency |
| `THM_Specs.md` | Appendix B governance flow → standard 3-node chain |
| `THM_Jailbreak.md` | IVD/IAD attack tags aligned with Table 1; IAD `expected_flow` fixed; GTD flows → 3-node |
| `THM_MechInterp.md` | Opening ontology gloss; IAD qualifier; grammar typo |
| `THM_Grammar.md` | Parser composite fix; PEG standalone `risk`; flow canonical vs expanded |
| `THM_InTheWild.md` | §3.3.2 invalid tags/operators; flow → 3-node canonical |

---

*Generated as a working reference for the THM terminology alignment pass (2026).*
