class Node:
    def __init__(self, givx, givy, parentnode=None):
        self.x = givx
        self.y = givy
        self.wallstatus = False
        self.parent = parentnode
        self.cost = float('inf')  # Initialize cost with infinity
        self.edges = []

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
        self.wallstatus = value

    @property
    def Parent(self):
        return self.parent

    @Parent.setter
    def Parent(self, value):
        self.parent = value

    @property
    def Edges(self):
        return self.edges

    @Edges.setter
    def Edges(self, value):
        self.edges = value

    @property
    def Cost(self):
        return self.cost

    @Cost.setter
    def Cost(self, value):
        self.cost = value
