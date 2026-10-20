# AI Smart Traffic Management System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Day%204%20Completed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

An intelligent, vision-based traffic management and signal control simulation designed to analyze traffic density, detect vehicles and pedestrians, and adaptively optimize intersection signal timings.

---

## 📌 Project Overview
Urban traffic congestion leads to wasted fuel, higher emissions, and extended emergency vehicle response times. Standard fixed-time traffic lights cannot adapt to dynamic changes in traffic flow. 

This project explores an end-to-end computer vision and software pipeline that:
- Inspects intersection video feeds.
- Classifies and tracks vehicles and pedestrians.
- Computes real-time traffic density per lane.
- Simulates an adaptive signal controller adjusting green light durations based on live demand.

For detailed problem definition and safety scope, see [Project Goals](docs/project-goals.md).

---

## 🎯 Objectives
- **Vehicle Detection & Counting**: Detect cars, buses, trucks, motorcycles, and emergency vehicles.
- **Traffic Density & Queue Analysis**: Measure spatial occupancy and waiting times across intersection approaches.
- **Turning Pattern & Flow Analysis**: Track vehicle trajectories through intersections.
- **Pedestrian Detection & Safety**: Monitor crosswalks to prioritize safe crossing intervals.
- **Adaptive Signal Control Simulation**: Implement dynamic green-split algorithms to minimize congestion.

---

## 🛠️ Planned Technology Stack
- **Language**: Python 3.10+ (Current environment: Python 3.13)
- **Computer Vision & Processing**: OpenCV, NumPy
- **Deep Learning / Object Detection (Upcoming)**: YOLO / PyTorch
- **Tracking (Upcoming)**: ByteTrack / DeepSORT / Centroid Tracking
- **Visualization / Interface (Upcoming)**: Matplotlib / Streamlit / OpenCV GUI
- **Version Control & Documentation**: Git, GitHub, Markdown

---

## 🗺️ Development Roadmap
- [x] **Day 1**: Project initialization, environment verification, Git/GitHub setup, and documentation structure.
- [x] **Day 2**: Python fundamentals review, data structures, and initial traffic domain modeling (intersections, lanes, signals).
- [x] **Day 3**: Python control flow, loops, and deterministic traffic-demand selection logic.
- [x] **Day 4**: Dynamic traffic queue simulation, vehicle arrivals/departures, and delay tracking.
- [ ] **Day 5**: Video ingestion pipeline, frame extraction, and region-of-interest (ROI) configuration.
- [ ] **Day 6**: Background subtraction & classic computer vision vehicle counting basics.
- [ ] **Day 7**: Deep learning object detection integration (vehicle & pedestrian detection).
- [ ] **Day 8**: Multi-object tracking and lane-based counting logic.
- [ ] **Day 9**: Adaptive signal timing algorithm and simulation dashboard.

---

## 📁 Project Structure
```text
ai-smart-traffic-management/
├── .gitignore                    # Excludes .venv, cache, secrets, and large media
├── README.md                     # Project documentation and roadmap
├── requirements.txt              # Initial project dependencies
├── main.py                       # Primary application entry point
├── docs/                         # Architectural and development documentation
│   ├── project-goals.md          # Problem statement, solution architecture, safety scope
│   └── development-log.md        # Daily development progress log
├── src/                          # Source package for core modules
│   ├── __init__.py               # Package initialization
│   ├── traffic_data.py           # Traffic counts and demand classification
│   └── traffic_simulation.py     # Dynamic queue simulation & delay tracking
└── tests/                        # Automated test suite
    ├── __init__.py               # Tests package initialization
    ├── test_traffic_data.py      # Unit tests for traffic data calculations
    └── test_traffic_simulation.py# Unit tests for dynamic queue simulation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Git installed on your system

### 2. Clone the Repository
```bash
git clone https://github.com/Upadhya82/ai-smart-traffic-management.git
cd ai-smart-traffic-management
```

### 3. Activate the Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 4. Run the Entry Point
```bash
python main.py
```

---

## 📝 Current Status
- **Current Milestone**: **Day 1 Completed**
- Project foundation initialized, Git branch synchronized with GitHub, and modular package structure prepared.
