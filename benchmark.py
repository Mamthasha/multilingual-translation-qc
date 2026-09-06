import time
import os
import json

try:
    from src.translate import translate, DIRECT_MODELS, DRAVIDIAN_MODEL, INDIC_MODEL
    from src.entity_protect import load_glossary
except ImportError:
    from translate import translate, DIRECT_MODELS, DRAVIDIAN_MODEL, INDIC_MODEL
    from entity_protect import load_glossary

import psutil


def get_model_size_mb(model_repo_folder_name):
    """Estimates size of a downloaded model from the HF cache folder."""
    cache_root = os.path.expanduser("~/.cache/huggingface/hub")
    target = os.path.join(cache_root, model_repo_folder_name)
    if not os.path.exists(target):
        return None
    total = 0
    for dirpath, _, filenames in os.walk(target):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return round(total / (1024 * 1024), 1)


def benchmark_language(text, target_lang, glossary):
    process = psutil.Process(os.getpid())

    start = time.time()
    result = translate(text, target_lang, glossary=glossary)
    elapsed = time.time() - start

    mem_after = process.memory_info().rss / (1024 * 1024)
    peak_ram_mb = round(mem_after, 1)

    return {
        "target_lang": target_lang,
        "runtime_sec": round(elapsed, 2),
        "peak_ram_mb": peak_ram_mb,
        "review_status": result["review_status"],
        "translated_text": result["translated_text"],
    }


def run_benchmark():
    glossary = load_glossary()
    text = "Hello, my name is Mamthasha and I study at SASTRA University."

    all_targets = ["hi", "ta", "te", "bn", "mr", "es", "fr", "de", "pt", "id"]
    results = []

    for lang in all_targets:
        print(f"Benchmarking {lang}...")
        r = benchmark_language(text, lang, glossary)
        results.append(r)
        print(f"  runtime: {r['runtime_sec']}s | peak RAM: {r['peak_ram_mb']}MB | status: {r['review_status']}")

    os.makedirs("data", exist_ok=True)
    with open("data/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\nBenchmark complete. Results saved to data/benchmark_results.json")


if __name__ == "__main__":
    run_benchmark()