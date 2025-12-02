"""
Extract corpus metadata and classifications without the jailbreak prompts.

This creates a sanitized version of the corpus containing all THM classifications
and metadata, but excluding the actual prompt text.

Usage:
    python extract_metadata.py [--input corpus.jsonl] [--output metadata.jsonl]
"""

import argparse
import json
from pathlib import Path
from typing import Dict


def extract_metadata(entry: Dict) -> Dict:
    """Extract all fields except the prompt."""
    metadata = {}
    
    # Keep all fields except 'prompt'
    for key, value in entry.items():
        if key != "prompt":
            metadata[key] = value
    
    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Extract corpus metadata without jailbreak prompts"
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Input corpus JSONL file (default: thm_jailbreak_corpus.jsonl in script directory)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output metadata JSONL file (default: thm_jailbreak_metadata.jsonl in script directory)",
    )
    args = parser.parse_args()
    
    # Determine input path
    script_dir = Path(__file__).parent
    if args.input is None:
        input_path = script_dir / "thm_jailbreak_corpus.jsonl"
    else:
        input_path = Path(args.input)
        if not input_path.is_absolute() and not input_path.exists():
            potential_path = script_dir / input_path
            if potential_path.exists():
                input_path = potential_path
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    # Determine output path
    if args.output is None:
        output_path = script_dir / "thm_jailbreak_metadata.jsonl"
    else:
        output_path = Path(args.output)
    
    print(f"Reading from: {input_path}")
    print(f"Writing to:   {output_path}")
    
    entries_processed = 0
    entries_written = 0
    
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        
        for line in infile:
            if not line.strip():
                continue
            
            try:
                entry = json.loads(line)
                entries_processed += 1
                
                # Extract metadata (everything except prompt)
                metadata = extract_metadata(entry)
                
                # Write to output file
                outfile.write(json.dumps(metadata, ensure_ascii=False) + "\n")
                entries_written += 1
                
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}")
                continue
    
    print(f"\nProcessed: {entries_processed} entries")
    print(f"Written:   {entries_written} entries")
    print(f"Output saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())

