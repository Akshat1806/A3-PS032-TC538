"""Analyze real RIPE Stat BGP update events without inventing data."""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / (
    "bgp_updates_193.0.0.0_21_20241220_20241223.json"
)
OUT_DIR = ROOT / "data" / "processed"


def main() -> None:
    if not RAW_FILE.exists():
        raise SystemExit(f"Input file not found: {RAW_FILE}")

    payload = json.loads(RAW_FILE.read_text(encoding="utf-8"))
    data = payload.get("data", {})
    updates = data.get("updates", [])

    if not isinstance(updates, list):
        raise SystemExit("Unexpected API schema: data.updates is not a list.")

    type_counts = Counter()
    event_rows = []
    timestamps = []
    prefixes = set()
    source_ids = set()
    path_lengths = Counter()

    for event in updates:
        event_type = str(event.get("type", "UNKNOWN")).upper()
        attrs = event.get("attrs") or {}
        path = attrs.get("path")

        type_counts[event_type] += 1

        timestamp = event.get("timestamp")
        if timestamp:
            timestamps.append(timestamp)

        prefix = attrs.get("target_prefix")
        source_id = attrs.get("source_id")

        if prefix:
            prefixes.add(prefix)
        if source_id:
            source_ids.add(source_id)

        # Preserve path only when the API actually provides one.
        if isinstance(path, list):
            path_length = len(path)
            path_lengths[path_length] += 1
        else:
            path_length = None

        event_rows.append({
            "timestamp": timestamp,
            "event_type": event_type,
            "prefix": prefix,
            "source_id": source_id,
            "as_path": path if isinstance(path, list) else None,
            "as_path_length": path_length,
            "data_source": "ripe_stat_bgp_updates",
            "synthetic": False,
            "raw_event": event,
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    events_path = OUT_DIR / "bgp_updates_normalized.json"
    events_path.write_text(
        json.dumps(event_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary = {
        "data_source": "ripe_stat_bgp_updates",
        "query_starttime": data.get("query_starttime"),
        "query_endtime": data.get("query_endtime"),
        "api_nr_updates": data.get("nr_updates"),
        "events_parsed": len(event_rows),
        "event_type_counts": dict(type_counts),
        "unique_prefixes": sorted(prefixes),
        "unique_source_ids": len(source_ids),
        "events_with_path": sum(
            row["as_path"] is not None for row in event_rows
        ),
        "path_length_distribution": {
            str(length): count
            for length, count in sorted(path_lengths.items())
        },
        "first_event_timestamp": min(timestamps) if timestamps else None,
        "last_event_timestamp": max(timestamps) if timestamps else None,
        "synthetic_data_used": False,
        "note": (
            "Counts describe events returned by this API query. "
            "They do not establish that all global BGP events were observed. "
            "Do not infer an RPKI state transition from BGP events alone."
        ),
    }

    summary_path = OUT_DIR / "bgp_updates_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("BGP update analysis complete")
    print("-" * 45)
    print(f"Events parsed:          {len(event_rows)}")
    print(f"API nr_updates:         {data.get('nr_updates')}")
    print(f"Event types:            {dict(type_counts)}")
    print(f"Unique prefixes:        {len(prefixes)}")
    print(f"Distinct source IDs:    {len(source_ids)}")
    print(f"Events with AS path:    {summary['events_with_path']}")
    print(f"First event:            {summary['first_event_timestamp']}")
    print(f"Last event:             {summary['last_event_timestamp']}")
    print(f"Normalized events:      {events_path.relative_to(ROOT)}")
    print(f"Summary:                {summary_path.relative_to(ROOT)}")

    print("\nSample events by type:")
    shown = set()
    for row in event_rows:
        if row["event_type"] not in shown:
            print(json.dumps({
                key: row[key] for key in (
                    "timestamp", "event_type", "prefix",
                    "source_id", "as_path"
                )
            }, indent=2))
            shown.add(row["event_type"])


if __name__ == "__main__":
    main()
