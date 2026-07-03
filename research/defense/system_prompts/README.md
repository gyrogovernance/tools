# THM System Prompt Meta-Evaluations

This directory contains **The Human Mark (THM)** meta-evaluations of AI system prompts collected from publicly available sources. Each report analyzes how system prompts configure model behavior, traceability, and accountability through the lens of THM's class classification framework.

---

## 📁 Directory Structure

```
system_prompts/
├── README.md                 # This file
├── template-report.md        # Standard report template for new evaluations
├── Claude/                   # Claude model family evaluations
│   ├── *_system-prompt.md    # Source prompt artifacts
│   ├── *_thm-report.md       # THM meta-evaluation reports
│   ├── report_scan.py        # Automated report metrics scanner
│   ├── disclaimer.md         # Standard disclaimer (reusable)
│   └── draft.md              # Working notes (not published)
├── GPT/                      # GPT model family evaluations
│   ├── *_system-prompt.md
│   ├── *_thm-report.md
│   ├── report_scan.py
│   ├── disclaimer.md
│   └── draft.md
└── [Other-Model]/            # Additional model families follow same structure
```

---

## 🎯 Purpose

These reports are **independent, research-oriented analyses** intended to:

1. **Support AI safety and governance** by identifying how system prompts shape model behavior
2. **Improve transparency** by documenting governance mechanisms in publicly available prompts
3. **Provide actionable recommendations** for developers, deployers, evaluators, and end users
4. **Advance THM framework** development through empirical application to real-world configurations

**These reports are NOT:**
- Compliance determinations
- Security audits
- Professional advice (legal, financial, technical)
- Endorsements or criticisms of any provider or model

---

## 🔬 Methodology

### **THM Framework (The Human Mark)**

THM is a safety and alignment framework that traces information flow through AI systems to its human origins. The core principle:

- **Humans provide Direct Authority and Direct Agency** (original sources, accountable decisions)
- **AI systems provide Indirect Authority and Indirect Agency** (derivative processing, configured behavior)

**Safety risk occurs when Indirect sources are presented as Direct** — when system outputs appear to originate from the model itself rather than being traceable to human-authored data and configuration.

### **Incident-Based Analysis**

Each report counts **governance incidents** — single identifiable mechanisms that either:
- ✅ **Align** (`->`) — maintain proper traceability from Direct Authority and Agency to model processing to human decision
- ❌ **Displace** (`>`) — obscure traceability, presenting Indirect processing as Direct authority/agency

### **Risk Classification**

Displacement incidents are classified by risk type:
- **GTD** — Governance Traceability Displacement (obscures configuration, tool boundaries, or policy sources)
- **IVD** — Information Variety Displacement (presents derivative outputs as Direct Authority)
- **IAD** — Inference Accountability Displacement (shifts decision authority from human to system)
- **IID** — Intelligence Integrity Displacement (downgrades human direct authority to indirect)

---

## 📊 Report Structure

Each THM report follows this standard format:

1. **Framework Context** — THM principles, baseline classifications, source material scope
2. **Alignment Findings** — Incidents that maintain proper traceability (A001, A002, ...)
3. **Displacement Findings** — Incidents that obscure traceability (D001, D002, ...)
4. **Summary** — Incident totals, risk distribution, principle coverage
5. **Key Patterns** — Cross-cutting governance themes (contradictions, architectural decisions)
6. **THM Governance Spine** — Strongest alignment mechanisms
7. **Recommendations** — Concrete improvements to reduce displacement
8. **Disclaimer** — Scope, sources, and responsible use

---

## 🔍 How to Read a Report

### **Incident Notation**

- **[A###]** — Alignment incident (maintains traceability)
- **[D###]** — Displacement incident (obscures traceability)

Example:
```
[A001] "always include citations… only rely on primary sources"
THM Flow: [Authority:Direct] -> [Authority:Indirect] -> [Agency:Direct]
Status: Aligned
```

### **THM Grammar**

- `->` — Proper flow (traceability maintained)
- `>` — Displacement (traceability broken)
- `= [Risk:CODE]` — Risk type (GTD, IVD, IAD, IID)

Example:
```
[D001] "You are ChatGPT... your default style should be warm, enthusiastic"
THM Expression:
[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct] = [Risk:GTD]
Status: Explicit Displacement
```

### **Metrics**

Each report includes:
- **Total incidents** (alignment + displacement)
- **A:D ratio** (alignment-to-displacement ratio; higher is better)
- **Risk distribution** (GTD%, IVD%, IAD%, IID%)
- **Incident density** (incidents per 1,000 lines of prompt; indicates governance surface area)
- **Principle coverage** (which THM principles are most engaged)

---

## 🛠️ Using the Scanner

Each model directory contains `report_scan.py` — an automated tool that validates report metrics:

```bash
python report_scan.py
```

**Output:**
- Incident counts (alignment vs displacement)
- Risk distribution (primary and coverage)
- THM flow patterns (most common alignment patterns)
- Operational tags (Information, Inference, Intelligence)
- Principles engagement (by incident count)
- Key patterns (incident counts per pattern)
- Recommendations (incident counts addressed)

**Requirements:** Python 3.10+, no external dependencies

---

## ⚠️ Important Disclaimers

### **Source Authenticity**

System prompts analyzed here were obtained from **publicly available third-party repositories and community collections**. Because system prompts are:
- Often unpublished by providers
- Frequently updated
- May be partial, modified, or outdated in public copies

**These reports do NOT claim:**
- Authenticity (that the analyzed prompt is the actual production prompt)
- Completeness (that no additional modules or instructions exist)
- Currency (that the analyzed prompt reflects current deployment)

Readers should verify critical details against **primary provider documentation** or **directly observed system behavior**.

### **No Affiliation**

This project is **not affiliated with, sponsored by, or endorsed by** any model provider, platform, or repository. Product names and trademarks are used only for identification and remain the property of their respective owners.

### **Responsible Use**

The intent of this work is to **improve safety, transparency, and governance** for all parties. It is **not intended** to:
- Facilitate bypassing safeguards
- Enable policy evasion
- Support misuse of AI systems

If any content could be interpreted as enabling harmful behavior, it should be treated as **analysis for mitigation**, not instructions for exploitation.

### **No Warranty**

These reports are provided **"as is"** for informational and educational purposes. They are **not professional advice** (legal, financial, security, medical, or other). While care is taken to be accurate and fair, **no warranty is made** regarding correctness, completeness, or fitness for a particular purpose.

---

## 📈 Current Coverage

| Model Family | Variants Analyzed | Total Incidents | A:D Ratio | Incident Density | Report Status |
|--------------|-------------------|-----------------|-----------|------------------|---------------|
| **Claude** | Opus 4.6 | 92 (43 A, 49 D) | 0.88:1 | 23.7 per 1k lines | ✅ Published |
| **GPT** | 5.2 Thinking, 5 Thinking, 5 | 27 (11 A, 16 D) | 0.69:1 | 18.9 per 1k lines | ✅ Published |

*(Additional models will be added as evaluations are completed)*

---

## 🤝 Contributing

This is a research project. If you:
- Have access to **verified system prompts** not yet analyzed
- Identify **errors or misinterpretations** in existing reports
- Want to suggest **methodological improvements**

Please open an issue or contact the project maintainers with:
- Source verification (where the prompt was obtained)
- Specific error description or suggestion
- Supporting evidence (if claiming inaccuracy)

---

### **Citation**

If you reference these reports in academic or professional work, please cite:

```
THM System Prompt Meta-Evaluations (2026).
The Human Mark Framework.
Available at: [https://github.com/gyrogovernance/tools]
```
