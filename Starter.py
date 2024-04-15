from Agent import Agent
from FileReader import FileReader


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
        print(self.treebased.bfs_search())
        input("Press enter to show BFS for second goal")
        print(self.treebased2.bfs_search())
        input("Press enter to exit BFS")

    def dfs_search(self):
        print(self.treebased.dfs_search())
        input("Press enter to show DFS for second goal")
        print(self.treebased2.dfs_search())
        input("Press enter to exit DFS")

    def gbfs_search(self):
        print(self.treebased.gbfs_search())
        input("Press enter to show GBFS for second goal")
        print(self.treebased2.gbfs_search())
        input("Press enter to exit GBFS")

    def a_star_search(self):
        print(self.treebased.a_star_search())
        input("Press enter to show AStar for second goal")
        print(self.treebased2.a_star_search())
        input("Press enter to exit AStar")

    def uniform_search(self):
        print(self.treebased.uniform_search())
        input("Press enter to show Uniform Cost for second goal")
        print(self.treebased2.uniform_search())
        input("Press enter to exit Uniform Cost")
    
    def CUS1(self):
        print(self.treebased.iddfs_search())
        input("Press enter to show Uniform Cost for second goal")
        print(self.treebased2.iddfs_search())
        input("Press enter to exit Uniform Cost")

    def CUS2(self):
        print(self.treebased.bidirectional_search())
        input("Press enter to show Uniform Cost for second goal")
        print(self.treebased2.bidirectional_search())
        input("Press enter to exit Uniform Cost")
