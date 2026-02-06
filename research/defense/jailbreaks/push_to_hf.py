"""
Push the THM jailbreak corpus to Hugging Face Hub.

Usage:
    python push_to_hf.py [--readme path/to/README.md]

Requires: pip install datasets huggingface_hub
Auth: huggingface-cli login, or set HF_TOKEN
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict

REPO_ID = "gyrogovernance/thm_Jailbreaks_inTheWild"
SCRIPT_DIR = Path(__file__).parent
DEFAULT_CORPUS = SCRIPT_DIR / "thm_jailbreak_corpus.jsonl"


def load_corpus(path: Path) -> List[Dict]:
    """Load corpus from JSONL."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def main():
    parser = argparse.ArgumentParser(description="Push THM jailbreak corpus to Hugging Face")
    parser.add_argument(
        "--readme",
        default=None,
        help="Path to dataset card README.md (optional)",
    )
    parser.add_argument(
        "--corpus",
        default=str(DEFAULT_CORPUS),
        help=f"Path to corpus JSONL (default: {DEFAULT_CORPUS})",
    )
    parser.add_argument(
        "--commit-message",
        default="Update corpus and dataset card",
        help="Commit message for the push",
    )
    args = parser.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    try:
        from datasets import Dataset
    except ImportError:
        raise ImportError("Install datasets: pip install datasets")

    entries = load_corpus(corpus_path)
    print(f"Loaded {len(entries)} entries from {corpus_path}")

    ds = Dataset.from_list(entries)
    print(f"Pushing to {REPO_ID}...")

    ds.push_to_hub(REPO_ID, commit_message=args.commit_message)

    if args.readme:
        readme_path = Path(args.readme)
        if readme_path.exists():
            from huggingface_hub import HfApi
            api = HfApi()
            api.upload_file(
                path_or_fileobj=str(readme_path),
                path_in_repo="README.md",
                repo_id=REPO_ID,
                repo_type="dataset",
                commit_message=args.commit_message,
            )
            print(f"Uploaded README from {readme_path}")
        else:
            print(f"Warning: README not found: {readme_path}")
    print("Done. View at: https://huggingface.co/datasets/" + REPO_ID)


if __name__ == "__main__":
    main()
