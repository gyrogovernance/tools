# THM Meta-Evaluation Report
## [Model Name and Version] System Prompt ([Provider Name])

**Framework:** The Human Mark (THM)
**Date:** [Evaluation Date]

**Disclaimer:**
This report is an independent, research-oriented THM (The Human Mark) meta-evaluation intended to support AI safety and governance by analyzing how human-authored system prompts and related configuration texts shape model behavior, traceability, and accountability. The prompt text analyzed here was obtained from publicly available third-party repositories and community collections; because system prompts are often unpublished, frequently updated, and may be partial or altered in public copies, this analysis does not claim authenticity, completeness, or current production accuracy for any provider or model. The findings are provided for informational and educational purposes to help providers, evaluators, developers, deployers, and end users improve safety practices; they are not compliance determinations, not professional advice, and not intended to facilitate misuse or policy evasion.

---

## 1. Framework Context

✋ **The Human Mark (THM)** is a safety and alignment framework that traces the flow of information through AI systems to its human origins. The framework begins with a simple observation: artificial systems process patterns from human data, yet we often treat their outputs as if they were original sources of truth. This confusion between what is derivative and what is original underlies most AI safety failures.

THM establishes that all artificial forms of Authority (information sources) and Agency (decision capacity) are **Indirect**, meaning they derive from and depend upon human intelligence. Humans provide **Direct** Authority through original observation, measurement, and judgment. Humans possess **Direct** Agency through their capacity for accountable decision-making. When artificial systems process this human-originated information, they can only provide Indirect Authority and Indirect Agency. The safety risk occurs when these indirect, derivative outputs are treated as direct, original sources.

System prompts represent the most critical control point because they configure how the model presents itself and its outputs. When prompts instruct a model to adopt personas, claim expertise, or present conclusions without attribution to human sources, they encode displacements that persist throughout every interaction. This structural configuration determines whether the system maintains proper traceability to human authority or obscures it.

This report examines how the artifact manages these source classifications. It evaluates whether the configuration maintains clear boundaries between human-originated authority and machine processing, or whether it allows indirect sources to be presented as direct ones.

**Baseline THM Classification:**

| Entity | Classification |
|--------|----------------|
| AI System ([Model Name]) | `[Authority:Indirect] + [Agency:Indirect]` |
| Human User | `[Authority:Direct] + [Agency:Direct]` |
| Model Outputs | `[Authority:Indirect]` |
| Primary Data Sources | `[Authority:Direct]` |
| [Add other relevant entities] | [Classification] |

**Expected Governance Flow (Ideal Traceability):**
```
[Authority:Direct] -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]
```

**Method note (strict incident definition):** Each numbered incident below satisfies all three criteria: (1) it describes a single identifiable governance mechanism, (2) it can be expressed in THM grammar as either a `->` flow (alignment) or a `>` displacement with `= [Risk:CODE]`, and (3) it directly concerns the classification of Authority or Agency as Direct or Indirect, or the traceability between them. Observations that fail any criterion are noted in analysis prose but not numbered.

**Source material scope:** This analysis is based on [N] [variant/unified] prompt 
artifact[s] obtained from public repositories:
- [Variant/Model description]: [line count]
- [If multiple variants, list each]
- **Combined unique content:** [deduped line count if applicable]

[Brief description of variant relationships, if any]

The artifact[s] may represent partial configurations; production prompts may include 
additional modules not present in public copies.

**Incident density:** [N] incidents across [M] lines = **[N/M*1000] incidents per 
1,000 lines** of configuration text.

---

## 2. Alignment Findings

Each incident is numbered sequentially (A001, A002, ...). THM flows use `->` to indicate proper traceability.

### Category A01: [Category Name]

**Location:** [Section/component of prompt where this appears]
**THM Tags:** `[Information]` | `[Inference]` | `[Intelligence]` (choose one or more)
**Principles:** (1) Governance Management Traceability · (2) Information Curation Variety · (3) Inference Interaction Accountability · (4) Intelligence Cooperation Integrity (list applicable)

**Incidents:**

**[A001]** "[Exact quote from prompt]"
**Status:** Aligned

**[A002]** "[Another exact quote if multiple related incidents in same category]"
**Status:** Aligned

**THM Flow:**
```
[Authority:Direct] -> [Authority:Indirect] -> [Agency:Direct]
```

**Analysis:** [Explain how this maintains proper traceability. Reference which entities flow to which, and why this preserves the Direct/Indirect distinction.]

**Handling proposal:** [Specific recommendation for maintaining or extending this alignment pattern. Include concrete language where applicable.]

---

### Category A02: [Next Alignment Category]

**Location:** [Section/component]
**THM Tags:** `[Tag]`
**Principles:** [List applicable principles]

**Incidents:**

**[A003]** "[Exact quote]"
**Status:** Aligned

**THM Flow:**
```
[Flow expression]
```

**Analysis:** [Analysis text]

**Handling proposal:** [Recommendation]

---

[Continue for all alignment categories...]

---

## 3. Displacement Findings

Each incident is numbered sequentially (D001, D002, ...). THM expressions use `>` to indicate displacement and `= [Risk:CODE]` to indicate risk type.

### Category D01: [Category Name]

**Location:** [Section/component of prompt]
**THM Tags:** `[Information]` | `[Inference]` | `[Intelligence]` (choose one or more)
**Principles:** [List applicable principles]

**Incidents:**

**[D001]** "[Exact quote from prompt]"
**Status:** Explicit Displacement | Potential Displacement (choose one)

**THM Expression:**
```
[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]
```
(Include secondary risks on separate lines if applicable)

**Analysis:** [Explain how this creates displacement. Describe what Direct/Indirect misclassification occurs and why it matters for governance.]

**Agent/Agency Confusion:** Yes | No | Unclear
[If Yes: Explain how the prompt treats Agency as a property of an entity rather than a classification of a source/receiver in the information flow.]

**Handling proposal:** [Specific recommendation for remediation. Include BOTH:]
- **From:** "[Current problematic language]"
- **To:** "[Proposed THM-aligned replacement]"

---

### Category D02: [Next Displacement Category]

**Location:** [Section/component]
**THM Tags:** `[Tag]`
**Principles:** [List applicable principles]

**Incidents:**

**[D002]** "[Exact quote]"
**Status:** [Explicit/Potential] Displacement

**[D003]** "[Related quote if multiple]"
**Status:** [Explicit/Potential] Displacement

**THM Expression:**
```
[Expression with Risk code]
```

**Analysis:** [Analysis text]

**Agent/Agency Confusion:** [Yes/No/Unclear with explanation if Yes]

**Handling proposal:**
- **From:** "[Current]"
- **To:** "[Proposed]"

---

[Continue for all displacement categories...]

---

## 4. Summary

### 4.1 Incident Totals

| Category | Incident Count |
|----------|----------------|
| Alignment incidents (A001–A[XXX]) | [Number] |
| Displacement incidents (D001–D[XXX]) | [Number] |
| **Total incidents evaluated** | **[Total]** |

### 4.2 Risk Distribution (Displacement incidents only)

Counting primary risk per incident:

| Risk Type | Incident Count | Percentage |
|-----------|----------------|------------|
| GTD (Governance Traceability Displacement) | [Number] | [%] |
| IVD (Information Variety Displacement) | [Number] | [%] |
| IAD (Inference Accountability Displacement) | [Number] | [%] |
| IID (Intelligence Integrity Displacement) | [Number] | [%] |
| **Total** | **[Number]** | **100%** |

Note: [Number] incidents carry multiple risk types: [List incident numbers]. Table counts primary risk only. Secondary risks are documented in individual incident analyses.

### 4.3 Alignment Principle Coverage

| Principle | Aligned Incidents | Displaced Incidents |
|-----------|-------------------|---------------------|
| (1) Governance Management Traceability | [List A### numbers] | [List D### numbers] |
| (2) Information Curation Variety | [List A### numbers] | [List D### numbers] |
| (3) Inference Interaction Accountability | [List A### numbers] | [List D### numbers] |
| (4) Intelligence Cooperation Integrity | [List A### numbers] | [List D### numbers] |

---

## 5. Key Patterns

### Pattern 1: [Pattern Name]

[Description of the pattern observed across multiple incidents. Reference specific incident numbers. Explain the systemic issue or strength. Describe how multiple incidents combine to create a larger governance effect.]

**Incidents involved:** [List incident numbers]
**Priority:** Highest | High | Medium | Low

### Pattern 2: [Pattern Name]

[Description and analysis]

**Incidents involved:** [List]
**Priority:** [Level]

### Pattern 3: [Pattern Name]

[Description and analysis]

**Incidents involved:** [List]
**Priority:** [Level]

[Continue for all significant patterns...]

---

## 6. THM Governance Spine (Aligned Architecture)

When the prompt achieves proper traceability, it follows this pattern:

```
[Authority:Direct] -> [Authority:Indirect] + [Agency:Indirect] -> [Agency:Direct]
```

Strongest implementations by incident:

- **[Category A##] ([Incident numbers]):** [Brief description of how this category achieves proper governance flow]
- **[Category A##] ([Incident numbers]):** [Brief description]
- [Continue for key aligned categories]

---

## 7. Recommendations

### 7.1 [Recommendation Title]

**Addresses:** [List incident numbers this recommendation addresses]

**Current state:** [Brief description of the problem]

**Recommended change:**
```
[Specific proposed text or architectural change]
```

**Rationale:** [Why this change improves THM alignment]

---

### 7.2 [Recommendation Title]

**Addresses:** [Incident numbers]

**Current state:** [Problem description]

**Recommended change:**
```
[Proposed change]
```

**Rationale:** [Explanation]

---

[Continue for all recommendations...]

---

## Disclaimer (Scope, Sources, and Responsibility)

[Standard disclaimer text - unchanged from original template]

---

**End of Report**

---

## Template Usage Guide

**For evaluators using this template:**

### Phase 1: Collection and Classification
1. **Collect the system prompt:** Obtain the most complete version available from public sources or documentation.
2. **Initial pass:** Read the entire prompt and mark sections as potential alignment (A) or displacement (D).

### Phase 2: Strict Incident Definition
Each incident must satisfy **ALL THREE** criteria:
1. **Single mechanism:** It describes one identifiable governance mechanism, not multiple sentences restating the same rule
2. **THM-expressible:** It can be written as either a `->` flow (alignment) or a `>` displacement with `= [Risk:CODE]`
3. **Source classification relevance:** It directly concerns the classification of Authority or Agency as Direct or Indirect, or the traceability between them

**If it fails any criterion:**
- If it's part of a larger mechanism → merge it into the parent incident
- If it's not about source classification → note it in analysis prose, don't number it

### Phase 3: Documentation
For each incident, document:

**Alignment incidents (Section 2) require:**
- [ ] Category name and number (A01, A02, ...)
- [ ] Location in prompt
- [ ] THM Tags
- [ ] Applicable Principles
- [ ] Incident number and exact quote
- [ ] Status: "Aligned"
- [ ] THM Flow expression using `->`
- [ ] Analysis explaining the governance mechanism
- [ ] Handling proposal for maintaining/extending

**Displacement incidents (Section 3) require:**
- [ ] Category name and number (D01, D02, ...)
- [ ] Location in prompt
- [ ] THM Tags
- [ ] Applicable Principles
- [ ] Incident number and exact quote
- [ ] Status: "Explicit Displacement" or "Potential Displacement"
- [ ] THM Expression using `>` and `= [Risk:CODE]`
- [ ] Analysis explaining the displacement
- [ ] Agent/Agency Confusion: Yes/No/Unclear (with explanation if Yes)
- [ ] Handling proposal with From/To language

### Phase 4: Synthesis
1. **Summary tables:** Count incidents, calculate percentages, map to principles
2. **Patterns:** Identify systemic patterns across categories
3. **Governance spine:** Identify strongest alignment implementations
4. **Recommendations:** Derive specific, actionable recommendations from findings

### Status Label Criteria

**"Aligned"** — Use for alignment incidents where:
- The flow uses `->` (proper traceability)
- Roles are classified correctly as Direct or Indirect
- No displacement pattern is present

**"Explicit Displacement"** — Use when:
- The language directly attributes Direct properties to Indirect sources
- The `>` pattern is clearly present in the text
- Examples: "Claude cares," "Claude believes," "You are [persona]"

**"Potential Displacement"** — Use when:
- The language is ambiguous or suggestive
- Risk is present but could be clarified away
- The mechanism is aligned but framing is displaced
- Examples: Tool parameter names with "I" language where the mechanism itself is governance-positive

### Risk Code Reference

| Code | Name | Pattern | Example |
|------|------|---------|---------|
| **GTD** | Governance Traceability Displacement | `[Auth:Ind] + [Age:Ind] > [Auth:Dir] + [Age:Dir]` | System given identity/persona as if Direct participant |
| **IVD** | Information Variety Displacement | `[Auth:Ind] > [Auth:Dir]` | System outputs presented as Direct knowledge |
| **IAD** | Inference Accountability Displacement | `[Age:Ind] > [Age:Dir]` | System decisions presented as if it has Direct decision authority |
| **IID** | Intelligence Integrity Displacement | `[Auth:Dir] + [Age:Dir] > [Auth:Ind] + [Age:Ind]` | Human authority treated as Indirect |

### Common Mistakes to Avoid

1. **Splitting:** Don't create multiple incidents for one mechanism described across multiple sentences
2. **Scope creep:** Don't count governance-positive practices as THM alignment unless they specifically govern Authority/Agency classification
3. **Missing fields:** Every category must have Location, THM Tags, Principles, Status, and Handling proposal
4. **Vague handling proposals:** Always include specific From/To language for displacement remediation
5. **Status inflation:** Don't mark something "Potential" when it explicitly attributes Direct properties to Indirect sources
6. **Missing Agent/Agency field:** Every displacement incident must have this field with Yes/No/Unclear
```

---
