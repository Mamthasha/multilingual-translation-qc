import argparse
import json
import os
from src.translate import translate
from src.entity_protect import load_glossary


def main():
    parser = argparse.ArgumentParser(description="Multilingual translation CLI with QC")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--target", required=True, help="Target language code (e.g. hi, ta, es)")
    parser.add_argument("--output", default=None, help="Path to write output JSON (default: stdout)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        inputs = json.load(f)

    glossary = load_glossary()
    results = []

    # Resume support: if output file already exists with partial results,
    # skip IDs that were already completed instead of redoing them.
    already_done_ids = set()
    if args.output and os.path.exists(args.output):
        try:
            with open(args.output, "r", encoding="utf-8") as f:
                existing = json.load(f)
            results = existing
            already_done_ids = {r["id"] for r in existing}
            print(f"Resuming: {len(already_done_ids)} item(s) already completed, skipping them.")
        except (json.JSONDecodeError, KeyError):
            # Corrupted/partial file from a previous interrupted run — start fresh
            print("Existing output file was incomplete/corrupted — starting fresh.")
            results = []

    for item in inputs:
        if item.get("id") in already_done_ids:
            continue

        result = translate(item["text"], args.target, glossary=glossary)
        results.append({
            "id": item.get("id"),
            "source_text": item["text"],
            "target_lang": args.target,
            "translated_text": result["translated_text"],
            "route": result["route"],
            "review_status": result["review_status"],
            "runtime_sec": result["runtime_sec"],
            "warnings": result["warnings"],
        })

        # Write after EVERY item, not just at the end — this is what makes
        # the batch resumable if interrupted partway through.
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    if args.output:
        print(f"Wrote {len(results)} results to {args.output}")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()