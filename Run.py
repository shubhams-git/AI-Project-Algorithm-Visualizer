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
    print("1 - BFS")
    print("2 - DFS")
    print("3 - GBFS")
    print("4 - AStar")
    print("5 - Uniform Cost")
    print("6 - Custom Search 1: Iterative Deepening Depth-First Search")
    print("7 - Custom Search 2: Bidirectional Search")
    print("8 - exit")

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
        elif response == "US":
            print(agent.uniform_search())
        elif response == "CUS1":
            print(agent.CUS1())
        elif response == "CUS2":
            print(agent.CUS2())
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
