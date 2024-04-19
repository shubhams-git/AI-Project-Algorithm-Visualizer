from Agent import Agent
from FileReader import FileReader
import json


class Starter:
    """
    Coordinates initialization and execution of search algorithms on a pathfinding agent based on input data.
    """
    def __init__(self, textfile):
        self.reader = FileReader(textfile)
        self.reader.read()
        gridsize = self.reader.get_grid()
        agentloc = self.reader.get_agent()
        goalloc = self.reader.get_goal()
        walls = self.reader.get_walls()
        self.treebased = Agent(agentloc[0], agentloc[1], goalloc[0], goalloc[1], gridsize[1], gridsize[0], walls)

    def execute_search(self, algorithm):
        """
        Executes the search algorithm specified by 'algorithm'. Initial execution defaults to BFS for setup.
        Processes the result into a readable format and returns the path if available.
        """
        result_json_string = self.treebased.bfs_search()
        if algorithm == "BFS":
            pass
        elif algorithm == "DFS":
            result_json_string = self.treebased.dfs_search()
        elif algorithm == "AS":
            result_json_string = self.treebased.a_star_search()
        elif algorithm == "GBFS":
            result_json_string = self.treebased.gbfs_search()
        elif algorithm == "CUS1":
            result_json_string = self.treebased.dldfs_search()
        elif algorithm == "CUS2":
            result_json_string = self.treebased.hill_climbing_search()
        
        result = json.loads(result_json_string)
        if 'result' in result:
            steps = result['result'].get('Steps', 0)
            goal = result['result'].get('Goal', [-1, -1])
            path = result['result'].get('Path_Directions', [-1,-1])
            if goal[0] != -1:
                print(self._format_goal_result(goal, steps))
                if path != [-1,-1]:
                    return path
                else:
                    return "" 
            else:
                return "No goal is reachable; {}".format(steps)
        else:
            steps = len(result['visited'])
            return "No goal is reachable; {}".format(steps)


    def _format_goal_result(self, goal, steps):
        """
        Returns a formatted string indicating the goal node and number of steps taken.
        """
        if goal[0] != -1:
            return f"<Node ({goal[0]}, {goal[1]})> {steps}"
        else:
            return f"No goal is reachable; {steps}"


    def reset_nodes(self):
        """
        Resets the states of all nodes in the agent's search space.
        """
        return self.treebased.reset_nodes()

    def nodes_for_gui(self, algorithm_id):
        """
        Executes a search using the specified algorithm and returns the results formatted for GUI display.
        """
        result_json_string = ""

        if algorithm_id == 'BFS':
            result_json_string = self.treebased.bfs_search()
        elif algorithm_id == 'DFS':
            result_json_string = self.treebased.dfs_search()
        elif algorithm_id == 'AStar':
            result_json_string = self.treebased.a_star_search()
        elif algorithm_id == 'GBFS':
            result_json_string = self.treebased.gbfs_search()
        elif algorithm_id == 'Depth Limited DFS':
            result_json_string = self.treebased.dldfs_search()
        elif algorithm_id == 'Hill Climbing':
            result_json_string = self.treebased.hill_climbing_search()
        else:
            print("There is some issue with the algorithm name")
            

        result = json.loads(result_json_string)
        if 'result' in result:
            path = result['result'].get('Path', [])
            steps = result['result'].get('Steps', 0)
            visited = [tuple(node.values()) for node in result['visited']]
            status = result['status']
            return path, visited, steps, status
        else:
            status = result.get('status', "")
            visited = [tuple(node.values()) for node in result.get('visited', [])]
            print(status if status else "No result provided")
            return [], visited, 0, status

