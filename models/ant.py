class Ant(object):
    """
    This class represents an ant and stores the information about its route and fitness.

    Attributes
    ----------
    route : array(tuple(int, int))
        a list of coordinates that represent the bin-item configuration.
    fitness : int
        the current fitness of the ants route.
    bins : array(Bin)
        holds the bin configuration if the ant is chosen as a generational champion.

    Methods
    -------
    lay_pheromones(graph)
        Distributes a pheromone weight on the graph at the positions defined in the route attribute.
    copy()
        Similar to deepcopy - creates a replica object of the ant.
    get_route_as_str()
        Format the route in a human readable format.
    """

    route = []
    fitness = -1
    bins = []

    def lay_pheromones(self, graph):
        """Distributes a pheromone weight on the graph at the positions defined in the route attribute."""
        pheromone_weight = 100.0 / self.fitness
        previous_bin = 0
        for b, item in self.route:
            graph.graph[previous_bin, item, b] += pheromone_weight
            previous_bin = b

    def copy(self):
        """Creates a replica object of the ant."""
        new_ant = Ant()
        new_ant.route = [r for r in self.route]
        new_ant.bins = self.bins.copy()
        new_ant.fitness = self.fitness
        return new_ant

    def get_route_as_str(self):
        """Format the route in a human readable format."""
        return " -> ".join("Item %d in Bin %d" % (point[1] + 1, point[0]) for point in self.route)