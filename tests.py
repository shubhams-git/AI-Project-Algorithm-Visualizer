import subprocess

def create_test_file(grid_size, start, goals, walls, file_name):
    with open(file_name, 'w') as file:
        # Write grid size
        file.write(f"[{grid_size[0]},{grid_size[1]}]\n")
        # Write start position
        file.write(f"({start[0]},{start[1]})\n")
        # Write goals
        goals_str = ' | '.join(f"({g[0]},{g[1]})" for g in goals)
        file.write(f"{goals_str}\n")
        # Write walls
        for wall in walls:
            file.write(f"({wall[0]},{wall[1]},{wall[2]},{wall[3]})\n")

def run_test(file_name, method):
    result = subprocess.run(['python', 'Run.py', file_name, str(method)], capture_output=True, text=True)
    return result.stdout

def main():
    # Define test cases
    test_cases = [
        # Empty Grid
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(4, 4)], "walls": []},
        # Single Wall Blocking Path
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(4, 4)], "walls": [(2, 0, 1, 5)]},
        # Multiple Goals (Agent Closer to One)
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(4, 4), (1, 1)], "walls": []},
        # Complex Wall Structures
        {"grid_size": (10, 10), "start": (0, 0), "goals": [(9, 9)], "walls": [(1, 1, 1, 8), (2, 8, 8, 1), (8, 1, 1, 7)]},
        # No Possible Path
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(4, 4)], "walls": [(0, 1, 5, 1)]},
        # Agent Starts at Goal
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(0, 0)], "walls": []},
        # Large Grid with Distant Goals
        {"grid_size": (20, 20), "start": (0, 0), "goals": [(19, 19)], "walls": []},
        # High Density of Walls
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(4, 4)], "walls": [(0, 1, 1, 3), (1, 3, 3, 1), (3, 0, 1, 3)]},
        # Randomly Generated Grids
        {"grid_size": (10, 10), "start": (0, 0), "goals": [(9, 9)], "walls": [(i, j, 1, 1) for i in range(1, 9, 2) for j in range(1, 9, 2)]},
        # Edge of Grid Start and Goal
        {"grid_size": (5, 5), "start": (0, 0), "goals": [(4, 4)], "walls": []},
        # Path with Equal Options
        {"grid_size": (5, 5), "start": (2, 2), "goals": [(2, 4)], "walls": []}
    ]
    
    methods = ["BFS", "DFS", "GBFS", "AS", "US", "CUS1", "CUS2"]  # Corresponding to BFS, DFS, etc.
    for case_id, case in enumerate(test_cases):
        file_name = f"test_{case_id}.txt"
        create_test_file(case['grid_size'], case['start'], case['goals'], case['walls'], file_name)
        
        for method in methods:
            print(f"Running {method} on test case {case_id}")
            output = run_test(file_name, method)
            print(f"Output for method {method}:\n{output}")

if __name__ == "__main__":
    main()
