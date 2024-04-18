import sys
from Starter import Starter

# Main script
if __name__ == "__main__":
    # Accept filename from the command line arguments
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test.txt"  # Default to "test.txt" if no arguments provided

    agent = Starter(filename)
    print("1 - BFS (Breadth First Search)")
    print("2 - DFS (Depth First Search)")
    print("3 - GBFS (Greedy Best First Search)")
    print("4 - AS (A Star Search)")
    print("5 - CUS1 (Uniform Cost Search)")
    print("6 - CUS2 (Iterative Deepening Depth-First Search)")

    # Replace the loop and input handling to allow command-line invocation
    if len(sys.argv) > 2:
        response = sys.argv[2]
        if response == "BFS":
            print(agent.bfs_search())
        elif response == "DFS":
            print(agent.dfs_search())
        elif response == "GBFS":
            print(agent.gbfs_search())
        elif response == "AS":
            print(agent.a_star_search())
        elif response == "CUS1":
            print(agent.uniform_cost_search())
        elif response == "CUS2":
            print(agent.iddfs_search())
        else:
            print("Invalid method.")
    else:
        # If no method is provided, enter a manual selection loop
        while True:
            response = input("Enter a method number: ")
            if response == "8":
                break
            elif response.isdigit():
                print(agent.run_method(int(response)))
            else:
                print("Please enter a valid response")
