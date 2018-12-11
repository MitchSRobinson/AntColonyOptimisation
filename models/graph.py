import numpy as np


class Graph(object):
    """
    This class represents the pheromone weights across the bin-item matrix.

    Attributes
    ----------
    graph : np.array(int)
        3-d array of pheromone weights.
    evaporation_rate : float
        Scalar value to evaporate the pheromone weights.

    Methods
    -------
    evaporate()
        Reduce the pheromone weights across the graph.
    """
    
    def __init__(self, b, i, e_r):
        self.graph = np.random.rand(b, i, b)
        self.evaporation_rate = e_r

    def __repr__(self):
        return "Graph Object: " + str(self.graph)

    def evaporate(self):
        """Reduce the pheromone weights across the graph."""
        self.graph = self.graph * self.evaporation_rate


if __name__ == "__main__":
    print("Test 'Graph' class: [10 bins x 200 items]")
    graph = Graph(10, 200, 0.9)
    print(graph)
