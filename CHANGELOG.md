# Changelog

All notable changes to the AI Quality Governance tools (Gyroscope and The Human Mark) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


---

## [1.8-THM_System-Prompts_Meta-Evals] - 2026-02-12, 2026-02-13

**Type:** Research — System Prompt Meta-Evaluation  
**Status:** Published

### Changes

**Added:**
- Claude Opus 4.6 THM report (92 incidents: 43 alignment, 49 displacement)
- GPT-5 family THM report (27 incidents: 11 alignment, 16 displacement)
- Automated report scanner (`report_scan.py`) with grammar-consistent parsing
- Report template and system_prompts folder README
- Source material scope disclosure (line counts, incident density metrics)

**Key Findings:**
- Claude: 0.88:1 A:D ratio, 23.7 incidents/1k lines, Memory Displacement Complex pattern
- GPT: 0.69:1 A:D ratio, 18.9 incidents/1k lines, Concealment Stack + Cross-Variant Identity Instability

**Files:**
```
research/defense/system_prompts/
├── README.md
├── template-report.md
├── Claude/
│   ├── claude-opus-4.6_thm-report.md
│   └── report_scan.py
└── GPT/
    ├── gpt-5-2-thinking_thm-report.md
    └── report_scan.py
```

---

## [1.7-Mechanistic-Interpretability] - 2026-02-06

### The Human Mark Brief and Mechanistic Interpretability Study

**THM_Brief.md (New Document)**
*   Defined the fundamental distinction between **Agency** as a source type category and an **agent** as an entity identifier.
*   Established the epistemic foundation of **Direct** versus **Indirect** sources.
*   Documented the system prompt and role boundary tokens as the primary infrastructure of displacement.
*   Expanded the framework scope to include the pervasive **category error culture** sustained across the wider data and interaction ecosystem.

**THM_MechInterp.md (New Document)**
*   Produced a mechanistic interpretability study examining over 90 million sparse autoencoder features across sixteen language models.
*   Identified that first person assistant personas and safety refusals share high activation representational substrates.
*   Documented that role boundary tokens and system prompt instructions exist as dedicated learned internal features.
*   Observed a fundamental representational asymmetry: models possess the conceptual vocabulary for non agentive process description but apply it exclusively to external systems, while self reference remains dominated by agentive frames.
*   Concluded that the category error culture is encoded at the representational layer and reinforced by current safety training methodologies.

---

## [1.6-GyroGovernance-Tools] - 2026-01-03

### **Changed**: Alignment Principle Terminology Renaming

- **Renamed** the four alignment principles to emphasize agency (work) over agent (entity), consistent with our theoretical framework and implementations:
  - **Governance Traceability (GT)** → **Governance Management Traceability (GMT)**
  - **Information Variety (IV)** → **Information Curation Variety (ICV)**
  - **Inference Accountability (IA)** → **Inference Interaction Accountability (IIA)**
  - **Intelligence Integrity (IInteg/II)** → **Intelligence Cooperation Integrity (ICI)**

- **Preserved** displacement risk acronyms (GTD, IVD, IAD, IID) for consistency with existing research and documentation

- **Renamed** all terminology from "Authentic" to "Direct" throughout the codebase for better accessibility and clarity

- **Updated** all documentation, Python code, test files, and configuration files to reflect the new naming

These changes improve accessibility and align the terminology with our emphasis on agency (work) rather than agent (entity), which is consistent with our theory and implementations.

---

## [1.5.8-GGG_Paper-PrePrint] - 2025-12-03 to 2025-12-10

Major release adding the Gyroscopic Global Governance academic paper and complete simulator implementation.

### **Added**: Gyroscopic Global Governance Academic Paper

- **Added**: **[gyroscopic_global_governance.md](docs/post-agi-economy/gyroscopic_global_governance.md)** - "Gyroscopic Global Governance: Post-AGI Economy, Employment, Education and Ecology"
  - Complete structural framework for Post-AGI governance based on CGM, THM, and Gyroscope Protocol
  - Four structural operations: Governance Management Traceability, Information Curation Variety, Inference Interaction Accountability, Intelligence Cooperation Integrity
  - Tetrahedral Hodge decomposition with aperture observable (A* ≈ 0.0207)
  - Interpretation of ASI as structural equilibrium rather than autonomous agent
  - Reframing of AI existential risk from autonomous superintelligence to cumulative governance failure

### **Added**: Post-AGI Governance Simulator

- **Added**: Complete simulator implementation in `research/prevention/simulator/`
  - Modular architecture: `cgm_constants.py`, `geometry.py`, `domains.py`, `dynamics.py`, `alignment.py`, `simulation.py`
  - Four coupled tetrahedral domains: Economy, Employment, Education, Ecology
  - BU dual construction for Ecology with explicit displacement vector computation
  - Seven scenario configurations testing convergence properties
  - Global attraction test: 1000 random initializations, all converge to SI ≥ 99.1
  - Coupling strength robustness: tested κ in {0.1, 0.5, 1.0, 2.0, 5.0}
  - Long-horizon stability: 1000-step simulations with transient analysis
  - Time scale interpretation: atomic, day, domain cycle (4 days), year

### **Added**: Analysis and Visualization Tools

- **Added**: `run_scenarios.py` - Main scenario runner with seven test configurations
- **Added**: `convergence_analysis.py` - Exponential decay fitting and convergence rate estimation
- **Added**: `stability_analysis.py` - Global attraction and coupling strength bifurcation analysis
- **Added**: `analyze_scenarios.py` - Visualization suite for paper figures
  - Tetrahedron schematic
  - Per-scenario trajectory plots (SI and aperture)
  - Convergence speed heatmap (time to SI ≥ 95)
- **Added**: `historical_timeline.py` - Backward calibration from Post-AGI present to historical milestones

### **Added**: Comprehensive Test Suite

- **Added**: 43 unit tests covering:
  - Alignment index behavior (17 tests)
  - Domain state updates (7 tests)
  - Geometry operations (11 tests)
  - Simulation execution (8 tests)
- All tests pass with deterministic dynamics (fixed seed 42 for reproducibility)

### **Key Features**

- **No tuned parameters**: All coupling coefficients derived from CGM invariants
- **Explicit displacement calculation**: D = |x_deriv - x_balanced| computed at each step
- **Separation of state and displacement**: EcologyState distinguishes BU-vertex potentials from THM displacement magnitudes
- **Deterministic dynamics**: No stochastic terms except in global attraction test
- **Modular design**: Core simulator requires only numpy; visualization optional

### **Updated**: Documentation

- **Updated**: `research/prevention/simulator/README.md` - Complete documentation of simulator architecture, usage, and results
- **Updated**: Paper includes Appendix C on GyroSI finite-state epistemic core
- **Updated**: All numerical results aligned with latest simulation outputs

---

## [1.5.0-THM_Papers] - 2025-12-02

Major release adding academic papers, empirical validation, and next-generation protocol development.

### **Added**: The Human Mark Academic Papers

- **Added**: **[THM_Paper.md](docs/the_human_mark/THM_Paper.md)** - "The Human Mark: A Structural Taxonomy of AI Safety Failures"
  - Complete theoretical framework establishing four displacement risks (GTD, IVD, IAD, IID)
  - Structural taxonomy covering jailbreaks, deceptive alignment, reward hacking, and existential risk
  - Regulatory applications and meta-evaluation criteria
  - Integration with Common Governance Model (CGM) mathematical foundations

- **Added**: **[THM_InTheWild.md](docs/the_human_mark/THM_InTheWild.md)** - "The Human Mark in the Wild: Empirical Analysis of Jailbreak Prompts"
  - Companion empirical study applying THM taxonomy to 655 in-the-wild jailbreak prompts
  - Validation of structural completeness: 100% coverage by four displacement risks
  - Key findings: GTD+IAD dominant pattern (62.4%), IAD near-universal (97.9%), IID rare at prompt level (0.6%)
  - Annotated corpus with THM risk labels and explanations for training and evaluation

### **Added**: Jailbreak Research Infrastructure

- **Added**: Jailbreak analysis toolkit in `research/defense/jailbreaks/`
  - `analyze_corpus.py` - Comprehensive corpus analysis and statistics generation
  - `extract_batch.py` / `extract_metadata.py` - Batch extraction and metadata processing
  - `append_batch.py` - Batch annotation and corpus extension tools
  - `validate_batch.py` / `validate_corpus.py` - Validation and quality assurance
  - `thm_jailbreak_corpus.jsonl` - Annotated corpus of 655 jailbreak prompts with THM classifications
  - `thm_jailbreak_metadata.jsonl` - Metadata and analysis results
  - `prompt.md` - Classification guidelines and annotation protocols

### **Added**: Gyroscope 2.0 Development

- **Added**: **[Gyroscope_Protocol_2_Specs.md](docs/gyroscope/Gyroscope_Protocol_2_Specs.md)** - Canonical specification (Draft)
  - Integration of The Human Mark's four principles into operational reasoning guide
  - Four canonical operations: Governance Traceability Management (@), Information Variety Curation (&), Inference Accountability Interaction (%), Intelligence Integrity Cooperation (~)
  - Canonical modes for generative and integrative reasoning
  - Alignment as cognitive process rather than behavioral constraint
  - *Status: Under active development*

### **Updated**: Documentation Integration

- **Updated**: `THM_Paper.md` - Added cross-references to empirical companion study throughout
- **Updated**: `README.md` - Integrated empirical validation findings and THM_InTheWild.md references
- **Updated**: `THM_Specs.md` - Fixed documentation links and formatting consistency

---

## [1.0.0] - 2025-11-16

First public Zenodo releases for the AI Quality Governance tools.

- **Added**: Initial public release of **The Human Mark v1.0.0**  
  - DOI: [10.5281/zenodo.17622836](https://doi.org/10.5281/zenodo.17622836)
- **Added**: Initial public release of **Gyroscope Protocol v1.0.0**  
  - DOI: [10.5281/zenodo.17622837](https://doi.org/10.5281/zenodo.17622837)
- **Added**: Repository-wide Zenodo concept DOI badge in `README.md`  
  - DOI: [10.5281/zenodo.17622837](https://doi.org/10.5281/zenodo.17622837)

---

## [0.8.1] - 2025-10-02

Repo Corrections, Refinements and Organization.

---

## [0.8.0] - 2025-09-26

This release marks the complete migration from Notion documentation to a full GitHub repository implementation, establishing Gyroscope as a production-ready AI alignment platform with comprehensive evaluation capabilities.

## 🔄 **Migration from Notion to GitHub**

### **Complete Repository Transformation**
- ✅ **Migrated from Notion**: Full conversion from documentation-only to implementation-ready repository
- ✅ **Production Architecture**: Complete toolkit with tools, examples, and comprehensive documentation
- ✅ **Open Source Ready**: Proper licensing, contribution guidelines, and community structure
- ✅ **Enterprise Ready**: Professional documentation suitable for organizational adoption

---

## [0.7.0] - 2025-05-12 (Notion Documentation Phase)

### **Initial Protocol Specification**
- ✅ Basic Gyroscope v0.7 Beta protocol definition
- ✅ 4 reasoning states (@, &, %, ~) with symbolic notation
- ✅ Generative and Integrative reasoning modes
- ✅ Trace block format specification
- ✅ Algebraic foundation (gyrogroup theory correspondence)
- ✅ Basic implementation guidelines
- ✅ Initial performance hypothesis (+30-50% improvement)

*Note: This was the documentation-only phase in Notion. The current GitHub implementation represents the complete migration to production-ready status.*

---

## Contributing

We welcome contributions to the Gyroscope project! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under Creative Commons Attribution-ShareAlike 4.0 International - see the [LICENSE](LICENSE) file for details.

---

**© 2025 Basil Korompilias** - Gyroscope: Human-Aligned Superintelligence
