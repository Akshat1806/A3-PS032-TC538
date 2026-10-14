"""Compare normalized BGP snapshots; no synthetic measurements."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_snapshot(path: Path) -> dict:
    records = json.loads(path.read_text(encoding="utf-8"))
    routes = {}

    for record in records:
        key = (record.get("prefix"), record.get("source_id"))
        routes[key] = record

    timestamp = records[0].get("timestamp") if records else None
    return {"timestamp": timestamp, "routes": routes}


def main() -> None:
    files = sorted(PROCESSED.glob("*_routes.json"))

    if len(files) < 2:
        raise SystemExit(
            "Need at least two normalized snapshots. "
            "Run ingest.py for additional timestamps, then normalize.py."
        )

    snapshots = [load_snapshot(path) for path in files]
    snapshots.sort(key=lambda item: item["timestamp"] or "")

    for previous, current in zip(snapshots, snapshots[1:]):
        old = previous["routes"]
        new = current["routes"]

        old_keys = set(old)
        new_keys = set(new)

        appeared = new_keys - old_keys
        disappeared = old_keys - new_keys
        changed_path = {
            key for key in old_keys & new_keys
            if old[key].get("as_path") != new[key].get("as_path")
        }

        report = {
            "comparison": {
                "from_timestamp": previous["timestamp"],
                "to_timestamp": current["timestamp"],
            },
            "route_record_counts": {
                "before": len(old),
                "after": len(new),
            },
            "observed_new_route_keys": len(appeared),
            "observed_missing_route_keys": len(disappeared),
            "observed_changed_as_paths": len(changed_path),
            "new_routes_sample": [
                {
                    "prefix": key[0],
                    "source_id": key[1],
                    "as_path": new[key].get("as_path"),
                }
                for key in sorted(appeared)[:10]
            ],
            "missing_routes_sample": [
                {
                    "prefix": key[0],
                    "source_id": key[1],
                    "as_path": old[key].get("as_path"),
                }
                for key in sorted(disappeared)[:10]
            ],
            "changed_paths_sample": [
                {
                    "prefix": key[0],
                    "source_id": key[1],
                    "old_path": old[key].get("as_path"),
                    "new_path": new[key].get("as_path"),
                }
                for key in sorted(changed_path)[:10]
            ],
            "synthetic_data_used": False,
            "interpretation_warning": (
                "Snapshot differences are observed state differences, "
                "not a complete log of BGP announcements or withdrawals. "
                "Missing observations may reflect coverage or data gaps."
            ),
        }

        from_tag = (previous["timestamp"] or "unknown").replace(":", "").replace("-", "")
        to_tag = (current["timestamp"] or "unknown").replace(":", "").replace("-", "")
        output = PROCESSED / f"comparison_{from_tag}_to_{to_tag}.json"
        output.write_text(json.dumps(report, indent=2), encoding="utf-8")

        print(f"\n{previous['timestamp']} -> {current['timestamp']}")
        print(f"Route records:       {len(old)} -> {len(new)}")
        print(f"New route keys:      {len(appeared)}")
        print(f"Missing route keys:  {len(disappeared)}")
        print(f"Changed AS paths:    {len(changed_path)}")
        print(f"Report:              {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
