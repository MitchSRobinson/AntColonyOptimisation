from operator import itemgetter
from time import time

from aco import ACO
from models.bins import generate_bins
from models.items import generate_items


def run_bpp(bins=10, scale=False):
    """Run a full bin packing problem test with the specificed parameters and return the results."""

    results = []

    bins = bins
    items = 200
    scale = scale
    rules = [
        {'population': 100, 'evaporation_rate': 0.9},
        {'population': 100, 'evaporation_rate': 0.4},
        {'population': 10,  'evaporation_rate': 0.9},
        {'population': 10,  'evaporation_rate': 0.4},
    ]

    # Test each rule configuration.
    for rule in rules:
        result = run_test(bins, items, rule['population'], rule['evaporation_rate'], scale=scale)
        results.append(result)
        print("Test Complete: Params - B=%d, I=200, S=%s, P=%d, E=%.1f" %
              (bins, scale, rule['population'], rule['evaporation_rate'])
              )
        print(" -- Achieved average fitness %.1f in %.2f seconds." % (result['average_fitness'], result['average_time']))
    return results


def run_test(bin_num, item_num, population, evaporation_rate, scale=False, verbose=False):
    """Run a singular ACO test and return an object of the results found."""
    results = []
    average_fitness = 0
    average_time = 0

    total_time = 0

    # Run 5 tests of the ACO algorithm and compile a set of averages.
    for i in range(5):
        bins = generate_bins(bin_num)
        items = generate_items(quantity=item_num, scale=scale)

        trial = ACO(bins, items, population, evaporation_rate, verbose=False)
        trial.run()

        fitness, time = trial.stats()
        results.append((fitness, time))
        average_fitness += fitness * 0.2
        average_time += time * 0.2

    log("Test finished in %d seconds." % total_time, verbose)
    log("Stats:", verbose)
    log(" -- Average Fitness of Test: %f" % average_fitness, verbose)
    log(" -- Average Time Per Test Run: %f" % average_time, verbose)

    return {
        'raw_results': results,
        'bins': bin_num,
        'items': item_num,
        'population': population,
        'evaporation_rate': evaporation_rate,
        'scale': scale,
        'average_fitness': average_fitness,
        'max_fitness': max(results, key=itemgetter(0))[0],
        'min_fitness': min(results, key=itemgetter(0))[0],
        'average_time': average_time,
        'max_time': max(results, key=itemgetter(1))[1],
        'min_time': min(results, key=itemgetter(1))[1],
        'total_time': total_time
    }


def pretty_print_results(results):
    """This function helps to format the results object in a readable format."""
    for i, bpp_results in enumerate(results):
        print("\nResult Set For BPP%s\n" % str(i+1))
        for j, test in enumerate(bpp_results):
            print("Test Conditions: - B=%d, I=%d, P=%d, E=%f, S=%s" %
                  (test['bins'], test['items'], test['population'], test['evaporation_rate'], test['scale'])
                  )
            print("Fitness - AVG: %6.1f MAX: %6s MIN: %6s    Time - AVG: %6.2f MAX: %6.2f MIN: %6.2f\n" % (
                test['average_fitness'],
                test['max_fitness'],
                test['min_fitness'],
                test['average_time'],
                test['max_time'],
                test['min_time']
            ))


def log(message, verbose=False):
    """Output to the console if verbose is true."""
    if verbose:
        print(message)


if __name__ == "__main__":
    print("Starting Full Test...")
    start_time = time()
    total_res = []
    print("Starting BPP1...")
    total_res.append(run_bpp())
    print("Finished BPP1.")
    print("Starting BPP2...")
    total_res.append(run_bpp(50, True))
    print("Finished BPP2.")

    print("Full test executed in %.2f" % float(time() - start_time))
    print("Results...\n\n")
    pretty_print_results(total_res)
