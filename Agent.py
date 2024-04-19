import time
from queue import Queue, LifoQueue, PriorityQueue
from heapq import heappush, heappop
from Node import Node
import math
import json

class Agent:
    def __init__(self, rootx, rooty, givengoalx, givengoaly, givlength, givwidth, walls):
        self.nodes = [[Node(x, y) for y in range(givwidth)] for x in range(givlength)]
        self.root = self.nodes[rootx][rooty]
        self.goalx = givengoalx
        self.goaly = givengoaly
        self.length = givlength
        self.width = givwidth
        self.wall = walls
        self.wallnodes = []
        for wall in walls:
            for i in range(wall[3]):
                for j in range(wall[2]):
                    self.wallnodes.append(self.nodes[wall[0] + j][wall[1] + i])
    
    def bfs_search(self):
        """
        Performs Breadth-First Search (BFS) from the root node to the goal node. BFS explores the graph
        level by level, starting at the root node and exploring all its neighbors at the current depth prior
        to moving on to nodes at the next depth level. This method uses a queue to keep track of the next node to visit.
        The function returns a JSON object containing the status of the search, time taken, path found, and other metrics.
        BFS is optimal for unweighted graphs and guarantees finding the shortest path.
        """
        response = {}
        steps = 0
        start_time = time.time()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            response['status'] = "Agent at goal already"
            response['function_time'] = (time.time() - start_time) * 1000
            return json.dumps(response)

        frontier = Queue()
        visited = []
        frontier.put(self.root)

        while not frontier.empty():
            current_node = frontier.get()
            visited.append({"x": current_node.x, "y": current_node.y}) 
            steps += 1

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                response['status'] = "BFS Completed"
                response['function_time'] = (time.time() - start_time) * 1000
                response['visited'] = visited
                response['frontier_size'] = frontier.qsize()
                response['result'] = {
                    "Agent": [self.root.x, self.root.y],
                    "Goal": [self.goalx, self.goaly],
                    "Path": self._format_path(path),
                    "Path_Directions": self._path_directions(path),
                    "Steps": steps
                }
                return json.dumps(response)

            for neighbor in self._get_neighbors(current_node):
                neighbor_coords = {"x": neighbor.x, "y": neighbor.y}
                if (not any(node['x'] == neighbor.x and node['y'] == neighbor.y for node in visited) and
                    neighbor not in [n for n in frontier.queue] and
                    not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes)):
                    neighbor.parent = current_node  
                    frontier.put(neighbor)

        response['status'] = "No goal found"
        response['visited'] = visited
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)
    
    def dfs_search(self):
        """
        Executes Depth-First Search (DFS) from the root node to the goal node. DFS explores as far as possible
        along each branch before backtracking, which means it uses a stack data structure to keep track of which node to visit next.
        This method might not find the shortest path, but it is useful for scenarios where complete search is needed without regard to path optimality.
        The function outputs a JSON object with details on the search status, time taken, and nodes visited.
        """
        response = {}
        steps = 0
        start_time = time.time()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            response['status'] = "Agent at goal already"
            response['function_time'] = (time.time() - start_time) * 1000
            return json.dumps(response)

        frontier = LifoQueue()
        visited = []
        frontier.put(self.root)

        while not frontier.empty():
            current_node = frontier.get()
            if current_node not in visited:
                visited.append({"x": current_node.x, "y": current_node.y}) 
                steps += 1

                if current_node.x == self.goalx and current_node.y == self.goaly:
                    path = self._reconstruct_path(current_node)
                    response['status'] = "DFS Completed"
                    response['function_time'] = (time.time() - start_time) * 1000
                    response['visited'] = visited
                    response['frontier_size'] = frontier.qsize()
                    response['result'] = {
                        "Agent": [self.root.x, self.root.y],
                        "Goal": [self.goalx, self.goaly],
                        "Path": self._format_path(path),
                        "Path_Directions": self._path_directions(path),
                        "Steps": steps
                    }
                    return json.dumps(response)
                
                for neighbor in reversed(self._get_neighbors(current_node)):
                     if (not any(node['x'] == neighbor.x and node['y'] == neighbor.y for node in visited) and
                        not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes)):
                        neighbor.parent = current_node
                        frontier.put(neighbor)

        response['status'] = "No goal found"
        response['visited'] = visited
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)
    
    def search(self, use_cost=True, use_heuristic=True):
        """
        Implements a flexible search algorithm that can be adapted to perform Uniform-Cost Search, A* Search, or Greedy Best-First Search depending on the flags used for cost and heuristic.
        The 'use_cost' flag enables or disables the consideration of the path cost from the root to the current node, while 'use_heuristic' controls the use of a heuristic function estimating the cost from the current node to the goal.
        This method uses a priority queue where each entry is prioritized based on the sum of the actual path cost and the heuristic value, making it suitable for a variety of pathfinding needs.
        It returns a JSON object with details about the search's progress, the path found, and the nodes visited, and it ensures that each node is visited at most once to maintain efficiency.
        """
        response = {}
        steps = 0
        start_time = time.time()
        status_message = "Currently running Search with" + (" Cost" if use_cost else "") + (" and Heuristic." if use_heuristic else ".")
        response['initial_status'] = status_message
        
        self.reset_nodes()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            response['status'] = "Agent at goal already"
            response['function_time'] = (time.time() - start_time) * 1000
            return json.dumps(response)

        frontier = PriorityQueue()
        visited = []
        self.root.Cost = 0
        counter = 0
        frontier.put((0, counter, self.root))

        while not frontier.empty():
            _, __, current_node = frontier.get()

            if (current_node.x, current_node.y) in visited:
                continue

            visited.append({"x": current_node.x, "y": current_node.y}) 
            steps += 1

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                response['status'] = "Search Completed"
                response['function_time'] = (time.time() - start_time) * 1000
                response['visited'] = visited
                response['frontier_size'] = frontier.qsize()
                response['result'] = {
                    "Agent": [self.root.x, self.root.y],
                    "Goal": [self.goalx, self.goaly],
                    "Path": self._format_path(path),
                    "Path_Directions": self._path_directions(path),
                    "Steps": steps
                }
                return json.dumps(response)
            
            for neighbor in self._get_neighbors(current_node):
                if (neighbor.x, neighbor.y) in visited or any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes):
                    continue 

                tentative_cost = current_node.Cost + 1 if use_cost else 0
                heuristic_cost = self._heuristic(neighbor) if use_heuristic else 0
                total_cost = tentative_cost + heuristic_cost

                if total_cost < getattr(neighbor, 'cost', float('inf')):
                    neighbor.cost = tentative_cost
                    neighbor.parent = current_node
                    counter += 1
                    frontier.put((total_cost, counter, neighbor))

        response['status'] = "No goal found"
        response['visited'] = visited
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)

    def gbfs_search(self):
        """
        Executes Greedy Best-First Search (GBFS), an informed search that uses a heuristic to prioritize nodes closest to the goal state.
        This method focuses only on the heuristic value (ignoring the cost to reach the node), potentially leading to faster but non-optimal paths.
        The function returns a JSON object detailing the search status, duration, and path outcomes, emphasizing speed over path optimality.
        """
        return self.search(use_cost=False, use_heuristic=True)
    
    def a_star_search(self):
        """
        Implements A* Search algorithm, which is an informed search algorithm that finds the least-cost path from start to goal.
        It combines aspects of uniform-cost search and a heuristic by optimizing the path cost from the start node along with an estimated cost from any node to the goal.
        A* is complete and optimal, given that the heuristic function is admissible. The response is formatted as JSON with comprehensive details on the search process.
        """
        return self.search(use_cost=True, use_heuristic=True)

    def dldfs_search(self, depth_limit=50):
        """
        Conducts Depth Limited Depth-First Search (DLDFS), a variant of DFS that limits the depth to a predetermined threshold.
        This method is useful in very large or infinite search spaces where standard DFS might suffer from excessive or infinite recursion.
        Returns JSON formatted results detailing each step's process, visited nodes, and the result of the search within the depth limit.
        """
        response = {}
        steps = 0
        start_time = time.time()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            response['status'] = "Agent at goal already"
            response['function_time'] = (time.time() - start_time) * 1000
            return json.dumps(response)

        frontier = LifoQueue() 
        visited = []
        frontier.put((self.root, 0))  

        while not frontier.empty():
            current_node, current_depth = frontier.get()
            visited.append({"x": current_node.x, "y": current_node.y})  
            steps += 1

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                response['status'] = "LDFS Completed"
                response['function_time'] = (time.time() - start_time) * 1000
                response['visited'] = visited
                response['frontier_size'] = frontier.qsize()
                response['result'] = {
                    "Agent": [self.root.x, self.root.y],
                    "Goal": [self.goalx, self.goaly],
                    "Path": self._format_path(path),
                    "Path_Directions": self._path_directions(path),
                    "Steps": steps
                }
                return json.dumps(response)

            if current_depth < depth_limit:
                for neighbor in reversed(self._get_neighbors(current_node)):
                    if not any(node['x'] == neighbor.x and node['y'] == neighbor.y for node in visited) and \
                    not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes):
                        neighbor.parent = current_node
                        frontier.put((neighbor, current_depth + 1))

        response['status'] = "No goal found"
        response['visited'] = visited
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)
    
    def hill_climbing_search(self):
        """
        Performs Hill Climbing Search, a local search algorithm that continuously moves towards the direction of increasing value (or decreasing cost),
        determined by a heuristic, to find the goal. It terminates when it reaches a peak where no adjacent neighbors have higher values.
        The method returns a JSON object with the path and steps taken until a solution is found or no further progress is possible.
        """
        response = {}
        start_time = time.time()
        steps = 0

        if self.root.x == self.goalx and self.root.y == self.goaly:
            response['status'] = "Agent at goal already"
            response['function_time'] = (time.time() - start_time) * 1000
            return json.dumps(response)

        current_node = self.root
        visited = [{"x": current_node.x, "y": current_node.y}]

        while current_node.x != self.goalx or current_node.y != self.goaly:
            neighbors = self._get_neighbors(current_node)
            if not neighbors:
                break

            neighbors.sort(key=lambda node: self._heuristic(node))
            
            next_node = neighbors[0]
            if self._heuristic(next_node) >= self._heuristic(current_node):
                break
            
            current_node = next_node
            visited.append({"x": current_node.x, "y": current_node.y})
            steps += 1

        if current_node.x == self.goalx and current_node.y == self.goaly:
            path = self._reconstruct_path(current_node)
            response['status'] = "Hill Climbing Search Completed"
            response['function_time'] = (time.time() - start_time) * 1000
            response['visited'] = visited
            response['result'] = {
                "Agent": [self.root.x, self.root.y],
                "Goal": [self.goalx, self.goaly],
                "Path": self._format_path(path),
                "Path_Directions": self._path_directions(path),
                "Steps": steps
            }
        else:
            response['visited'] = visited
            response['status'] = "No goal found"
            response['function_time'] = (time.time() - start_time) * 1000

        return json.dumps(response)


   
    def _get_neighbors(self, current_node):
        """
        Returns a list of accessible neighbors for the given node, excluding any that are walls or outside the grid boundaries.
        """
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Up, Left, Down, Right
        neighbors = []
        for dx, dy in directions:
            nx, ny = current_node.x + dx, current_node.y + dy
            if 0 <= nx < self.length and 0 <= ny < self.width and self.nodes[nx][ny] not in self.wallnodes:
                neighbors.append(self.nodes[nx][ny])
        return neighbors

    def _heuristic(self, node):
        """
        Calculates and returns the Manhattan distance from a given node to the goal, used as a heuristic for pathfinding.
        """
        return abs(node.x - self.goalx) + abs(node.y - self.goaly)

    def _reconstruct_path(self, current_node):
        """
        Reconstructs the path from the goal node back to the root node by following parent links and returns the sequence of nodes.
        """
        path = []
        while current_node:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()
        return path
    
    def _format_path(self, path):
        """
        Return a list of tuples where each tuple is (x, y) of a node along the path
        """
        path_coordinates = [(node.x, node.y) for node in path]
        return path_coordinates

    def reset_nodes(self):
        """
        Resets all nodes in the grid by setting their cost to infinity and parent to None, preparing them for a new search.
        """
        for row in self.nodes:
            for node in row:
                node.cost = float('inf') 
                node.parent = None  
    
    def _path_directions(self, path):
        """
        Generates a list of directional steps (up, left, down, right) for the given path based on the relative positions of consecutive nodes.
        """
        directions = {"(0, -1)": "up", "(-1, 0)": "left", "(0, 1)": "down", "(1, 0)": "right"}
        path_directions = []
        for i in range(1, len(path)):
            dx, dy = path[i].x - path[i-1].x, path[i].y - path[i-1].y
            direction = directions.get(str((dx, dy)), '')
            path_directions.append(direction)
        return path_directions
