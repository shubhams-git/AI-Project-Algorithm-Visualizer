class Node:
    """
    Represents a node in a graph for pathfinding algorithms, encapsulating position,
    cost, and connectivity details.
    """
    def __init__(self, givx, givy, parentnode=None):
        self.x = givx
        self.y = givy
        self.wallstatus = False # Indicates whether the node is impassable
        self.parent = parentnode
        self.cost = float('inf')  # Pathfinding cost initialized to infinity
        self.edges = []  # Adjacent nodes

    @property
    def X(self):
        return self.x

    @X.setter
    def X(self, value):
        self.x = value

    @property
    def Y(self):
        return self.y

    @Y.setter
    def Y(self, value):
        self.y = value

    @property
    def Wallstatus(self):
        return self.wallstatus

    @Wallstatus.setter
    def Wallstatus(self, value):
        self.wallstatus = value # Sets node as a wall if True

    @property
    def Parent(self):
        return self.parent

    @Parent.setter
    def Parent(self, value):
        self.parent = value

    @property
    def Edges(self):
        return self.edges # Updates connections to other nodes

    @Edges.setter
    def Edges(self, value):
        self.edges = value

    @property
    def Cost(self):
        return self.cost

    @Cost.setter
    def Cost(self, value):
        self.cost = value # Updates the cost of reaching this node
