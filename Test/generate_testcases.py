import os
import sys
import random

# Add parent directory to path so we can import search
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from search import search

def generate_random_config():
    tiles = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    positions = list(range(9))
    random.shuffle(positions)
    
    # 8 tiles get the first 8 positions
    tile_positions = positions[:8]
    empty_pos = positions[8]
    
    parts = []
    for tile, pos in zip(tiles, tile_positions):
        rot = random.randint(0, 3)
        parts.append((pos, f"{pos}{tile}{rot}"))
        
    # Sort parts by position
    parts.sort(key=lambda x: x[0])
    
    # Choose player position from the tile positions
    player_pos = random.choice(tile_positions)
    
    config_str = " ".join([x[1] for x in parts]) + f" {player_pos}"
    return config_str

def main():
    print("Generating solvable Temple Trap configurations...")
    random.seed(42)  # For reproducibility
    
    categories = {
        'Easy (cost <= 15)': [],
        'Medium (15 < cost <= 30)': [],
        'Hard (cost > 30)': []
    }
    
    attempts = 0
    needed_per_category = 2
    
    while any(len(lst) < needed_per_category for lst in categories.values()) and attempts < 2000:
        attempts += 1
        config = generate_random_config()
        # Use A* search to check solvability quickly
        solution, path_cost = search(config, algorithm='astar')
        
        if solution is not None:
            if path_cost <= 15:
                cat = 'Easy (cost <= 15)'
            elif path_cost <= 30:
                cat = 'Medium (15 < cost <= 30)'
            else:
                cat = 'Hard (cost > 30)'
                
            if len(categories[cat]) < needed_per_category:
                categories[cat].append((config, path_cost))
                print(f"Found {cat} test case: '{config}' with path cost {path_cost} (attempt {attempts})")
                
    # Save the test cases to a file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_testcases.txt')
    with open(output_path, 'w') as f:
        f.write("# Generated Temple Trap Solvable Test Cases\n\n")
        for cat, cases in categories.items():
            f.write(f"## {cat}\n")
            for config, cost in cases:
                f.write(f"{config} # cost = {cost}\n")
            f.write("\n")
            
    print(f"\nSaved generated test cases to {output_path}")

if __name__ == '__main__':
    main()
