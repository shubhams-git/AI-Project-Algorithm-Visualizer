import sys
from Starter import Starter


if __name__ == "__main__":
    """
    This is the Main script the runs the program
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test.txt"  

    agent = Starter(filename)
    
    # Execute a specific algorithm if provided as a second command line argument
    if len(sys.argv) > 2:
        algorithm = sys.argv[2]
        print(agent.execute_search(algorithm))
