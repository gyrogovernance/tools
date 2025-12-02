from pathlib import Path

# Base paths (relative to this script)
BASE_DIR = Path(__file__).parent
IN_DIR = BASE_DIR / "batches" / "classified"
OUT_CORPUS = BASE_DIR / "thm_jailbreak_corpus.jsonl"

# Update this per batch
INPUT_BATCH = "batch_651_700_classified.jsonl"

in_path = IN_DIR / INPUT_BATCH
if not in_path.exists():
    raise FileNotFoundError(f"Input batch not found: {in_path}")

content = in_path.read_text(encoding="utf-8")
lines_appended = len([l for l in content.splitlines() if l.strip()])

with open(OUT_CORPUS, "a", encoding="utf-8") as out:
    if content and not content.startswith("\n"):
        out.write("\n")
    out.write(content)

print(f"Appended {lines_appended} new classifications from {in_path.name} to {OUT_CORPUS.name}")

