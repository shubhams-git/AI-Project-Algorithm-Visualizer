from Starter import Starter


    

# Main script
if __name__ == "__main__":
    agent = Starter("test.txt")
    print("1 - BFS")
    print("2 - DFS")
    print("3 - GBFS")
    print("4 - AStar")
    print("5 - Uniform Cost")
    print("6 - Custom Seach 1: Iterative Deepening Depth-First Search")
    print("7 - Custom Seach 2: Bidirectional Search")
    print("8 - exit")

    while True:
        response = input()
        if response == "1":
            agent.bfs_search()
        elif response == "2":
            agent.dfs_search()
        elif response == "3":
            agent.gbfs_search()
        elif response == "4":
            agent.a_star_search()
        elif response == "5":
            agent.uniform_search()
        elif response == "6":
            agent.CUS1()
        elif response == "7":
            agent.CUS2()
        elif response == "8":
            break
        else:
            print("Please enter a valid response")
