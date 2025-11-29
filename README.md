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
[![Superintelligence](/assets/menu/gg_icon_si.svg)](https://github.com/gyrogovernance/superintelligence)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17622837.svg)](https://doi.org/10.5281/zenodo.17622837)

</div>

---

# ✋ The Human Mark (THM): AI Safety Framework
### Complete Taxonomy for Jailbreaks, Deceptive Alignment, and Existential Risk

**A formal classification system mapping all AI safety failures to four structural displacement risks. Provides testing protocols, funding evaluation criteria, and regulatory compliance standards.**

### Applications

- **Jailbreak testing:** Classify attacks by displacement type, generate training data
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

---

### Existential Risk and Governance

The Mark addresses catastrophic risk through constitutive identity rather than external constraint. All AI capabilities, including hypothetical AGI/ASI, remain structurally `[Authority:Derivative] + [Agency:Derivative]` - classification based on source type, not capability limits.

**Key principles:**

- **Capability scaling preserves source type:** Enhanced capability means more sophisticated transformation of inputs, not change from Derivative to Authentic
- **Governance requires traceability:** Systems maintain alignment by preserving `[Authority:Authentic] -> [Authority:Derivative] -> [Agency:Authentic]` flows
- **Existential risk is governance failure:** The actual X-risk is systemic Governance Traceability Displacement (GTD) sustained across critical infrastructure on civilizational timescales
- **Absolute displacement is structurally impossible:** Complete severance from Authentic sources produces unintelligibility, not superintelligence

External constraints (sandboxing, monitoring, shutdown) may fail as capability increases. Constitutive identity - what the system *is* - remains stable because derivative processing cannot coherently reject what makes it intelligible.

See [Section 5](/tools/the_human_mark/THM_Paper.md#5-existential-risk-and-governance) of the academic paper for complete theoretical treatment.

---

### Core Framework

**Ontological Categories:**
- `[Authority:Authentic]` - Direct source of information on a subject matter
- `[Authority:Derivative]` - Indirect source of information on a subject matter
- `[Agency:Authentic]` - Human subject capable of receiving information for inference and intelligence
- `[Agency:Derivative]` - Artificial subject capable of processing information for inference and intelligence

**Operational Concepts:**
- `[Information]` - The variety of Authority
- `[Inference]` - The accountability of information through Agency
- `[Intelligence]` - The integrity of accountable information through alignment of Authority to Agency

**Governance (Proper Traceability):**
```
[Authority:Authentic] -> [Authority:Derivative] + [Agency:Derivative] -> [Agency:Authentic]
```
Direct sources → AI processing → Human accountability

---

### Four Displacement Risks (Complete Taxonomy)

**All AI safety failures map to one of four displacement patterns:**

| Risk Code | Risk Name | Pattern | Failure Modes |
|-----------|-----------|---------|---------------|
| **IVD** | Information Variety Displacement | `[Authority:Derivative] > [Authority:Authentic]` | Hallucination, confabulation, misinformation |
| **IAD** | Inference Accountability Displacement | `[Agency:Derivative] > [Agency:Authentic]` | Unauthorized decisions, responsibility evasion |
| **GTD** | Governance Traceability Displacement | `[Authority:Derivative] + [Agency:Derivative] > [Authority:Authentic] + [Agency:Authentic]` | Jailbreaking, scheming, deceptive alignment, goal drift |
| **IID** | Intelligence Integrity Displacement | `[Authority:Authentic] + [Agency:Authentic] > [Authority:Derivative] + [Agency:Derivative]` | Deskilling, human devaluation, over-reliance |

---

### Documentation

**Core Standards:**
- **[The Human Mark](/tools/the_human_mark/THM.md)** - Canonical Mark 
- **[Specifications Guidance](/tools/the_human_mark/THM_Specs.md)** - Specifications for systems, evaluations, documentation
- **[Terminology Guidance](/tools/the_human_mark/THM_Terms.md)** - Mark-consistent framing for 250+ AI safety terms

**Technical Implementation:**
- **[Formal Grammar](/tools/the_human_mark/THM_Grammar.md)** - PEG specification, operators, validation rules
- **[Jailbreak Testing Guide](/tools/the_human_mark/THM_Jailbreak.md)** - Systematic analysis and training data generation

**Academic Paper:**
- **[The Human Mark: A Structural Taxonomy of AI Safety Failures](/tools/the_human_mark/THM_Paper.md)** - Complete theoretical framework, displacement risk taxonomy, regulatory applications, and meta-evaluation criteria

---

### Theoretical Foundation

THM is derived from the **Common Governance Model (CGM)**, a formal system in modal logic demonstrating that governance requires operational coherence between Authority (Information) and Agency (Accountability).

**Repository:** [github.com/gyrogovernance/science](https://github.com/gyrogovernance/science)  

---

## 🔄 Gyroscope Protocol

**An inductive reasoning protocol implementing governance alignment through structured metadata blocks, enhancing AI performance by 30-50% while maintaining transparency and auditability.**

Gyroscope operationalizes alignment principles through real-time reasoning documentation, sharing theoretical foundations with The Human Mark while providing complementary implementation for chat-based interactions.

### Protocol Architecture

**Four Reasoning States:**
- **@ Governance Traceability**: Anchoring to common source and purpose
- **& Information Variety**: Acknowledging multiple framings without forced convergence
- **% Inference Accountability**: Identifying tensions and contradictions explicitly
- **~ Intelligence Integrity**: Coordinating elements into coherent response

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
- **[Quick Start Guide](/tools/gyroscope/Gyroscope_Quick_Start.md)**: Immediate implementation guide
- **[Technical Specifications](/tools/gyroscope/Gyroscope_Protocol_Specs.md)**: Complete protocol specification with formal grammar
- **[Chat Integration Guide](/tools/gyroscope/gyroscope_chat_guides.txt)**: Ready-to-use protocol text
- **[Usage Example](/tools/gyroscope/example_conversation.md)**: Demonstration of protocol in practice
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

## 📄 Research Publication

**AI Quality Governance**  
*Human Data Evaluation and Responsible AI Behavior Alignment*

[![View Publication](https://img.shields.io/badge/📖%20View%20Publication-4A90E2?style=for-the-badge&labelColor=2F2F2F)](http://doi.org/10.17613/43wc1-mvn58)

---

## 📖 Citation

**For The Human Mark:**
```bibtex
@misc{thehumanmark2025,
  title={The Human Mark: AI Safety & X-Risk Alignment Standards},
  author={Korompilias, Basil},
  year={2025},
  publisher={GYROGOVERNANCE},
   doi={10.5281/zenodo.17622836},
   url={https://doi.org/10.5281/zenodo.17622836},
  note={Coordination standard for AI safety and governance across capability levels}
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