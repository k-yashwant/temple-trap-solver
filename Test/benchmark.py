import os
import sys
import time

# Add parent directory to path so we can import search and search_stats
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from search import search, search_stats

def run_benchmark():
    # We will load all test cases from testcases.txt in the same directory.
    # If testcases.txt does not exist, we fall back to the default sample cases.
    cases = []
    
    # Path to testcases.txt
    testcases_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcases.txt')
    
    # --- Format of testcases.txt ---
    # - Lines starting with '#' are treated as comments and ignored.
    # - Lines starting with '##' define the active level/difficulty (e.g., '## Starter', '## Junior').
    # - Non-empty lines contain the configuration string. Any comments on the same line starting with '#' are stripped.
    #
    # Example format:
    # ## Starter
    # 0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8 # Challenge 1
    # ## Junior
    # 0B1 1D0 2F2 3A0 4E0 5G2 6H0 7C1 5 # Challenge 28
    
    if os.path.exists(testcases_path):
        print(f"Loading test cases from {testcases_path}...")
        try:
            with open(testcases_path, 'r') as f:
                current_level = "Default"
                for line in f:
                    line = line.strip()
                    if line.startswith("##"):
                        current_level = line[2:].strip()
                    elif line and not line.startswith("#"):
                        # Extract configuration before any inline comments
                        config = line.split("#")[0].strip()
                        if config:
                            cases.append((config, current_level))
        except Exception as e:
            print(f"Error reading testcases.txt: {e}")
            
    if not cases:
        print("testcases.txt not found or empty. Falling back to default booklet samples...")
        cases = [
            ("0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8", "Starter (Challenge 1)"),
            ("0B1 1D0 2H2 3E1 4G0 5F3 7A0 8C0 3", "Starter (Challenge 4)"),
            ("0B1 1D0 2F2 3A0 4E0 5G2 6H0 7C1 5", "Junior (Challenge 28)"),
            ("0B2 1C0 3F1 4E0 5A0 6G1 7H0 8D3 4", "Master (Challenge 57)"),
            ("0F2 1A1 3H2 4B3 5E0 6D2 7C1 8G3 5", "Wizard (Challenge 60)"),
        ]
            
    print(f"Starting benchmark on {len(cases)} test cases...\n")
    
    results = []
    
    for i, (config, label) in enumerate(cases):
        print(f"Running Test Case {i+1} ({label}): '{config}'")
        
        # --- Run UCS ---
        t0 = time.time()
        sol_ucs, cost_ucs = search(config, algorithm='ucs')
        t1 = time.time()
        time_ucs = (t1 - t0) * 1000 # in ms
        exp_ucs = search_stats['nodes_expanded']
        front_ucs = search_stats['max_frontier_size']
        
        # --- Run A* ---
        t0 = time.time()
        sol_astar, cost_astar = search(config, algorithm='astar')
        t1 = time.time()
        time_astar = (t1 - t0) * 1000 # in ms
        exp_astar = search_stats['nodes_expanded']
        front_astar = search_stats['max_frontier_size']
        
        # Validation
        if cost_ucs != cost_astar:
            print(f"  WARNING: Path cost mismatch! UCS: {cost_ucs}, A*: {cost_astar}")
            
        results.append({
            'index': i + 1,
            'label': label,
            'cost': cost_ucs,
            'ucs': {'time': time_ucs, 'expanded': exp_ucs, 'frontier': front_ucs},
            'astar': {'time': time_astar, 'expanded': exp_astar, 'frontier': front_astar}
        })
        print(f"  UCS: Cost={cost_ucs}, Expanded={exp_ucs}, MaxFrontier={front_ucs}, Time={time_ucs:.1f}ms")
        print(f"  A* : Cost={cost_astar}, Expanded={exp_astar}, MaxFrontier={front_astar}, Time={time_astar:.1f}ms")
        print("-" * 60)
        
    # Print the markdown table
    print("\n### Benchmark Results Table\n")
    print("| Test Case | Category / Level | Optimal Cost | Algorithm | Nodes Expanded | Max Frontier Size | Execution Time (ms) |")
    print("|---|---|---|---|---|---|---|")
    for r in results:
        idx = r['index']
        lbl = r['label']
        cost = r['cost']
        
        # UCS Row
        print(f"| {idx} | {lbl} | {cost} | UCS | {r['ucs']['expanded']} | {r['ucs']['frontier']} | {r['ucs']['time']:.1f} ms |")
        # A* Row
        print(f"| | | | A* (Manhattan) | {r['astar']['expanded']} | {r['astar']['frontier']} | {r['astar']['time']:.1f} ms |")
        print("| | | | | | | |") # spacer
        
    print("\nBenchmark completed.")

if __name__ == '__main__':
    run_benchmark()
