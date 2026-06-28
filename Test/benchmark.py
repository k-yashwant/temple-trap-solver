import os
import sys
import time

# Add parent directory to path so we can import search and search_stats
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from search import search, search_stats

def run_benchmark():
    # Hardcoded sample cases from sample_states.txt
    cases = [
        ("0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8", "Sample 1 (Easy)"),
        ("0B1 1D0 2H2 3E1 4G0 5F3 7A0 8C0 3", "Sample 2 (Easy)"),
        ("0B1 1D0 2F2 3A0 4E0 5G2 6H0 7C1 5", "Sample 3 (Easy)"),
        ("0B2 1C0 3F1 4E0 5A0 6G1 7H0 8D3 4", "Sample 4 (Medium)"),
        ("0F2 1A1 3H2 4B3 5E0 6D2 7C1 8G3 5", "Sample 5 (Hard)"),
    ]
    
    # Try to load generated test cases if they exist
    gen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_testcases.txt')
    if os.path.exists(gen_path):
        print("Found generated_testcases.txt, loading additional cases...")
        try:
            with open(gen_path, 'r') as f:
                current_cat = ""
                for line in f:
                    line = line.strip()
                    if line.startswith("## "):
                        current_cat = line[3:]
                    elif line and not line.startswith("#"):
                        # line format: "config # cost = X"
                        parts = line.split("#")
                        config = parts[0].strip()
                        if config:
                            cases.append((config, f"Gen: {current_cat}"))
        except Exception as e:
            print(f"Error reading generated test cases: {e}")
            
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
    print("| Test Case | Difficulty | Optimal Cost | Algorithm | Nodes Expanded | Max Frontier Size | Execution Time (ms) |")
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
