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
