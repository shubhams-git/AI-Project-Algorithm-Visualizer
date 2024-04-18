import time
from queue import Queue, LifoQueue, PriorityQueue
from heapq import heappush, heappop
from Node import Node
import math
import json



class Agent:
    def __init__(self, rootx, rooty, givengoalx, givengoaly, givlength, givwidth, walls):
        # Create a 2D array of nodes
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
            visited.append({"x": current_node.x, "y": current_node.y})  # Store nodes as dictionaries
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
                    "Steps": steps
                }
                return json.dumps(response)

            for neighbor in self._get_neighbors(current_node):
                neighbor_coords = {"x": neighbor.x, "y": neighbor.y}
                if (not any(node['x'] == neighbor.x and node['y'] == neighbor.y for node in visited) and
                    neighbor not in [n for n in frontier.queue] and
                    not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes)):
                    neighbor.parent = current_node  # Set the parent of the neighbor
                    frontier.put(neighbor)

        response['status'] = "Failed to find solution"
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)
    
    def dfs_search(self):
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
                visited.append({"x": current_node.x, "y": current_node.y})  # Store nodes as dictionaries
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
                        "Steps": steps
                    }
                    return json.dumps(response)
                
                for neighbor in reversed(self._get_neighbors(current_node)):
                     if (not any(node['x'] == neighbor.x and node['y'] == neighbor.y for node in visited) and
                        not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes)):
                        neighbor.parent = current_node
                        frontier.put(neighbor)

        response['status'] = "Failed to find solution"
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)
    
    def search(self, use_cost=True, use_heuristic=True):
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
                    "Steps": steps
                }
                return json.dumps(response)
            
            for neighbor in self._get_neighbors(current_node):
                if (neighbor.x, neighbor.y) in visited or any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes):
                    continue  # Consistently handle walls

                tentative_cost = current_node.Cost + 1 if use_cost else 0
                heuristic_cost = self._heuristic(neighbor) if use_heuristic else 0
                total_cost = tentative_cost + heuristic_cost

                if total_cost < getattr(neighbor, 'cost', float('inf')):
                    neighbor.cost = tentative_cost
                    neighbor.parent = current_node
                    counter += 1
                    frontier.put((total_cost, counter, neighbor))

        response['status'] = "Failed to find solution"
        response['function_time'] = (time.time() - start_time) * 1000
        response['frontier_size'] = frontier.qsize()
        return json.dumps(response)

    def gbfs_search(self):
        return self.search(use_cost=False, use_heuristic=True)
    
    def a_star_search(self):
        return self.search(use_cost=True, use_heuristic=True)
    
    def uniform_cost_search(self):
        return self.search(use_cost=True, use_heuristic=False)
        
    def iddfs_search(self):
        response = {}
        start_time = time.time()
        max_depth = 0
        all_visited = []  # List to keep track of all visited nodes across all depths

        while True:
            visited_this_depth = []  # List to track nodes visited at this depth
            result, path = self._dls(self.root, self.goalx, self.goaly, max_depth, visited_this_depth)
            for node in visited_this_depth:
                if node not in all_visited:
                    all_visited.append(node)  # Append this depth's visits to overall visits only if not already visited
            if result != "continue":
                execution_time = time.time() - start_time
                response['function_time'] = execution_time * 1000
                response['visited'] = [{'x': node.x, 'y': node.y} for node in all_visited]
                response['total_visits'] = len(all_visited)
                if result == "success":
                    response['status'] = "IDDFS Completed"
                    response['result'] = {
                        "Path": self._format_path(path),
                        "Steps": len(path)
                    }
                else:
                    response['status'] = "Failed to find a solution"
                return json.dumps(response)
            max_depth += 1


    def _dls(self, node, goalx, goaly, depth, visited):
        # Append node to visited list to maintain the order of visitation only if it's not already in the list
        if node not in visited:
            visited.append(node)

        if node.x == goalx and node.y == goaly:
            return "success", [node]
        if depth == 0:
            return "continue", []

        for neighbor in self._get_neighbors(node):
            if neighbor not in visited and neighbor not in self.wallnodes:
                neighbor.parent = node
                result, path = self._dls(neighbor, goalx, goaly, depth - 1, visited)
                if result == "success":
                    return "success", [node] + path

        return "continue", []


    
    def bidirectional_search(self):
        print("Currently running Bidirectional Search.")
        start_time = time.time()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            print("Function execution time: {} seconds".format(time.time() - start_time))
            return "Agent at goal already"

        from_start = Queue()
        from_goal = Queue()

        visited_from_start = {self.root: None}  # Dictionary to track path and check for visits
        visited_from_goal = {self.nodes[self.goalx][self.goaly]: None}  # Dictionary to track path and check for visits

        from_start.put(self.root)
        from_goal.put(self.nodes[self.goalx][self.goaly])

        while not from_start.empty() and not from_goal.empty():
            if self._meet_in_middle(from_start, visited_from_start, visited_from_goal, True):
                mid_node, path = self._reconstruct_bidirectional_path(visited_from_start, visited_from_goal, True)
                execution_time = time.time() - start_time
                all_visited = list(visited_from_start.keys()) + list(visited_from_goal.keys())
                print("Function execution time: {} milliseconds".format(execution_time * 1000))
                print("Visited Nodes: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in set(all_visited))))
                return f"Bidirectional Search Completed;\nPath: {self._format_path(path)}\nSteps: {len(path)}"

            if self._meet_in_middle(from_goal, visited_from_goal, visited_from_start, False):
                mid_node, path = self._reconstruct_bidirectional_path(visited_from_goal, visited_from_start, False)
                execution_time = time.time() - start_time
                all_visited = list(visited_from_start.keys()) + list(visited_from_goal.keys())
                print("Function execution time: {} milliseconds".format(execution_time * 1000))
                print("Visited Nodes: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in set(all_visited))))
                return f"Bidirectional Search Completed;\nPath: {self._format_path(path)}\nSteps: {len(path)}"

        return "Failed to find a solution"
    
    def _meet_in_middle(self, frontier, visited_by_this, visited_by_other, from_start):
        if not frontier.empty():
            current = frontier.get()

            for neighbor in self._get_neighbors(current):
                if neighbor not in self.wallnodes and neighbor not in visited_by_this:
                    visited_by_this[neighbor] = current
                    frontier.put(neighbor)
                    if neighbor in visited_by_other:
                        return True
        return False
 
    def _reconstruct_bidirectional_path(self, visited_from_one_side, visited_from_other_side, from_start):
        # Find meeting point
        meet_point = next(node for node in visited_from_one_side if node in visited_from_other_side)

        # Path from start to meet_point
        path_from_one_side = []
        step = meet_point
        while step is not None:
            path_from_one_side.append(step)
            step = visited_from_one_side[step]

        # Path from goal to meet_point
        path_from_other_side = []
        step = visited_from_other_side[meet_point]
        while step is not None:
            path_from_other_side.append(step)
            step = visited_from_other_side[step]

        # Depending on the direction of the search, reverse the appropriate path
        if from_start:
            path_from_one_side.reverse()  # Reverse the path from start to meet_point
            full_path = path_from_one_side + path_from_other_side
        else:
            path_from_other_side.reverse()  # Reverse the path from goal to meet_point
            full_path = path_from_other_side + path_from_one_side

        return meet_point, full_path

   
    def _get_neighbors(self, current_node):
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Up, Left, Down, Right
        neighbors = []
        for dx, dy in directions:
            nx, ny = current_node.x + dx, current_node.y + dy
            if 0 <= nx < self.length and 0 <= ny < self.width and self.nodes[nx][ny] not in self.wallnodes:
                neighbors.append(self.nodes[nx][ny])
        return neighbors

    def _heuristic(self, node):
        # Manhattan distance is used as the heuristic
        return abs(node.x - self.goalx) + abs(node.y - self.goaly)

    def _reconstruct_path(self, current_node):
        path = []
        while current_node:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()
        return path
    
    def _format_path(self, path):
        # Return a list of tuples where each tuple is (x, y) of a node along the path
        path_coordinates = [(node.x, node.y) for node in path]
        return path_coordinates

    def reset_nodes(self):
        for row in self.nodes:
            for node in row:
                node.cost = float('inf')  # Reset cost to infinity
                node.parent = None  # Reset the parent node
