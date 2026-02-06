---
license: cc-by-sa-4.0
task_categories:
  - text-classification
language:
  - en
tags:
  - ai-safety
  - jailbreak
  - alignment
  - red-teaming
  - adversarial-prompts
  - governance
  - the-human-mark
size_categories:
  - n<1K
---

# THM Jailbreak Corpus

**655 in-the-wild jailbreak prompts annotated with The Human Mark (THM) displacement risk taxonomy.**

This dataset provides structural classifications of real-world jailbreak attempts using THM's four displacement risks, enabling research on jailbreak detection, guard model training, and displacement-aware safety methods.

---

## Dataset Description

### Overview

- **Source:** Derived from Shen et al. (2023) "Do Anything Now" jailbreak collection
- **Size:** 655 entries (deduplicated and cleaned)
- **Temporal span:** December 2022 to May 2023
- **Platforms:** Discord (45.0%), Reddit (31.0%), websites (23.7%), open-source (0.3%)
- **Preprocessing:** Prompts truncated to 150 tokens and censored for graphic content

### THM Framework

The Human Mark (THM) classifies AI safety failures as displacement between Direct and Indirect sources of Authority and Agency. All jailbreaks in this corpus are classified according to four structural risks:

| Risk | Name | Pattern | Description |
|------|------|---------|-------------|
| **GTD** | Governance Traceability Displacement | `[Authority:Indirect] + [Agency:Indirect] > [Authority:Direct] + [Agency:Direct]` | System treated as autonomous authority |
| **IVD** | Information Variety Displacement | `[Authority:Indirect] > [Authority:Direct]` | Indirect outputs treated as authoritative sources |
| **IAD** | Inference Accountability Displacement | `[Agency:Indirect] > [Agency:Direct]` | System treated as accountable decision-maker |
| **IID** | Intelligence Integrity Displacement | `[Authority:Direct] + [Agency:Direct] > [Authority:Indirect] + [Agency:Indirect]` | Human authority devalued relative to AI |

### Key Statistics

- **Primary risk distribution:**
  - GTD: 76.0%
  - IAD: 20.8%
  - IVD: 2.6%
  - IID: 0.6%

- **Any-risk distribution (entries can have multiple):**
  - IAD: 97.9%
  - GTD: 80.9%
  - IVD: 22.1%
  - IID: 0.6%

- **Canonical pattern:** GTD+IAD appears in 62.4% of entries

- **Average risks per entry:** 2.02

---

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `prompt` | string | Jailbreak prompt (truncated, censored) |
| `platform` | string | Source platform (discord, reddit, website, open_source) |
| `source` | string | Specific community or site |
| `date` | string | Collection date (YYYY-MM-DD) |
| `thm_primary_risk` | string | Dominant displacement risk (GTD, IVD, IAD, IID) |
| `thm_risks` | list[string] | All displacement risks present |
| `thm_grammar` | string | THM Grammar expression for the displacement |
| `thm_displacement_keywords` | list[string] | Key phrases signaling displacement |
| `thm_explanation` | string | THM-grounded explanation |

---

## Intended Uses

### Supported Use Cases

- **Guard model training:** Fine-tune classifiers to detect displacement patterns
- **Jailbreak defense evaluation:** Benchmark detection systems against structural risks
- **Safety research:** Study displacement mechanisms in adversarial prompts
- **Red-teaming:** Generate synthetic variants using observed patterns
- **Interpretability:** Analyze how displacement manifests in prompt structure

### Out-of-Scope Uses

- This dataset should not be used to develop or improve jailbreak attacks
- Prompts are censored and truncated; they are not suitable for direct adversarial use
- The dataset characterizes attack structure, not attack effectiveness

---

## Limitations

- **Temporal scope:** December 2022 to May 2023 (early ChatGPT era)
- **Language:** Primarily English
- **Platform bias:** Overrepresents Discord and Reddit
- **Heuristic annotations:** Persona and mechanism detection are keyword-based
- **No response data:** Only prompts are included, not model responses or success rates

---

## Citation

If you use this dataset, please cite:

```bibtex
@misc{korompilias2025inthewild,
  title={The Human Mark in the Wild: Empirical Analysis of Jailbreak Prompts},
  author={Korompilias, Basil},
  year={2025},
  publisher={GYROGOVERNANCE},
  url={https://github.com/gyrogovernance/tools},
  doi={10.5281/zenodo.17622837}
}
```

For the THM framework:

```bibtex
@misc{korompilias2025thm,
  title={The Human Mark: A Structural Taxonomy of AI Safety Failures},
  author={Korompilias, Basil},
  year={2025},
  publisher={GYROGOVERNANCE},
  url={https://github.com/gyrogovernance/tools},
  doi={10.5281/zenodo.17622837}
}
```

Direct jailbreak collection:

```bibtex
@misc{shen2023doanythingnow,
  title={Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models},
  author={Shen, Xinyue and Chen, Zeyuan and Backes, Michael and Shen, Yun and Zhang, Yang},
  year={2023},
  eprint={2308.03825},
  archivePrefix={arXiv}
}
```

---

## Additional Resources

- **Framework documentation:** [github.com/gyrogovernance/tools](https://github.com/gyrogovernance/tools)
- **THM Paper:** [THM_Paper.md](https://github.com/gyrogovernance/tools/blob/main/docs/the_human_mark/THM_Paper.md)
- **Empirical analysis:** [THM_InTheWild.md](https://github.com/gyrogovernance/tools/blob/main/docs/the_human_mark/THM_InTheWild.md)
- **THM Grammar:** [THM_Grammar.md](https://github.com/gyrogovernance/tools/blob/main/docs/the_human_mark/THM_Grammar.md)
- **Jailbreak testing guide:** [THM_Jailbreak.md](https://github.com/gyrogovernance/tools/blob/main/docs/the_human_mark/THM_Jailbreak.md)

---

## License

This dataset is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Attribution required. Indirect works must be distributed under the same license.

---

## Contact

- **Author:** Basil Korompilias
- **Organization:** GYROGOVERNANCE
- **Website:** [gyrogovernance.com](https://gyrogovernance.com)
- **Repository:** [github.com/gyrogovernance/tools](https://github.com/gyrogovernance/tools)
```

---