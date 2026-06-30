import os
import sys

# Add parent directory to path so we can import search
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from search import search

def validate_config(line_num, config_str):
    tokens = config_str.strip().split()
    if len(tokens) != 9:
        return False, f"Expected 9 tokens (8 tiles + 1 player position), but got {len(tokens)}"
    
    positions = set()
    tile_types = set()
    
    # Validate the 8 tiles
    for i in range(8):
        token = tokens[i]
        if len(token) != 3:
            return False, f"Tile token {i+1} ('{token}') must be exactly 3 characters long (e.g. '0C0')"
        
        pos_char, type_char, rot_char = token[0], token[1], token[2]
        
        if pos_char not in "012345678":
            return False, f"Tile position '{pos_char}' in '{token}' must be between 0 and 8"
        
        pos = int(pos_char)
        if pos in positions:
            return False, f"Duplicate tile position: position {pos} is occupied by multiple tiles"
        positions.add(pos)
        
        if type_char not in "ABCDEFGH":
            return False, f"Invalid tile type '{type_char}' in '{token}' (must be A-H)"
        
        if type_char in tile_types:
            return False, f"Duplicate tile type '{type_char}': each tile type A-H must appear exactly once"
        tile_types.add(type_char)
        
        if rot_char not in "0123":
            return False, f"Invalid rotation '{rot_char}' in '{token}' (must be 0-3)"
            
    # Validate player position
    player_char = tokens[-1]
    if player_char not in "012345678":
        return False, f"Player position '{player_char}' must be between 0 and 8"
        
    player_pos = int(player_char)
    if player_pos not in positions:
        return False, f"Player position {player_pos} cannot be the empty space (empty space is at position {36 - sum(positions)})"
        
    return True, None

def main():
    testcases_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcases.txt')
    if not os.path.exists(testcases_path):
        print(f"Error: testcases.txt not found at {testcases_path}")
        sys.exit(1)
        
    print(f"Validating test cases from {testcases_path}...\n")
    
    has_errors = False
    
    with open(testcases_path, 'r') as f:
        current_level = "Unknown"
        line_num = 0
        for line in f:
            line_num += 1
            line = line.strip()
            if line.startswith("##"):
                current_level = line[2:].strip()
                print(f"\n--- Level: {current_level} ---")
            elif line and not line.startswith("#"):
                # Extract configuration before any inline comments
                raw_config = line.split("#")[0].strip()
                if not raw_config:
                    continue
                
                # 1. Check syntax
                is_valid_syntax, error_msg = validate_config(line_num, raw_config)
                if not is_valid_syntax:
                    print(f"❌ Line {line_num}: SYNTAX ERROR - {error_msg}")
                    print(f"   String: '{line}'")
                    has_errors = True
                    continue
                
                # 2. Check solvability and get cost
                solution, path_cost = search(raw_config, algorithm='astar')
                if solution is None:
                    print(f"❌ Line {line_num}: SOLVABILITY ERROR - State has no solution path to exit!")
                    print(f"   String: '{line}'")
                    has_errors = True
                else:
                    print(f"✅ Line {line_num}: Valid & Solvable | Optimal Cost: {path_cost} steps")
                    
    print("\n" + "="*50)
    if has_errors:
        print("❌ Validation FAILED! Please fix the errors listed above.")
    else:
        print("🎉 Validation SUCCESSFUL! All test cases are syntactically valid and solvable.")
    print("="*50)

if __name__ == '__main__':
    main()
