"""Analyze normalized, real BGP route snapshots."""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "data" / "processed"


def analyze_file(path: Path) -> dict:
    routes = json.loads(path.read_text(encoding="utf-8"))

    if not routes:
        raise ValueError(f"No routes found in {path.name}")

    origins = Counter()
    path_lengths = Counter()
    source_ids = set()
    prefixes = set()
    unique_paths = set()

    for route in routes:
        origin = route.get("origin_as")
        if origin is not None:
            origins[str(origin)] += 1

        length = route.get("as_path_length")
        if length is not None:
            path_lengths[length] += 1

        if route.get("source_id"):
            source_ids.add(route["source_id"])

        if route.get("prefix"):
            prefixes.add(route["prefix"])

        as_path = route.get("as_path") or []
        if as_path:
            unique_paths.add(tuple(as_path))

    lengths = [
        route["as_path_length"]
        for route in routes
        if route.get("as_path_length") is not None
    ]

    report = {
        "input_file": path.name,
        "timestamp": routes[0].get("timestamp"),
        "data_source": routes[0].get("data_source"),
        "synthetic_data_used": any(
            route.get("synthetic", True) for route in routes
        ),
        "route_record_count": len(routes),
        "unique_prefix_count": len(prefixes),
        "unique_source_id_count": len(source_ids),
        "unique_as_path_count": len(unique_paths),
        "origin_as_counts": dict(
            origins.most_common()
        ),
        "as_path_length_distribution": {
            str(length): count
            for length, count in sorted(path_lengths.items())
        },
        "as_path_length_min": min(lengths) if lengths else None,
        "as_path_length_max": max(lengths) if lengths else None,
        "as_path_length_mean": (
            round(sum(lengths) / len(lengths), 3)
            if lengths else None
        ),
        "rpki_status": "not_analyzed_time_aligned_data_unavailable",
    }

    return report


def main() -> None:
    files = sorted(PROCESSED_DIR.glob("*_routes.json"))

    if not files:
        raise SystemExit(
            "No normalized route files found. Run src/normalize.py first."
        )

    for path in files:
        report = analyze_file(path)
        output_path = REPORT_DIR / f"{path.stem}_analysis.json"

        output_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        print(f"\nSnapshot: {path.name}")
        print("-" * 55)
        print(f"Timestamp:             {report['timestamp']}")
        print(f"Route records:         {report['route_record_count']}")
        print(f"Unique prefixes:       {report['unique_prefix_count']}")
        print(f"Distinct source IDs:   {report['unique_source_id_count']}")
        print(f"Unique AS paths:       {report['unique_as_path_count']}")
        print(f"Mean AS-path length:   {report['as_path_length_mean']}")
        print(f"Min / max path length: {report['as_path_length_min']} / "
              f"{report['as_path_length_max']}")
        print(f"Origins:               {report['origin_as_counts']}")
        print(f"Synthetic data used:   {report['synthetic_data_used']}")
        print(f"RPKI:                  {report['rpki_status']}")
        print(f"Report saved:          {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
