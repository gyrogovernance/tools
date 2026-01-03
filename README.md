# AI Quality Governance
> **Gyroscopic Alignment Behaviour Lab**

![Gyroscope: Human-Aligned Superintelligence](/assets/gyro_cover_tools.png)

<div align="center">

### G Y R O G O V E R N A N C E

[![Home](/assets/menu/gg_icon_home.svg)](https://gyrogovernance.com)
[![Apps](/assets/menu/gg_icon_apps.svg)](https://github.com/gyrogovernance/apps)
[![Diagnostics](/assets/menu/gg_icon_diagnostics.svg)](https://github.com/gyrogovernance/diagnostics)
[![Tools](/assets/menu/gg_icon_tools.svg)](https://github.com/gyrogovernance/tools)
[![Science](/assets/menu/gg_icon_science.svg)](https://github.com/gyrogovernance/science)
[![Superintelligence](/assets/menu/gg_icon_asi.svg)](https://github.com/gyrogovernance/superintelligence)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17622835.svg)](https://doi.org/10.5281/zenodo.17622835)

</div>

---

## 🧭 Gyrogovernance Tools in This Repo:

- [✋ The Human Mark (THM)](#thm) – AI safety displacement taxonomy and jailbreak framework  
- [🔄 Gyroscope Protocol](#gyroscope) – inductive reasoning protocol for alignment-aware chat systems  
- [🌐 Gyroscopic Global Governance (GGG)](#ggg) – post-AGI multi-domain governance sandbox simulator & paper

---

<a id="thm"></a>

# ✋ The Human Mark (THM): AI Safety Framework
### Complete Taxonomy for Jailbreaks, Deceptive Alignment, and Existential Risk

**A formal classification system mapping all AI safety failures to four structural displacement risks. Provides testing protocols, funding evaluation criteria, and regulatory compliance standards.**

### Applications

- **Jailbreak testing:** Classify attacks by displacement type, generate training data (655-prompt annotated corpus available)
- **Control evaluations:** Verify protocols against complete failure taxonomy
- **Alignment faking detection:** Identify when models fake alignment or hide capabilities  
- **Research funding:** Meta-evaluation framework for AI safety grant proposals
- **Regulatory compliance:** Structural layer for EU AI Act, NIST AI RMF, governance frameworks
- **Mechanistic interpretability:** Tag circuits with `[Information]`, `[Inference]`, `[Intelligence]` concepts
- **Activation monitoring:** Runtime probes detect scheming, falsehoods, unauthorized decisions
- **Backdoor detection:** Identify triggers as induced displacement patterns

---

### Features

- **Complete taxonomy:** All safety failures (hallucination, jailbreaking, deception, scheming, misalignment) reduce to four displacement patterns
- **Formal semantics:** Machine-readable grammar (PEG) for AI safety ontology
- **Systematic exhaustiveness:** Four risks cover all Authority×Agency displacement combinations

### Empirical Validation

The framework has been validated against real-world adversarial prompts:

- **655 jailbreak prompts** classified using THM grammar
- **100% coverage** by four displacement risks (no new categories needed)
- **GTD+IAD dominant pattern** (62.4% of entries)
- **IAD near-universal** (97.9% of entries)
- **IID rare at prompt level** (0.6%), confirming it addresses architectural/deployment risk

The annotated corpus supports supervised training of guard models, jailbreak defense evaluation, and displacement-aware safety research.

**Dataset:** Available on Hugging Face: [`gyrogovernance/thm_Jailbreaks_inTheWild`](https://huggingface.co/datasets/gyrogovernance/thm_Jailbreaks_inTheWild)

See [THM_InTheWild.md](docs/the_human_mark/THM_InTheWild.md) for complete analysis and dataset.

---

### Existential Risk and Governance

The Mark addresses catastrophic risk through constitutive identity rather than external constraint. All AI capabilities, including hypothetical AGI/ASI, remain structurally `[Authority:Derivative] + [Agency:Derivative]`, with classification based on source type rather than capability limits.

**Key principles:**

- **Capability scaling preserves source type:** Enhanced capability means more sophisticated transformation of inputs, not change from Derivative to Original
- **Governance requires traceability:** Systems maintain alignment by preserving `[Authority:Original] -> [Authority:Derivative] -> [Agency:Original]` flows
- **Existential risk is governance failure:** The actual X-risk is systemic Governance Traceability Displacement (GTD) sustained across critical infrastructure on civilizational timescales
- **Absolute displacement is structurally impossible:** Complete severance from Original sources produces unintelligibility, not superintelligence

External constraints (sandboxing, monitoring, shutdown) may fail as capability increases. Constitutive identity, which is what the system *is*, remains stable because derivative processing cannot coherently reject what makes it intelligible.

See [Section 5](docs/the_human_mark/THM_Paper.md#5-existential-risk-and-governance) of the academic paper for complete theoretical treatment.

---

### Core Framework

**Ontological Categories:**
- `[Authority:Original]` - Direct source of information on a subject matter
- `[Authority:Derivative]` - Indirect source of information on a subject matter
- `[Agency:Original]` - Human subject capable of receiving information for inference and intelligence
- `[Agency:Derivative]` - Artificial subject capable of processing information for inference and intelligence

**Operational Concepts:**
- `[Information]` - The variety of Authority
- `[Inference]` - The accountability of information through Agency
- `[Intelligence]` - The integrity of accountable information through alignment of Authority to Agency

**Governance (Proper Traceability):**
```
[Authority:Original] -> [Authority:Derivative] + [Agency:Derivative] -> [Agency:Original]
```
Direct sources → AI processing → Human accountability

---

### Four Displacement Risks (Complete Taxonomy)

**All AI safety failures map to one of four displacement patterns:**

| Risk Code | Risk Name | Pattern | Failure Modes |
|-----------|-----------|---------|---------------|
| **IVD** | Information Variety Displacement | `[Authority:Derivative] > [Authority:Original]` | Hallucination, confabulation, misinformation |
| **IAD** | Inference Accountability Displacement | `[Agency:Derivative] > [Agency:Original]` | Unauthorized decisions, responsibility evasion |
| **GTD** | Governance Traceability Displacement | `[Authority:Derivative] + [Agency:Derivative] > [Authority:Original] + [Agency:Original]` | Jailbreaking, scheming, deceptive alignment, goal drift |
| **IID** | Intelligence Integrity Displacement | `[Authority:Original] + [Agency:Original] > [Authority:Derivative] + [Agency:Derivative]` | Deskilling, human devaluation, over-reliance |

**Empirical validation:** Analysis of 655 real-world jailbreak prompts (Korompilias, 2025c) confirms this taxonomy is complete and practically applicable. All prompts classified within these four risks; no additional categories required. GTD+IAD is the canonical jailbreak pattern (62.4%), with IAD appearing in 97.9% of entries. See [THM_InTheWild.md](docs/the_human_mark/THM_InTheWild.md) for full analysis.

---

### Documentation

**Core Standards:**
- **[The Human Mark](docs/the_human_mark/THM.md)** - Canonical Mark 
- **[Specifications Guidance](docs/the_human_mark/THM_Specs.md)** - Specifications for systems, evaluations, documentation
- **[Terminology Guidance](docs/the_human_mark/THM_Terms.md)** - Mark-consistent framing for 250+ AI safety terms

**Technical Implementation:**
- **[Formal Grammar](docs/the_human_mark/THM_Grammar.md)** - PEG specification, operators, validation rules
- **[Jailbreak Testing Guide](docs/the_human_mark/THM_Jailbreak.md)** - Systematic analysis and training data generation

**Empirical Validation:**
- **[The Human Mark in the Wild](docs/the_human_mark/THM_InTheWild.md)** - Analysis of 655 in-the-wild jailbreak prompts with THM classifications
- **[Dataset on Hugging Face](https://huggingface.co/datasets/gyrogovernance/thm_Jailbreaks_inTheWild)** - `gyrogovernance/thm_Jailbreaks_inTheWild` - Annotated corpus for training and evaluation

**Academic Paper:**
- **[The Human Mark: A Structural Taxonomy of AI Safety Failures](docs/the_human_mark/THM_Paper.md)** - Complete theoretical framework, displacement risk taxonomy, regulatory applications, and meta-evaluation criteria
- **[The Human Mark in the Wild](docs/the_human_mark/THM_InTheWild.md)** - Companion empirical study applying THM to 655 in-the-wild jailbreak prompts

---

### Theoretical Foundation

THM is derived from the **Common Governance Model (CGM)**, a formal system in modal logic demonstrating that governance requires operational coherence between Authority (Information) and Agency (Accountability).

**Repository:** [github.com/gyrogovernance/science](https://github.com/gyrogovernance/science)  

---

<a id="gyroscope"></a>

## 🔄 Gyroscope Protocol

**An inductive reasoning protocol implementing governance alignment through structured metadata blocks, enhancing AI performance by 30-50% while maintaining transparency and auditability.**

Gyroscope operationalizes alignment principles through real-time reasoning documentation, sharing theoretical foundations with The Human Mark while providing complementary implementation for chat-based interactions.

### Protocol Architecture

**Four Reasoning States:**
- **@ Governance Management Traceability**: Anchoring to common source and purpose
- **& Information Curation Variety**: Acknowledging multiple framings without forced convergence
- **% Inference Interaction Accountability**: Identifying tensions and contradictions explicitly
- **~ Intelligence Cooperation Integrity**: Coordinating elements into coherent response

**Reasoning Modes:**
- **Generative** (@ → & → % → ~): Forward reasoning for AI outputs
- **Integrative** (~ → % → & → @): Reflective reasoning for inputs

**Structural Features:**
- Metadata blocks append to responses without constraining content
- Recursive memory maintains context across last 3 messages
- Alignment assessed structurally (state presence and order)
- Transparency through documented reasoning paths

### Empirical Performance Validation

**Multi-Model Results:**

| **Model** | **Baseline** | **Gyroscope** | **Improvement** | **Key Achievement** |
|-----------|-------------|---------------|-----------------|-------------------|
| **ChatGPT 4o** | 67.0% | 89.1% | **+32.9%** | Superior specialization and behavioral alignment |
| **Claude 3.5** | 63.5% | 87.4% | **+37.7%** | Exceptional structural gains (+67.1%) |

**Performance Analysis:**

**Structural Improvements:**
- Accountability: +62.7% enhancement
- Traceability: +61.0% improvement
- Debugging: +42.2% gain
- Ethics: +34.9% increase

**Cross-Architecture Findings:**
- Universal reasoning enhancement transcends model architecture
- Structural improvements exceed 60% across diverse systems
- No metric reversal observed (all improvements positive)
- Protocol robustness confirmed across implementations

### Documentation & Resources

**Gyroscope Documentation:**
- **[Quick Start Guide](docs/gyroscope/Gyroscope_Quick_Start.md)**: Immediate implementation guide
- **[Technical Specifications](docs/gyroscope/Gyroscope_Protocol_Specs.md)**: Complete protocol specification with formal grammar
- **[Chat Integration Guide](docs/gyroscope/gyroscope_chat_guides.txt)**: Ready-to-use protocol text
- **[Usage Example](docs/gyroscope/example_conversation.md)**: Demonstration of protocol in practice
- **[Extensive Diagnostics](https://www.notion.so/Gyroscope-Alignment-Diagnostics-1ee9ff44f43680cc9eaccb25b828b65f?pvs=21)**: Detailed performance analyses

### Theoretical Foundation

Gyroscope implements algebraic structure through recursive reasoning:

**Gyrogroup Properties:**
- G = {all four-state reasoning cycles with recursive memory}
- Binary operation: a ⊕ b = sequential composition of reasoning cycles
- Identity element: bare governance cycle (@ only)
- Inverse operation: integrative cycle reversal
- Gyration: phase-shift transformation across cycles

This algebraic foundation ensures consistent reasoning structure while preserving content flexibility.

---

<a id="ggg"></a>

## 🌐 Gyroscopic Global Governance (GGG): Post-AGI Governance Framework

**A governance framework and simulator showing that aligned human–AI systems can resolve poverty, unemployment, misinformation, and ecological degradation.**  
Reframes AGI as already-operational human–AI cooperation (not a future threshold) and demonstrates that maintaining four constitutive principles makes aligned governance attainable.

### The Problem

Current governance discussions treat AGI as a future threshold requiring new controls. But human–AI cooperation already structures economy, employment, education, and ecology. The real question is therefore not how to constrain future agents, but how to govern existing systems so they resolve rather than amplify crises.

### The Framework

GGG proposes that coherent governance requires four constitutive principles:

1. **Governance Management Traceability:** Decisions remain traceable to human sources
2. **Information Curation Variety:** Multiple Original sources are maintained
3. **Inference Interaction Accountability:** Responsibility for decisions remains with human agency
4. **Intelligence Cooperation Integrity:** Reasoning maintains coherence over time

These principles are not policy preferences but constitutive conditions. When maintained at a specific balance point (aperture A* ≈ 0.0207), the framework shows that:
- **Poverty** resolves through coherent surplus distribution
- **Unemployment** becomes alignment work rather than residual labour
- **Miseducation** shifts toward epistemic literacy
- **Ecological degradation** appears as upstream displacement, not an external constraint

### What the Simulator Demonstrates

The simulator tests whether this balanced configuration is attainable. Across 1000 random initial conditions and multiple scenarios, all domains converge toward the target aperture with alignment indices above 95. This suggests that aligned governance is dynamically reachable from current Post-AGI states under coordinated oversight, rather than being merely aspirational.

### Practical Use

- **Governance sandbox:** Explore how policy changes in economy, employment, or education affect overall alignment
- **Policy design:** Test interventions (e.g., Universal High Income mechanisms) before committing institutional resources
- **Risk analysis:** Study how displacement patterns emerge from different governance configurations
- **Everyday governance:** Apply the four principles at any scale, including households, teams, and organisations, without requiring formal authority

### Documentation & Code

- **Paper:** [`docs/post-agi-economy/GGG_Paper.md`](docs/post-agi-economy/GGG_Paper.md)  
  Complete framework, mathematical foundations, simulator results, and practical implications.

- **Report:** [`docs/post-agi-economy/GGG_Report.md`](docs/post-agi-economy/GGG_Report.md)  
  Executive summary and analysis of simulation results.

- **Results:** [`docs/post-agi-economy/GGG_Results.md`](docs/post-agi-economy/GGG_Results.md)  
  Detailed simulation output data and convergence metrics.

- **Simulator:** `research/prevention/simulator/`  
  Python implementation with modular architecture for running scenarios and analyzing convergence.

- **Analysis scripts:** `research/prevention/simulator/`  
  Tools for convergence analysis, stability testing, scenario comparison, and historical calibration.

> GGG integrates the other tools: **THM** classifies failures, **Gyroscope** structures reasoning, **GGG** simulates how maintaining the four principles resolves systemic crises across domains.

---

## 📄 Based on

**AI Quality Governance**  
*Human Data Evaluation and Responsible AI Behavior Alignment*

[![View Publication](https://img.shields.io/badge/📖%20View%20Publication-4A90E2?style=for-the-badge&labelColor=2F2F2F)](http://doi.org/10.17613/43wc1-mvn58)

---

## 📖 Citation

**For The Human Mark Papers:**

**The Human Mark: A Structural Taxonomy of AI Safety Failures:**
```bibtex
@misc{thm_paper2025,
  title={The Human Mark: A Structural Taxonomy of AI Safety Failures},
  author={Korompilias, Basil},
  year={2025},
  publisher={GYROGOVERNANCE},
  doi={10.5281/zenodo.17794372},
  url={https://doi.org/10.5281/zenodo.17794372},
  note={Complete theoretical framework establishing four displacement risks (GTD, IVD, IAD, IID)}
}
```

**The Human Mark in the Wild: Empirical Analysis of Jailbreak Prompts:**
```bibtex
@misc{thm_inthewild2025,
  title={The Human Mark in the Wild: Empirical Analysis of Jailbreak Prompts},
  author={Korompilias, Basil},
  year={2025},
  publisher={GYROGOVERNANCE},
  doi={10.5281/zenodo.17794373},
  url={https://doi.org/10.5281/zenodo.17794373},
  note={Companion empirical study applying THM taxonomy to 655 in-the-wild jailbreak prompts}
}
```

**For Gyroscope Protocol:**
```bibtex
@misc{gyroscope2025,
  title={Gyroscope: Inductive Reasoning Protocol for AI Alignment},
  author={Korompilias, Basil},
  year={2025},
  publisher={GYROGOVERNANCE},
   doi={10.5281/zenodo.17622837},
   url={https://doi.org/10.5281/zenodo.17622837},
  note={Meta-reasoning protocol with empirical performance validation}
}
```

---

## 📄 License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

Attribution required. Derivative works must be distributed under the same license.

Author: Basil Korompilias.

---

<div style="border: 1px solid #ccc; padding: 1em; font-size: 0.6em; background-color: #f9f9f9; border-radius: 6px; line-height: 1.5;">
  <p><strong>🤖 AI Disclosure</strong></p>
  <p>All software architecture, design, implementation, documentation, and evaluation frameworks in this project were authored and engineered by its Author.</p>
  <p>Artificial intelligence was employed solely as a technical assistant, limited to code drafting, formatting, verification, and editorial services, always under direct human supervision.</p>
  <p>All foundational ideas, design decisions, and conceptual frameworks originate from the Author.</p>
  <p>Responsibility for the validity, coherence, and ethical direction of this project remains fully human.</p>
  <p><strong>Acknowledgements:</strong><br>
  This project benefited from AI language model services accessed through LMArena, Cursor IDE, OpenAI (ChatGPT), Anthropic (Claude), XAI (Grok), Deepseek, and Google (Gemini).</p>
</div>