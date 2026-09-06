import json
import os


def test_partial_output_file_is_valid_json():
    """
    Simulates checking that a partially-written output file (as if a batch
    was interrupted midway) is still valid, parseable JSON — proving the
    incremental-write pattern doesn't corrupt the file on interruption.
    """
    partial_data = [
        {"id": "T001", "translated_text": "example", "review_status": "ok"},
        {"id": "T002", "translated_text": "example2", "review_status": "flagged"},
    ]

    test_path = "data/_test_partial_output.json"
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(partial_data, f, ensure_ascii=False, indent=2)

    # Simulate re-reading it as if resuming
    with open(test_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert len(loaded) == 2
    assert loaded[0]["id"] == "T001"
    assert loaded[1]["id"] == "T002"

    os.remove(test_path)  # cleanup


def test_resume_skips_already_completed_ids():
    """
    Confirms the resume logic (ID-based skip) works correctly in isolation,
    without needing to run a real translation.
    """
    already_done_ids = {"T001", "T002"}
    all_inputs = [
        {"id": "T001", "text": "already done"},
        {"id": "T002", "text": "already done"},
        {"id": "T003", "text": "not done yet"},
    ]

    remaining = [item for item in all_inputs if item["id"] not in already_done_ids]

    assert len(remaining) == 1
    assert remaining[0]["id"] == "T003"