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

            if current_node.x == self.goalx and current_node.y == self.goaly:
                path = self._reconstruct_path(current_node)
                print("Function execution time: {} milliseconds".format((time.time() - start_time) * 1000))
                print("Visited: {}".format('; '.join('[{},{}]'.format(node.x, node.y) for node in visited)))
                print("Number of nodes in the frontier: {}".format(len(frontier)))
                return "GBFS Completed;\nAgent: [{},{}]\nGoal: [{},{}]\nPath: {}\nSteps: {}".format(self.root.x, self.root.y, self.goalx, self.goaly, self._format_path(path), len(visited))

            for neighbor in sorted(self._get_neighbors(current_node), key=lambda x: (self._heuristic(x), priority_map.get((x.x - current_node.x, x.y - current_node.y), 99))):
                if neighbor not in visited and not any(node[2] == neighbor for node in frontier) and neighbor not in self.wallnodes:
                    neighbor.parent = current_node  # Set the parent of the neighbor before pushing to the heap
                    counter += 1
                    heappush(frontier, (self._heuristic(neighbor), counter, neighbor))

        return "Failed to get solution"

    def _heuristic(self, node):
        return abs(node.x - self.goalx) + abs(node.y - self.goaly)

    def _reconstruct_path(self, current_node):
        path = []
        while current_node:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()
        return path
    
    def _get_neighbors(self, current_node):
        # Up, Left, Down, Right
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        neighbors = []
        for dx, dy in directions:
            new_x, new_y = current_node.x + dx, current_node.y + dy
            if 0 <= new_x < self.length and 0 <= new_y < self.width:
                # Use the existing node from the 2D array
                neighbors.append(self.nodes[new_x][new_y])
        return neighbors

    def _format_path(self, path):
        # Define directions based on the delta of x and y coordinates
        directions = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
        path_str = "[{},{}]".format(path[0].x, path[0].y)  # Start with the root node

        for i in range(1, len(path)):
            dx, dy = path[i].x - path[i - 1].x, path[i].y - path[i - 1].y
            direction = directions.get((dx, dy), '')
            path_str += " => {} => [{},{}]".format(direction, path[i].x, path[i].y)

        return path_str

    

   
    