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

---

## Day 3: Control Flow, Traffic Analysis & Signal Demand Selection
- **Date**: October 18, 2026
- **Status**: Completed

### 1. Work Completed
- **Traffic Demand Selection Logic (`src/traffic_data.py`)**:
  - Implemented `select_highest_demand_approach(counts, priority_order)`.
  - Formulated a deterministic tie-breaking policy prioritizing directional order (`North` > `South` > `East` > `West`).
  - Added robust validation to reject negative values with descriptive `ValueError` exceptions.
  - Handled edge cases: empty dictionaries return `None`, all-zero intersection demand returns `None`.
  - Enhanced `generate_traffic_summary(counts)` to flag recommended green approaches directly in the summary table.
- **Demonstration & Architectural Education (`main.py`)**:
  - Demonstrated sequential `if / elif / else` conditional blocks.
  - Demonstrated iterating over dictionary key-value pairs using `for` loops.
  - Walked through clear leader scenarios vs. tied scenarios.
  - Documented why single-frame vehicle count alone is insufficient for real-world signal control (starvation, delay accumulation, safety intervals, clearance times, emergency preemption).
- **Automated Unit Testing Expansion (`tests/test_traffic_data.py`)**:
  - Expanded test suite from 9 to 16 unit tests.
  - Tested single clear leader, 2-way ties, 4-way ties, custom priority orders, empty dictionaries, all-zero traffic, and negative value error handling.
  - Achieved 100% pass rate across all 16 tests in 0.001s.

### 2. Concepts Learned
- **Conditional Branching (`if`, `elif`, `else`)**:
  - Evaluates expressions sequentially; the first branch evaluating to `True` executes while the rest are skipped.
  - Using comparison operators (`<=`, `==`, `>`) to establish non-overlapping numerical intervals.
- **Loops (`for` Iteration)**:
  - Iterating cleanly across dictionaries using `counts.items()` without index counters.
- **Deterministic Decision Making**:
  - Ensuring automated algorithms avoid non-deterministic behavior (e.g., random coin flips or arbitrary dictionary order) when ties occur.
- **Traffic Engineering vs. Prototype Logic**:
  - Recognizing the gap between greedy instantaneous vehicle-count heuristics and true actuated signal timing (e.g., NEMA phase dual-ring controllers, min/max green times, coordination, pedestrian walk intervals).

### 3. Challenges & Resolutions
- **Issue**: How to treat intersections where all approaches report zero vehicles.
- **Resolution**: Returning `None` explicitly conveys "no active demand" rather than arbitrarily allocating green to an empty road.
- **Issue**: Preventing tie-breaking from relying on Python dictionary ordering across different platforms.
- **Resolution**: Created `DEFAULT_APPROACH_PRIORITY` tuple and explicitly scanned candidate approaches in declared priority order.

### 4. Next Steps (Day 4)
- Advance from static snapshot counts to multi-step dynamic simulation over time (discrete time steps / ticks).
- Implement vehicle arrival and departure queues using Python collections (lists and queues).
- Track waiting times per vehicle to implement anti-starvation logic.

---

## Day 4: Dynamic Traffic Queue Simulation & Delay Tracking
- **Date**: October 21, 2026
- **Status**: Completed

### 1. Work Completed
- **Traffic Simulation Module (`src/traffic_simulation.py`)**:
  - Built discrete-time queue simulation for a 4-way intersection (`North`, `South`, `East`, `West`).
  - Implemented `create_initial_queues()` with input validation and defensive copying.
  - Implemented `simulate_step()` executing arrivals, green-phase departures (bounded by departure rate and current queue size), and non-negative queue bounds.
  - Implemented `run_simulation()` coordinating multi-step runs with support for both caller-specified green schedules and automatic adaptive demand selection (`select_highest_demand_approach`).
  - Implemented queue-based waiting time tracking calculating per-step delay and cumulative intersection delay.
  - Implemented `generate_simulation_summary()` and `print_simulation_summary()` rendering readable ASCII progress tables.
- **Application Integration (`main.py`)**:
  - Preserved Day 1–3 demonstrations and added Section 3 demonstrating a 4-step simulation with dynamic arrivals and adaptive signal selection.
- **Automated Testing Suite (`tests/test_traffic_simulation.py`)**:
  - Authored 13 dedicated unit tests covering:
    1. Default empty initial queues.
    2. Correct arrival distribution per approach.
    3. Departure restriction strictly to the green approach.
    4. Departures never exceeding waiting queue.
    5. Non-negative queue invariants under high departure rates.
    6. Empty queue handling during green phases.
    7. Multi-step deterministic progression.
    8. Cumulative waiting-time tracking verification.
    9. Rejection of negative queues, negative rates, and non-integer types (including bools).
    10. Rejection of invalid approach names.
    11. Verification that caller input data is never mutated.
    12. Zero-step simulation behavior.
    13. Integration with Day 3 adaptive demand selection.
  - Full test suite now contains 29 tests passing with 100% success rate.

### 2. Concepts Learned & Waiting-Time Calculation
- **Discrete-Time Simulation (Ticks)**:
  - Modeling time as sequential discrete steps ($t_1, t_2, \dots, t_N$) where state changes occur synchronously in phases (Arrivals $\rightarrow$ Selection $\rightarrow$ Departure $\rightarrow$ Metrics).
- **Waiting-Time Rule & Calculation**:
  - At the end of each simulation step, any vehicle remaining in queue has experienced 1 time step of delay.
  - Step Delay = $\sum (\text{Remaining vehicles on all approaches at end of step})$.
  - Cumulative Delay = $\sum_{t=1}^{N} (\text{Step Delay}_t)$.
- **Simulation Limitations**:
  - Aggregated queue vs. individual vehicle tracking: We approximate delay by queue occupancy rather than stamping arrival times on individual vehicle objects.
  - Uniform departure rate: Real vehicles incur start-up lost time (reaction latency) and variable turning speeds.
  - Discrete batching: Real traffic flows continuously rather than in synchronized discrete pulses.
- **Defensive Immutability in Python**:
  - Using dictionary copies (`dict.copy()` and dictionary comprehensions) to ensure that running a simulation does not unexpectedly modify caller dictionaries.

### 3. Challenges & Resolutions
- **Issue**: In Python, `isinstance(True, int)` evaluates to `True` because `bool` is a subclass of `int`.
- **Resolution**: Explicitly checked `not isinstance(x, bool)` during input validation to prevent boolean values from being accepted as numeric vehicle counts.
- **Issue**: Ensuring clean integration between Day 3's instantaneous demand selection and Day 4's multi-step queues.
- **Resolution**: Allowed `run_simulation()` to look ahead at updated queues (queue + arrivals) to dynamically select the highest-demand green approach when no fixed schedule is provided.

### 4. Next Steps (Day 5)
- Video ingestion pipeline: OpenCV basics (`cv2.VideoCapture`), frame extraction, and video metadata inspection.
- Region of Interest (ROI) specification: Defining lane boundaries and bounding boxes over camera coordinates.
