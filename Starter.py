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

    def execute_search(self, algorithm):
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
            result_json_string = self.treebased.ldfs_search()
        elif algorithm == "CUS2":
            result_json_string = self.treebased.hill_climbing_search()
        
        result = json.loads(result_json_string)
        if 'result' in result:
            steps = result['result'].get('Steps', 0)
            goal = result['result'].get('Goal', [-1, -1])  # Default to [-1, -1] if no goal is found
            path = result['result'].get('Path_Directions', [-1,-1])
            if goal[0] != -1:  # Check if goal is reachable
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
        if goal[0] != -1:
            return f"<Node ({goal[0]}, {goal[1]})> {steps}"
        else:
            return f"No goal is reachable; {steps}"


    def reset_nodes(self):
        return self.treebased.reset_nodes()

    def nodes_for_gui(self, algorithm_id):
        print("From Starter: Algorithm id: ", algorithm_id)
        result_json_string = self.treebased.bfs_search()

        if algorithm_id == 'BFS':
            pass
        elif algorithm_id == 'DFS':
            result_json_string = self.treebased.dfs_search()
        elif algorithm_id == 'AStar':
            result_json_string = self.treebased.a_star_search()
        elif algorithm_id == 'GBFS':
            result_json_string = self.treebased.gbfs_search()
        elif algorithm_id == 'Uniform Cost':
            result_json_string = self.treebased.ldfs_search()
        elif algorithm_id == 'Hill Climbing':
            result_json_string = self.treebased.hill_climbing_search()
            

        result = json.loads(result_json_string)
        if 'result' in result:
            path = result['result'].get('Path', [])
            steps = result['result'].get('Steps', 0)  # Extract step count from result
            visited = [tuple(node.values()) for node in result['visited']]
            status = result['status']
            return path, visited, steps, status
        else:
            if 'status' in result:
                visited = [tuple(node.values()) for node in result['visited']]
                status = result['status']
                print(status)
                return [],visited,0, status
            return [], [], 0, ""  # No path or steps found


