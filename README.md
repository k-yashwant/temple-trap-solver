#  Temple Trap Solver

An optimal pathfinding solver and interactive GUI visualizer for the **SmartGames Temple Trap** sliding puzzle. The project models the puzzle as a state-space search problem and compares **Uniform Cost Search (UCS)** against **A\* Search** guided by an admissible **Manhattan Distance** heuristic.

---

##  Features

*   **Optimal Solver**: Uses Uniform Cost Search (UCS) and A* Search to find the mathematically shortest sequence of moves to solve any solvable puzzle configuration.
*   **Admissible & Consistent Heuristic**: Employs the player's grid Manhattan distance to position 0 to guide A* Search, reducing search time and explored nodes by up to **58%**.
*   **Custom Heap Architecture**: Implements a custom Min-Heap in Python with $O(\log N)$ decrease-key operations using index tracking, overcoming the limitations of Python's standard `heapq` module.
*   **Interactive GUI**: Built using **Tkinter** and **Pillow** to allow users to input initial configurations and visually play through the step-by-step optimal solution.
*   **Validation & Benchmarking**: Includes automated testcase validation and performance profiling scripts that export results directly to CSV.

---

##  Project Structure

```text
.
├── Tiles/                      # Image assets for the puzzle pieces and adventurer
├── Test/
│   ├── testcases.txt           # Input booklet challenges to benchmark
│   ├── benchmark.py            # Compares UCS and A* performance
│   └── validate_testcases.py   # Verifies configuration syntax and solvability
├── TempleTrapGame.py           # GUI entrypoint
├── search.py                   # Core search algorithms (UCS & A*)
├── priority_queue.py           # Custom Min-Heap with index-tracking
├── state_node.py               # Game state representation
├── generate_actions.py         # State transition logic
├── tiles.py                    # Puzzle tile definitions
└── solution.py                 # Solution tracking and goal test
```

---

##  Benchmark Results

Here is a comparison of search space exploration between **UCS** and **A\* (Manhattan)** across official booklet challenges:

| Test Case | Challenge & Level | Optimal Cost | UCS Nodes Expanded | A\* Nodes Expanded | Search Space Reduction |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | Challenge 1 (Starter) | 11 | 584 | 241 | **58.7%** |
| **2** | Challenge 4 (Starter) | 10 | 302 | 231 | **23.5%** |
| **3** | Challenge 28 (Junior) | 12 | 717 | 520 | **27.5%** |
| **4** | Challenge 57 (Master) | 15 | 2,206 | 1,462 | **33.7%** |
| **5** | Challenge 60 (Wizard) | 13 | 1,392 | 903 | **35.1%** |
| **8** | Challenge 22 (Expert) | 22 | 22,748 | 9,678 | **57.5%** |
| **10** | Challenge 27 (Master) | 27 | 47,944 | 34,537 | **28.0%** |
| **11** | Challenge 48 (Master) | 48 | 48,745 | 36,581 | **25.0%** |

*Detailed execution times and peak memory footprints are logged automatically to `Test/benchmark_results.csv` after running the benchmark.*

---

##  Setup & Installation

Ensure you have Python 3 and the required libraries installed:

```bash
pip install pillow tk numpy
```

---

##  Usage

Run the scripts from the repository root directory:

### 1. Launch the Visualizer GUI
```bash
python3 TempleTrapGame.py
```
*Enter the initial configuration in the prompt window (e.g. `0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8`), press Enter, and use the GUI controls to play, pause, or step through the optimal solution.*

### 2. Validate Your Custom Test Cases
Write your booklet configurations in `Test/testcases.txt` and validate them for syntactic correctness and solvability:
```bash
python3 Test/validate_testcases.py
```

### 3. Run the Performance Benchmark
Compare search speeds, frontier sizes, and node expansions between A* and UCS:
```bash
python3 Test/benchmark.py
```

---

##  Configuration String Format
Configurations are written as a whitespace-separated sequence of 8 tiles followed by the player's initial position:

`[position][tile_letter][rotation] x 8` + `[player_position]`

*   **Grid Positions**:
    ```text
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    ```
*   **Tile Types**: Letters `A` to `H`.
*   **Rotation**: `0` to `3` (representing number of 90-degree clockwise rotations).
*   **Example**: `0D1 1B2 2C1 3G0 4F2 5A3 6H3 7E3 0` (adventurer starts at position `0`).

---

##  Credits
*   **Author**: Kotikala Yashwant (Roll No: 24AI10034)
| **11** | Challenge 48 (Master) | 48 | 48,745 | 36,581 | **25.0%** |

*Detailed execution times and peak memory footprints are logged automatically to `Test/benchmark_results.csv` after running the benchmark.*

---

## 🛠️ Setup & Installation

Ensure you have Python 3 and the required libraries installed:

```bash
pip install pillow tk numpy
```

---

## 💻 Usage

Run the scripts from the repository root directory:

### 1. Launch the Visualizer GUI
```bash
python3 TempleTrapGame.py
```
*Enter the initial configuration in the prompt window (e.g. `0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8`), press Enter, and use the GUI controls to play, pause, or step through the optimal solution.*

### 2. Validate Your Custom Test Cases
Write your booklet configurations in `Test/testcases.txt` and validate them for syntactic correctness and solvability:
```bash
python3 Test/validate_testcases.py
```

### 3. Run the Performance Benchmark
Compare search speeds, frontier sizes, and node expansions between A* and UCS:
```bash
python3 Test/benchmark.py
```

---

## 📝 Configuration String Format
Configurations are written as a whitespace-separated sequence of 8 tiles followed by the player's initial position:

`[position][tile_letter][rotation] x 8` + `[player_position]`

*   **Grid Positions**:
    ```text
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    ```
*   **Tile Types**: Letters `A` to `H`.
*   **Rotation**: `0` to `3` (representing number of 90-degree clockwise rotations).
*   **Example**: `0D1 1B2 2C1 3G0 4F2 5A3 6H3 7E3 0` (adventurer starts at position `0`).

---

## 👤 Credits
*   **Author**: Kotikala Yashwant (Roll No: 24AI10034)
