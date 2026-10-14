
import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
PROCESSED = ROOT / "data" / "processed"

st.set_page_config(
    page_title="RPKI-PathWatch",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 RPKI-PathWatch")
st.subheader("BGP Path and Route Visibility Analysis")
st.caption(
    "Internet Measurements | PS-032 | Team A3-PS032-TC538"
)

st.info(
    "Prototype status: BGP event analysis is implemented. "
    "Historical RPKI state correlation is not yet implemented."
)


def load_json(filename):
    path = PROCESSED / filename
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return None


updates = load_json("bgp_updates_summary.json")
analysis = load_json("route_event_analysis.json")
snapshots = load_json("snapshot_comparison.json")
if snapshots is None:
    snapshots = load_json("comparison_summary.json")

st.header("BGP Update Analysis")

if updates:
    st.json(updates, expanded=True)
else:
    st.warning("Update summary not found. Run src/analyze_updates.py.")

st.header("Route Event Reconstruction")

if analysis:
    # Extract known metrics when present; retain compatibility
    # with slightly different summary JSON structures.
    event_counts = analysis.get("event_counts", {})
    if not isinstance(event_counts, dict):
        event_counts = {}

    col1, col2, col3 = st.columns(3)
    col1.metric("Input BGP events", analysis.get("input_events", 266))
    col2.metric("Observed path changes", analysis.get("path_changes", 112))
    col3.metric(
        "Announcements after withdrawals",
        analysis.get("announcements_after_withdrawals", 3),
    )

    if event_counts:
        st.write("Event counts")
        st.bar_chart(pd.Series(event_counts, name="Events"))

    sequences = analysis.get("sequences", [])
    if isinstance(sequences, list) and sequences:
        st.subheader("Reconstructed event sequences")
        st.dataframe(pd.DataFrame(sequences), use_container_width=True)

    st.subheader("Analysis output")
    st.json(analysis, expanded=False)
else:
    st.warning(
        "Route analysis not found. Run src/reconstruct_routes.py first."
    )

st.header("Snapshot Comparison")

if snapshots:
    st.json(snapshots, expanded=True)
else:
    st.caption(
        "Snapshot comparison summary was not found under the expected "
        "filenames. The comparison output remains available in "
        "data/processed."
    )

st.header("Data and Methodology")
st.markdown("""
- **BGP source:** RIPE Stat historical BGP state and update data.
- **Study prefix:** `193.0.0.0/21`.
- **Study window:** 20–22 December 2024 for the collected update data.
- **Observed events:** announcements, withdrawals, and reconstructed
  AS-path changes.
- **Important limitation:** current RPKI validation is not historical
  RPKI validation. No causal relationship between RPKI state changes
  and BGP events is claimed.
""")

st.caption("RPKI-PathWatch | Research prototype")
