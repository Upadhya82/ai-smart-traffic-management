# Development Log

## Day 1: Project Setup, Environment Verification & Git Foundations
- **Date**: October 16, 2026
- **Status**: Completed

### 1. Work Completed
- **Environment Verification**:
  - Verified Python 3.13 virtual environment (`.venv`) is operational.
  - Verified Git version control integration and established branch tracking with `origin/main`.
- **Project Structure Scaffolding**:
  - Organized directory hierarchy: `src/` for source code, `docs/` for project documentation, `.venv/` for isolated packages.
  - Initialized `src/__init__.py` to define `src` as a modular Python package.
  - Created root entry point `main.py` with system status and environment sanity check.
  - Generated `requirements.txt` containing planned initial dependencies (`numpy`, `opencv-python`).
- **Repository Security & Cleanliness**:
  - Configured comprehensive `.gitignore` preventing `.venv/`, compiled bytecode, secret keys, temporary files, large media/videos, and AI model checkpoints from entering version control.
  - Removed accidental misplaced files to maintain a clean project root.
- **Documentation**:
  - Authored `docs/project-goals.md` detailing problem definition, system architecture, and safety scope.
  - Authored comprehensive `README.md` with system overview, planned features, and setup instructions.

### 2. Concepts Learned
- **Virtual Environments (`.venv`)**:
  - Why isolating dependencies per-project prevents package conflicts and keeps system Python clean.
  - Why the virtual environment directory itself must never be checked into Git.
- **Git vs. GitHub**:
  - **Git**: Local version control software running on your computer to track code history via snapshots (commits).
  - **GitHub**: Remote cloud platform hosting Git repositories for collaboration, backup, and code sharing.
- **Git Lifecycle**:
  - **Working Directory**: The actual files on disk being edited.
  - **Staging Area (`git add`)**: The preparation area where selected changes are queued before saving.
  - **Commit (`git commit`)**: A permanent, named cryptographic snapshot of staged changes.
  - **Remote Push (`git push`)**: Transmitting local commits to the remote repository on GitHub.
- **Importance of `.gitignore`**:
  - Prevents uploading gigabytes of virtual environment binaries, credentials, or proprietary videos that can break repository performance or leak private information.

### 3. Challenges & Resolutions
- **Issue**: An empty `main.py` was unintentionally located inside `.venv/main.py` instead of the project root.
- **Resolution**: Removed the misplaced file from `.venv/` and established the clean root-level `main.py` entry point.
- **Issue**: Ensuring Git ignore rules accurately covered both video assets and model weights without interfering with standard Python code.
- **Resolution**: Added specific wildcards (`*.mp4`, `*.pt`, `*.onnx`) to `.gitignore`.

### 4. Next Steps (Day 2)
- Introduce Python variables, traffic-related data structures (dictionaries, lists, tuples).
- Model traffic intersection approaches, lane queues, and signal phase states in Python code.
- Write modular functions to simulate vehicle counts and queue updates.

---

## Day 2: Python Fundamentals & Traffic Data Modeling
- **Date**: October 16, 2026
- **Status**: Completed

### 1. Work Completed
- **Traffic Data Module (`src/traffic_data.py`)**:
  - Modeled 4-way intersection approaches (North, South, East, West) using Python dictionaries.
  - Built `calculate_total_vehicles(counts)` to aggregate intersection loads with input validation.
  - Built `classify_traffic_demand(vehicle_count)` using illustrative demo thresholds (0-5: LOW, 6-15: MEDIUM, 16+: HIGH).
  - Built `generate_traffic_summary(counts)` and `print_traffic_summary(counts)` to render formatted reports.
- **Application Entry Point Update (`main.py`)**:
  - Demonstrated core Python primitives (`str`, `int`, `float`, `bool`) using real-world traffic context.
  - Connected `main.py` to `src.traffic_data` functions and executed an end-to-end intersection report.
- **Automated Testing Suite (`tests/test_traffic_data.py`)**:
  - Created 9 comprehensive unit tests using Python's built-in `unittest` framework.
  - Tested edge cases including empty counts, all-zero traffic, negative value validation, and precise classification threshold boundaries (0, 5, 6, 15, 16).
  - Verified 100% test pass rate with zero external package overhead.

### 2. Concepts Learned
- **Python Primitive Types in Real Systems**:
  - `int`: Representing discrete physical counts (e.g., number of vehicles queued).
  - `float`: Continuous physical measurements with decimal precision (e.g., vehicle speed in km/h).
  - `str`: Textual identifiers and labels (e.g., road names, direction labels).
  - `bool`: Binary signal states (e.g., `is_signal_green` is either `True` or `False`).
- **Dictionaries (`dict`)**:
  - Using key-value pairs (`{"North": 4, "South": 12, ...}`) to model multi-lane or multi-approach sensor inputs.
- **Defensive Programming & Validation**:
  - Raising descriptive `ValueError` exceptions when vehicle counts are negative, preventing invalid downstream calculations.
- **Automated Unit Testing with `unittest`**:
  - Structuring test cases with `self.assertEqual` and `self.assertRaises`.
  - Testing boundary conditions (off-by-one errors) to ensure business logic is resilient.
- **Demonstration vs. Production Thresholds**:
  - Understanding that simplified classification thresholds (0-5: LOW, 6-15: MEDIUM, 16+: HIGH) are prototype heuristics rather than validated highway engineering standards.

### 3. Challenges & Resolutions
- **Issue**: Ensuring clean module imports between `main.py` and `src/` without path manipulation.
- **Resolution**: Kept `src` as a standard package with `__init__.py` and executed scripts from the repository root.
- **Issue**: Windows terminal character encoding (`cp1252`) compatibility when printing summaries.
- **Resolution**: Formatted tables using clean ASCII characters (`|`, `-`) ensuring seamless cross-platform display.

### 4. Next Steps (Day 3)
- Explore Python collections in greater depth: Lists of dictionaries, filtering, and sorting traffic data.
- Introduce simulated vehicle queues with arrival/departure rates.
- Model multi-lane approaches and compute weighted queue delays.
