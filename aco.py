from random import random
from time import time
from itertools import repeat
from matplotlib import pyplot as plt

from models.graph import Graph
from models.ant import Ant


class ACO(object):
    """This class holds all relevant infomation for objects required for running the ACO algorithm.

    ...

    Attributes
    ----------
    bins : Bin
        a bin object that holds items and a total weight.
    items : array(int)
        an array of integers representing the weights of items.
    ants : array(Ant)
        an array of Ant objects to be controlled during the algorithms run.
    best_ant : Ant
        an ant object - the best ant of the final generation of a algorithm run.
    graph : Graph
        a graph object to store the pheromone weights.
    num_paths : int
        the number of routes evaluated.
    limit : int
        the maximum number of evaluations allowed.
    verbose : boolean
        whether or not to print to the console when log() is called.
    ran : boolean
        has the ACO been run.
    runtime : float
        time duration of the last run.
    avg_fits : array(float)
        the timeseries of average fitnesses over each cycle.

    Methods
    -------
    summary()
        prints a summary of the last run if there is one.
    stats()
        returns the best fitness and time elapsed over last run if there is one.
    run()
        runs the ACO algorithm.
    explore()
        runs one cycle of route creation and evaporation.
    ant_run(ant)
        reset the ant and recreate its route.
    create_route(ant)
        create a route through the graph of pheromones.
    route_step(prev_bin, item)
        return a step from the current bin to the next bin position.
    route_fitness()
        calculate the fitness for the current bin configuration.
    set_champion()
        set the best ant for the current generation.
    empty_bins()
        reset all bins.
    log(message)
        prints to the console if verbose is true.
    graph_averages()
        create a graph using the data from avg_fits.
    """

    def __init__(self, bins, items, population, evaporation_rate, limit=10000, verbose=False):
        """Initialise the ACO object with the required parameters."""
        self.bins = bins
        self.items = items

        self.ants = [Ant() for _ in range(population)]
        self.best_ant = None

        self.graph = Graph(len(bins), len(items), evaporation_rate)

        self.num_paths = 0
        self.limit = limit
        self.verbose = verbose

        self.ran = False
        self.runtime = 0

        self.avg_fits = []

    def summary(self):
        """Print a summary of the last run if there is one."""
        if hasattr(self, 'ran') and self.ran:
            print("Run was successful and took %d seconds." % int(self.runtime))
            print("--- Best fitness: %d" % self.best_ant.fitness)
            print("--- Best bin config:")
            for i, b in enumerate(self.best_ant.bins):
                print("%4d. %s" % (i + 1, b))

    def stats(self):
        """Return the best fitness achieved in the final generation and the time taken to run the ACO"""
        if hasattr(self, 'ran') and self.ran:
            return self.best_ant.fitness, self.runtime

    def run(self):
        """Runs a full ACO run."""
        self.log("--- Starting ACO Run ---")
        self.ran = False
        self.best_fits = []
        self.avg_fits = []
        start_time = time()

        while self.num_paths < self.limit:
            self.explore()

        self.set_champion()

        self.ran = True
        self.runtime = time() - start_time

    def explore(self):
        """Create a route for all ants and evaporate the graph."""
        self.ants = [*map(self.ant_run, self.ants)]
        best = None
        for ant in self.ants:
            ant.lay_pheromones(self.graph)
        fitnesses = [ant.fitness for ant in self.ants]
        self.best_fits.append(min(fitnesses) / sum(self.items))
        self.avg_fits.append(sum(fitnesses) / len(fitnesses))
        self.graph.evaporate()

    def ant_run(self, ant):
        """Reset the bins and create a route for the given ant."""
        self.empty_bins()
        ant = self.create_route(ant)
        ant.bins = self.bins.copy()
        return ant

    def create_route(self, ant):
        """Calculate a route through the pheromone graph."""
        prev_bin = 0
        ant.route = []
        for item in enumerate(self.items):
            prev_bin, item = self.route_step(prev_bin, item)
            ant.route.append((prev_bin, item))

        ant.fitness = self.route_fitness()

        self.num_paths += 1

        return ant

    def route_step(self, prev_bin, item):
        """Get the index of the next bin to place the item in."""
        column = self.graph.graph[prev_bin][item[0]].tolist()
        total = sum(column)
        threshold = total * random()

        current = 0.0
        for index, weight in enumerate(column):
            if current + weight >= threshold:
                self.bins[index].add_item(item[1])
                return index, item[0]
            current += weight

    def route_fitness(self):
        """Calculate the fitness of the current bin configuration."""
        max_weight = self.bins[0].total_weight
        min_weight = self.bins[0].total_weight
        for b in self.bins:
            if b.total_weight > max_weight:
                max_weight = b.total_weight
            if b.total_weight < min_weight:
                min_weight = b.total_weight

        return max_weight - min_weight

    def set_champion(self):
        """Allocate the best ant of the generation to the best_ant."""
        for ant in self.ants:
            if self.best_ant and ant.fitness < self.best_ant.fitness:
                    self.best_ant = ant.copy()
            elif not self.best_ant:
                self.best_ant = ant.copy()

    def empty_bins(self):
        """Resets the bin configuration."""
        [b.empty() for b in self.bins]

    def log(self, message):
        """Prints a message to the console if verbose is true."""
        if self.verbose:
            print(message)

    def graph_averages(self):
        """Output a graph to the user based on the values in avg_fits"""
        plt.plot(self.avg_fits)
        plt.show()


if __name__ == '__main__':
    from models.bins import generate_bins
    from models.items import generate_items

    bins = generate_bins(10)
    items = generate_items(quantity=200)
    population = 10
    evaporation_rate = 0.4

    trial = ACO(bins, items, population, evaporation_rate, verbose=True)
    trial.run()
    trial.graph_averages()
