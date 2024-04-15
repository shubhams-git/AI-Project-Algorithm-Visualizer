import time
from queue import Queue, LifoQueue, PriorityQueue
from heapq import heappush, heappop
from Node import Node
import math



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
        steps = 0
        print("Currently running BFS.")
        start_time = time.time()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            print("Function execution time: {} seconds".format(time.time() - start_time))
            return "Agent at goal already"

        frontier = Queue()
        visited = []
        frontier.put(self.root)

        while not frontier.empty():
            current_node = frontier.get()
            visited.append(current_node)
            steps += 1

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                print("Function execution time: {} milliseconds".format((time.time() - start_time) * 1000))
                print("Visited: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in visited)))
                print("Number of nodes in the frontier: {}".format(frontier.qsize()))  # Print the number of nodes in the frontier
                return "BFS Completed;\nAgent: [{},{}]\nGoal: [{},{}]\nPath: {}\nSteps: {}".format(self.root.x, self.root.y, self.goalx, self.goaly, self._format_path(path), steps)

            for neighbor in self._get_neighbors(current_node):
                if (neighbor not in visited and 
                    neighbor not in [n for n in frontier.queue] and 
                    not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes)):
                    neighbor.parent = current_node  # Set the parent of the neighbor
                    frontier.put(neighbor)

        print("Number of nodes in the frontier: {}".format(frontier.qsize()))  # Print the number of nodes in the frontier
        return "Failed to get solution"

    def dfs_search(self):
        steps = 0
        print("Currently running DFS.")
        start_time = time.time()

        if self.root.x == self.goalx and self.root.y == self.goaly:
            print("Function execution time: {} seconds".format(time.time() - start_time))
            return "Agent at goal already"

        frontier = LifoQueue()
        visited = []
        frontier.put(self.root)

        while not frontier.empty():
            current_node = frontier.get()
            visited.append(current_node)
            steps += 1

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                print("Function execution time: {} milliseconds".format((time.time() - start_time) * 1000))
                print("Visited: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in visited)))
                print("Number of nodes in the frontier: {}".format(frontier.qsize()))  # Print the number of nodes in the frontier
                return "DFS Completed;\nAgent: [{},{}]\nGoal: [{},{}]\nPath: {}\nSteps: {}".format(self.root.x, self.root.y, self.goalx, self.goaly, self._format_path(path), steps)

            neighbors = self._get_neighbors(current_node)
            neighbors.reverse()  # Reverse the order of neighbors
            for neighbor in neighbors:
                if (neighbor not in visited and 
                    neighbor not in [n for n in frontier.queue] and 
                    not any(node.x == neighbor.x and node.y == neighbor.y for node in self.wallnodes)):
                    neighbor.parent = current_node  # Set the parent of the neighbor
                    frontier.put(neighbor)

        print("Number of nodes in the frontier: {}".format(frontier.qsize()))  # Print the number of nodes in the frontier
        return "Failed to get solution"
    
    
    def gbfs_search(self):
        steps = 0
        print("Currently running GBFS.")
        start_time = time.time()
        if self.root.x == self.goalx and self.root.y == self.goaly:
            print("Function execution time: {} seconds".format(time.time() - start_time))
            return "Agent at goal already"

        priority_map = {(0, -1): 0, (-1, 0): 1, (0, 1): 2, (1, 0): 3}  # Priorities: Up, Left, Down, Right
        frontier = []
        visited = []
        counter = 0
        heappush(frontier, (0, counter, self.root))

        while frontier:
            _, __, current_node = heappop(frontier)
            visited.append(current_node)
            steps += 1


            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                print("Function execution time: {} milliseconds".format((time.time() - start_time) * 1000))
                print("Visited: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in visited)))
                print("Number of nodes in the frontier: {}".format(len(frontier)))
                return "GBFS Completed;\nAgent: [{},{}]\nGoal: [{},{}]\nPath: {}\nSteps: {}".format(self.root.x, self.root.y, self.goalx, self.goaly, self._format_path(path), steps)

            for neighbor in sorted(self._get_neighbors(current_node), key=lambda x: (self._heuristic(x), priority_map.get((x.x - current_node.x, x.y - current_node.y), 99))):
                if (neighbor not in visited and 
                    neighbor not in [n for n in frontier]  and
                    neighbor not in self.wallnodes):
                    neighbor.parent = current_node  # Set the parent of the neighbor before pushing to the heap
                    counter += 1
                    heappush(frontier, (self._heuristic(neighbor), counter, neighbor))

        return "Failed to get solution"
    
    def a_star_search(self):
        steps = 0
        print("Currently running A Star Algorithm.")
        start_time = time.time()
        self.root.cost = 0  # Initialize the starting node's cost to 0

        if self.root.x == self.goalx and self.root.y == self.goaly:
            print("Function execution time: {} seconds".format(time.time() - start_time))
            return "Agent at goal already"

        # Modify the structure to use a list and heapq as in gbfs_search
        frontier = []
        visited = []
        counter = 0
        heappush(frontier, (0, counter, self.root))

        while frontier:
            _, __, current_node = heappop(frontier)
            visited.append(current_node)
            steps += 1

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                execution_time = time.time() - start_time
                print("Function execution time: {} milliseconds".format(execution_time * 1000))
                print("Visited: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in visited)))
                print("Number of nodes in the frontier: {}".format(len(frontier)))
                return "A* Completed;\nAgent: [{},{}]\nGoal: [{},{}]\nPath: {}\nSteps: {}".format(self.root.x, self.root.y, self.goalx, self.goaly, self._format_path(path), steps)

            for neighbor in self._get_neighbors(current_node):
                if (neighbor.x, neighbor.y) in visited or neighbor in self.wallnodes:
                    continue  # Consistently handle walls

                tentative_cost = current_node.cost + 1
                if tentative_cost < neighbor.cost:
                    neighbor.cost = tentative_cost
                    total_cost = tentative_cost + self._heuristic(neighbor)
                    neighbor.parent = current_node
                    counter += 1
                    heappush(frontier, (total_cost, counter, neighbor))

        return "Failed to find a solution"
    
    def uniform_search(self):
        print("Currently running Uniform Cost Search.")
        start_time = time.time()
        self.root.cost = 0  # Start with the root node having zero cost

        if self.root.x == self.goalx and self.root.y == self.goaly:
            print("Function execution time: {} seconds".format(time.time() - start_time))
            return "Agent at goal already"

        frontier = []
        visited = []
        counter = 0
        heappush(frontier, (self.root.cost, counter, self.root))  # Push the root with its cost to the frontier

        while frontier:
            current_cost, _, current_node = heappop(frontier)
            visited.append(current_node)

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                execution_time = time.time() - start_time
                print("Function execution time: {} milliseconds".format(execution_time * 1000))
                print("Visited: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in visited)))
                print("Number of nodes in the frontier: {}".format(len(frontier)))
                return "Uniform Cost Search Completed;\nAgent: [{},{}]\nGoal: [{},{}]\nPath: {}\nSteps: {}".format(self.root.x, self.root.y, self.goalx, self.goaly, self._format_path(path), len(path))

            for neighbor in self._get_neighbors(current_node):
                if neighbor in visited or neighbor in self.wallnodes:
                    continue

                tentative_cost = current_cost + 1  # Assuming uniform step cost

                if not any((neighbor.x == n.x and neighbor.y == n.y) for _, _, n in frontier):
                    neighbor.parent = current_node
                    neighbor.cost = tentative_cost
                    counter += 1
                    heappush(frontier, (tentative_cost, counter, neighbor))
                else:
                    # Check if a cheaper path to the neighbor exists
                    for i, (cost, _, n) in enumerate(frontier):
                        if n.x == neighbor.x and n.y == neighbor.y and cost > tentative_cost:
                            frontier[i] = (tentative_cost, counter, neighbor)
                            neighbor.parent = current_node
                            neighbor.cost = tentative_cost
                            heappush(frontier, heappop(frontier))  # Reorder the heap after modification
                            break

        return "Failed to find a solution"
    
    def iddfs_search(self):
        print("Currently running Iterative Deepening Depth-First Search.")
        start_time = time.time()
        max_depth = 0
        all_visited = []  # List to keep track of all visited nodes across all depths

        while True:
            visited_this_depth = []
            result, path = self._dls(self.root, self.goalx, self.goaly, max_depth, visited_this_depth)
            all_visited.extend(visited_this_depth)  # Extend the overall visited list with this depth's visits
            if result != "continue":
                execution_time = time.time() - start_time
                print("Function execution time: {} milliseconds".format(execution_time * 1000))
                print("Visited Nodes: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in all_visited)))
                if result == "success":
                    return "IDDFS Completed;\nPath: {}\nSteps: {}".format(self._format_path(path), len(path))
                else:
                    return "Failed to find a solution"
            max_depth += 1

    def _dls(self, node, goalx, goaly, depth, visited):
        visited.append(node)  # Add the node to visited list
        if node.x == goalx and node.y == goaly:
            return "success", [node]
        if depth == 0:
            return "continue", []
        else:
            for neighbor in self._get_neighbors(node):
                if neighbor.parent is None and neighbor not in self.wallnodes:  # Avoid revisiting the parent and ensure not a wall
                    neighbor.parent = node
                    result, path = self._dls(neighbor, goalx, goaly, depth - 1, visited)
                    if result == "success":
                        return "success", [node] + path
                    neighbor.parent = None
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
        # Define directions based on the delta of x and y coordinates
        directions = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
        path_str = "[{},{}]".format(path[0].x, path[0].y)  # Start with the root node

        for i in range(1, len(path)):
            dx, dy = path[i].x - path[i - 1].x, path[i].y - path[i - 1].y
            direction = directions.get((dx, dy), '')
            path_str += " => {} => [{},{}]".format(direction, path[i].x, path[i].y)

        return path_str

    

   
    