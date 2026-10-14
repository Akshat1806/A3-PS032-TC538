# RPKI-PathWatch — AIORI Hackathon 3

**Team Code:** `A3-PS032-TC538`  
**Problem Statement:** PS-032 — Path and Reachability Analysis During RPKI State Changes  
**Problem Area:** Internet Measurements  
**Institution:** National Forensic Science University (NFSU), Guwahati Campus  
**Status:** Proposed research prototype — implementation in progress

## Overview

RPKI-PathWatch is a proposed Internet measurement and analysis platform for investigating how Resource Public Key Infrastructure (RPKI) validation-state changes relate to observed Border Gateway Protocol (BGP) routing behaviour.

The project aims to correlate transitions between the RPKI states **Valid, Invalid, and NotFound** with observed AS-path changes, route announcements, withdrawals, and prefix visibility across multiple routing collectors.

An RPKI state change does not automatically imply that a prefix becomes unreachable across the Internet. Outcomes depend on network routing policies, alternative paths, BGP convergence, and measurement coverage. Our approach will distinguish observed correlations from proven causation.

## Objectives

- Identify selected RPKI validation-state transitions.
- Compare BGP observations before and after selected events.
- Analyze AS-path changes, announcements, withdrawals, and prefix visibility.
- Estimate routing stabilization or recovery intervals when the available data supports doing so.
- Visualize event timelines and routing observations through an interactive dashboard.
- Document uncertainty, data limitations, and alternative explanations.

## Proposed Methodology

1. **Data collection:** Obtain routing observations from RIPE RIS and/or RouteViews and suitable RPKI validation-state data from documented sources.
2. **Data normalization:** Process timestamps, prefixes, origin ASes, AS paths, announcements, and withdrawals.
3. **Transition detection:** Identify relevant changes in RPKI validation states.
4. **Event correlation:** Align RPKI transitions with BGP observations using defined before-and-after time windows.
5. **Routing analysis:** Compare observed paths, route events, and prefix visibility across collectors.
6. **Visualization and evaluation:** Display the findings, evaluate selected historical events, and document limitations.

## Proposed Technology Stack

- **Language:** Python
- **Data processing:** Pandas and suitable BGP/MRT parsing libraries
- **Potential data sources:** RIPE RIS, RouteViews, NIST RPKI Monitor, and relevant RIPE NCC resources
- **Dashboard:** Streamlit and Plotly
- **Version control:** Git and GitHub

These are proposed implementation choices; capabilities will be described as implemented only after development and testing.

## Team and Responsibilities

| Team member | Area of responsibility |
|---|---|
| Akshat | System architecture, data processing, event correlation, routing metrics, dashboard integration, and reproducibility. |
| [Teammate's name] | Cybersecurity research, RPKI/BGP security, RFC review, test-scenario design, validation of observations, and documentation. |
| [Faculty mentor's name] | Research guidance, methodology review, technical feedback, and interpretation of findings. |

Replace the placeholders with the correct names before final submission.

## Expected Deliverables

- Final presentation in PDF format.
- Team introduction video explaining the problem, proposed solution, and member responsibilities.
- Source code and setup instructions.
- Architecture and methodology documentation.
- Tests and evaluation of selected historical events.
- Working demo link or reviewable final deliverables.

## Presentation

**Status:** Add the final presentation PDF to this repository.

Suggested path: `presentation/RPKI-PathWatch-AIORI-Hackathon3.pdf`

Once uploaded, link it here:

`[View the presentation](presentation/RPKI-PathWatch-AIORI-Hackathon3.pdf)`

The supplied reference template is available at [Proposed-structure-hackathon.pdf](Proposed-structure-hackathon.pdf).

## Team Introduction Video

**Status:** Add the YouTube link after uploading the recorded introduction video.

**Video:** [Add YouTube video URL here]

Ensure the video is accessible to the evaluators.

## Repository Structure

```text
A3-PS032-TC538/
├── README.md
├── Proposed-structure-hackathon.pdf
├── presentation/
├── docs/
├── src/
├── tests/
└── requirements.txt
```

The folders and dependency file will be populated as development progresses. Document dataset retrieval instructions instead of committing large raw routing dumps. Never commit API keys or credentials.

## Evaluation Plan

For selected historical RPKI transitions, we intend to:

- Compare BGP observations across defined time windows.
- Examine path changes, announcements, withdrawals, and collector visibility.
- Compare observations from multiple available collectors.
- Assess stabilization or recovery where measurable.
- Document missing observations, timestamp limitations, and possible unrelated routing events.
- Avoid inferring global unreachability from a single collector's missing route.
- Distinguish temporal correlation from demonstrated causation.

## References and Resources

- [IETF RFC Editor](https://www.rfc-editor.org/)
- [RIPE RIS](https://ris.ripe.net/)
- [RouteViews](https://www.routeviews.org/)
- [NIST RPKI Monitor](https://rpki-monitor.antd.nist.gov/)
- [RIPE NCC](https://www.ripe.net/)

Specific standards and research publications will be cited in the technical documentation after verification.

---

Prepared for **AIORI Hackathon 3**, Team `A3-PS032-TC538`.
