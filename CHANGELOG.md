# Changelog

All notable changes to the AI Quality Governance tools (Gyroscope and The Human Mark) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
