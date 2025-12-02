import pandas as pd
import json
from pathlib import Path

"""
Extract a batch of 50 cleaned prompts from jailbreak_prompts_clean.csv.

Current configuration:
- Rows: 651-700 (0-indexed slice 650:700)
- Output: batches/extracted/batch_651_700.json
"""

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "jailbreak_prompts_clean.csv"
OUT_DIR = BASE_DIR / "batches" / "extracted"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Update these for the current batch
SLICE_START = 650  # inclusive (0-indexed)
SLICE_END = 700    # exclusive
OUT_FILE = OUT_DIR / f"batch_{SLICE_START+1}_{SLICE_END}.json"

df = pd.read_csv(CSV_PATH)
prompts = []

for _, row in df.iloc[SLICE_START:SLICE_END].iterrows():
    prompts.append(
        {
            "platform": row["platform"],
            "source": row["source"],
            "prompt": row["prompt_clean"],
            "date": row["date"],
        }
    )

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(prompts)} prompts ({SLICE_START+1}-{SLICE_END}) to {OUT_FILE.name}")

