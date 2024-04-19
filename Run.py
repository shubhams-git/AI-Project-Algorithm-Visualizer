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

    # Replace the loop and input handling to allow command-line invocation
    if len(sys.argv) > 2:
        algorithm = sys.argv[2]
        print(agent.execute_search(algorithm))
