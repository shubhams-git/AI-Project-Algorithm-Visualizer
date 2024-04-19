import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import re


# Constants for the directory paths and file names
TESTS_DIR = "tests"
RESULTS_FILE = "test_results.json"
SUMMARY_FILE = "summary_report.txt"

def generate_test_cases():
    # This function generates a list of test case dictionaries based on the scenarios.
    return [
        # Simple straight path
        {
            'id': 1,
            'grid_size': [3, 3],
            'start': (0, 0),
            'goals': [(2, 2)],
            'walls': []
        },
        # Single obstacle
        {
            'id': 2,
            'grid_size': [3, 3],
            'start': (0, 0),
            'goals': [(2, 2)],
            'walls': [(1, 1, 1, 1)]
        },
        # Multiple obstacles
        {
            'id': 3,
            'grid_size': [5, 5],
            'start': (0, 0),
            'goals': [(4, 4)],
            'walls': [(0, 1, 5, 1), (2, 2, 1, 3)]
        },
        # Corner goal
        {
            'id': 4,
            'grid_size': [3, 3],
            'start': (1, 1),
            'goals': [(0, 0)],
            'walls': []
        },
        # Edge goal
        {
            'id': 5,
            'grid_size': [3, 3],
            'start': (1, 1),
            'goals': [(0, 1)],
            'walls': []
        },
        # Central goal
        {
            'id': 6,
            'grid_size': [3, 3],
            'start': (0, 0),
            'goals': [(1, 1)],
            'walls': []
        },
        # Dead ends
        {
            'id': 7,
            'grid_size': [3, 3],
            'start': (0, 0),
            'goals': [(2, 2)],
            'walls': [(1, 0, 1, 2), (0, 1, 2, 1)]
        },
        # Multiple goals
        {
            'id': 8,
            'grid_size': [3, 3],
            'start': (0, 0),
            'goals': [(2, 0), (0, 2)],
            'walls': []
        },
        # Large grid
        {
            'id': 9,
            'grid_size': [10, 10],
            'start': (0, 0),
            'goals': [(9, 9)],
            'walls': []
        },
        # Path with minimum turns
        {
            'id': 10,
            'grid_size': [5, 5],
            'start': (0, 0),
            'goals': [(4, 4)],
            'walls': [(0, 1, 1, 4), (1, 3, 3, 1), (3, 1, 1, 2)]
        },
        # Unreachable goal
        {
            'id': 11,
            'grid_size': [3, 3],
            'start': (0, 0),
            'goals': [(1, 1)],
            'walls': [(0, 1, 1, 2), (1, 0, 2, 1), (1, 2, 2, 1), (2, 1, 1, 2)]
        },
        # Complex maze
        {
            'id': 12,
            'grid_size': [5, 5],
            'start': (0, 0),
            'goals': [(4, 4)],
            'walls': [(0, 1, 1, 1), (1, 1, 1, 1), (1, 3, 3, 1), (3, 1, 1, 2), (2, 2, 1, 1)]
        },
    ]


def create_test_file(test_case, test_id):
    # Given a test_case dictionary and a test_id, this function creates a test file in the TESTS_DIR.
    test_file_name = os.path.join(TESTS_DIR, f"test_{test_id}.txt")
    with open(test_file_name, 'w') as file:
        file.write(f"[{test_case['grid_size'][0]},{test_case['grid_size'][1]}]\n")
        file.write(f"({test_case['start'][0]},{test_case['start'][1]})\n")
        file.write(' | '.join(f"({g[0]},{g[1]})" for g in test_case['goals']) + '\n')
        for wall in test_case['walls']:
            file.write(f"({wall[0]},{wall[1]},{wall[2]},{wall[3]})\n")
    return test_file_name

def run_search_algorithm(test_file, algorithm):
    # Runs a search algorithm on a test file and returns the results.
    command = ['python', 'Run.py', test_file, algorithm]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def collect_results(test_cases, algorithms):
    # This function runs each algorithm on each test case and collects the results.
    results = {}
    for test_case in test_cases:
        test_file = create_test_file(test_case, test_case['id'])
        results[test_case['id']] = {}
        for algorithm in algorithms:
            output = run_search_algorithm(test_file, algorithm)
            results[test_case['id']][algorithm] = parse_output(output)
    return results

def parse_output(output):
    result = {"goal_reached": False, "nodes_created": 0, "path": [], "goal_node": None}
    if "No goal is reachable" in output:
        match = re.search(r"No goal is reachable; (\d+)", output)
        if match:
            result.update({"nodes_created": int(match.group(1))})
    else:
        match = re.search(r"<Node \((\d+, \d+)\)> (\d+)\n\[(.*)\]", output, re.DOTALL)
        if match:
            goal_node = tuple(map(int, match.group(1).split(", ")))
            nodes_created = int(match.group(2))
            path = match.group(3).replace("'", "").split(", ")
            result.update({"goal_reached": True, "goal_node": goal_node, "nodes_created": nodes_created, "path": path})
    return result

def save_results(results):
    # Saves the collected results to a JSON file in the TESTS_DIR.
    with open(os.path.join(TESTS_DIR, RESULTS_FILE), 'w') as f:
        json.dump(results, f, indent=4)

def generate_summary_report(results):
    # Generates a summary report from the results and saves it as a text file.
    summary = ""
    for test_id, test_results in results.items():
        summary += f"Test Case ID: {test_id}\n"
        for algorithm, result in test_results.items():
            if result is not None and result['goal_reached']:
                summary += f"{algorithm}: Goal Node - {result['goal_node']}, Path - {result['path']}, Nodes Created - {result['nodes_created']}\n"
            elif result is not None:
                summary += f"{algorithm}: No goal is reachable; Nodes Created - {result['nodes_created']}\n"
            else:
                summary += f"{algorithm}: No output received or output was not parseable\n"
        summary += "\n"
    with open(os.path.join(TESTS_DIR, SUMMARY_FILE), 'w') as f:
        f.write(summary)

def main():
    # Ensure the tests directory exists
    Path(TESTS_DIR).mkdir(exist_ok=True)
    
    # Generate test cases
    test_cases = generate_test_cases()
    
    # Define the algorithms to test
    algorithms = ["BFS", "DFS", "GBFS", "AS", "CUS1", "CUS2"]
    
    # Collect results from running the test cases
    results = collect_results(test_cases, algorithms)
    
    # Save the results to a file
    save_results(results)
    
    # Generate a summary report
    generate_summary_report(results)

if __name__ == "__main__":
    main()
