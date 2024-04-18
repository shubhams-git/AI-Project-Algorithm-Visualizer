from Agent import Agent
from FileReader import FileReader
import json


class Starter:
    def __init__(self, textfile):
        self.reader = FileReader(textfile)
        self.reader.read()
        gridsize = self.reader.get_grid()
        agentloc = self.reader.get_agent()
        goalloc = self.reader.get_goal()
        walls = self.reader.get_walls()
        self.treebased = Agent(agentloc[0], agentloc[1], goalloc[0], goalloc[1], gridsize[1], gridsize[0], walls)
        self.treebased2 = Agent(agentloc[0], agentloc[1], goalloc[2], goalloc[3], gridsize[1], gridsize[0], walls)

    def draw(self):
        return ""

    def bfs_search(self):
        result_json_string = self.treebased.bfs_search()
        result = json.loads(result_json_string)
        if 'result' in result:
            print("Path: ", result['result'].get('Path', 'No path found'))
        else:
            print("Search status: ", result.get('status', 'Unknown status'))
        # input("Press enter to show BFS for second goal")
        # print(self.treebased2.bfs_search())
        # input("Press enter to exit BFS")

    def dfs_search(self):
        print(self.treebased.dfs_search())
        # input("Press enter to show DFS for second goal")
        # print(self.treebased2.dfs_search())
        # input("Press enter to exit DFS")

    def gbfs_search(self):
        print(self.treebased.gbfs_search())
        # input("Press enter to show GBFS for second goal")
        # print(self.treebased2.gbfs_search())
        # input("Press enter to exit GBFS")

    def a_star_search(self):
        print(self.treebased.a_star_search())
        # input("Press enter to show AStar for second goal")
        # print(self.treebased2.a_star_search())
        # input("Press enter to exit AStar")

    def uniform_cost_search(self):
        print(self.treebased.uniform_cost_search())
        # input("Press enter to show Uniform Cost Searchfor second goal")
        # print(self.treebased2.uniform_cost_search())
        # input("Press enter to exit Uniform Cost Search")
    
    def iddfs_search(self):
        print(self.treebased.iddfs_search())
        # input("Press enter to show Uniform Cost for second goal")
        # print(self.treebased2.iddfs_search())
        # input("Press enter to exit Uniform Cost")

    def nodes_for_gui(self, algorithm_id):
        print("From Starter: Algorithm id: ", algorithm_id)
        if algorithm_id == 'BFS':
            result_json_string = self.treebased.bfs_search()
            result = json.loads(result_json_string)
            if 'result' in result:
                path = result['result'].get('Path', [])
                visited = [tuple(node.values()) for node in result['visited']]
                return path, visited
            else:
                return [], []  # No path found

