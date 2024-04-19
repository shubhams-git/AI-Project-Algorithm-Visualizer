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
    ]
    
    methods = ["BFS", "DFS", "GBFS", "AS", "CUS1", "CUS2"]  # Corresponding to BFS, DFS, etc.
    for case_id, case in enumerate(test_cases):
        file_name = f"test_{case_id}.txt"
        create_test_file(case['grid_size'], case['start'], case['goals'], case['walls'], file_name)
        
        for method in methods:
            print(f"Running {method} on test case {case_id}")
            output = run_test(file_name, method)
            print(f"Output for method {method}:\n{output}")

if __name__ == "__main__":
    main()
