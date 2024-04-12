import time
from queue import Queue, LifoQueue
from heapq import heappush, heappop
from Node import Node

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
                    frontier.put(neighbor)

        print("Number of nodes in the frontier: {}".format(frontier.qsize()))  # Print the number of nodes in the frontier
        return "Failed to get solution"



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
        directions = {"(0, -1)": "up", "(-1, 0)": "left", "(0, 1)": "down", "(1, 0)": "right"}
        path_str = ''
        for i in range(1, len(path)):
            dx, dy = path[i].x - path[i-1].x, path[i].y - path[i-1].y
            direction = directions.get(str((dx, dy)), '')
            path_str += "=>{}=>[{},{}]".format(direction, path[i].x, path[i].y)
        return "[{},{}]{}".format(self.root.x, self.root.y, path_str)
    

   
    