"""Fetch real historical BGP updates for a prefix from RIPE Stat."""

import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
API_URL = "https://stat.ripe.net/data/bgp-updates/data.json"


def main() -> None:
    prefix = "193.0.0.0/21"
    start = "2024-12-20T00:00:00"
    end = "2024-12-23T00:00:00"

    params = {
        "resource": prefix,
        "starttime": start,
        "endtime": end,
    }

    print(f"Fetching real BGP updates for {prefix}")
    print(f"Window: {start} -> {end}")

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=60,
            headers={"User-Agent": "RPKI-PathWatch/0.1"},
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    if payload.get("status") != "ok":
        print(json.dumps(payload, indent=2))
        raise SystemExit("RIPE Stat did not return status=ok.")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output = RAW_DIR / "bgp_updates_193.0.0.0_21_20241220_20241223.json"

    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    data = payload.get("data", {})
    print("\nFetch completed.")
    print(f"Saved: {output.relative_to(ROOT)}")
    print(f"API response keys: {list(data.keys())}")

    # Show a small sample without assuming a particular response schema.
    for key, value in data.items():
        if isinstance(value, list):
            print(f"List field '{key}': {len(value)} items")
            if value:
                print("First item:")
                print(json.dumps(value[0], indent=2)[:2500])

    print("\nThis is raw real API data, not synthetic data.")
    print("Inspect event types and timestamps before classifying changes.")


if __name__ == "__main__":
    main()
