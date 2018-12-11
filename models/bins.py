class Bin(object):
    """
    This class represents bin that can hold items and caches it's current fitness.

    Attributes
    ----------
    total_weight : int
        the sum of the items in the bin.
    items : array(int)
        the item weights currently in the bin.

    Methods
    -------
    add_item(item)
        Add an item to the bin and increase the total weight.
    copy()
        Similar to deepcopy - creates a replica object of the bin.
    empty()
        Reset the contents of the bin.
    """
    total_weight = 0
    items = []

    def __repr__(self):
        return "Bin with %d items weighing %d: %s" \
            % (len(self.items), self.total_weight, self.items)

    def add_item(self, item):
        """Add an item to the bin and increase the total weight."""
        self.items.append(item)
        self.total_weight += item

    def copy(self):
        """Creates a replica object of the bin."""
        new_bin = Bin()
        new_bin.total_weight = self.total_weight
        new_bin.items = [item for item in self.items]
        return new_bin

    def empty(self):
        """Reset the contents of the bin."""
        self.items = []
        self.total_weight = 0


def generate_bins(quantity):
    """This function creates a number of Bins and returns them as an array"""
    return [Bin() for _ in range(quantity)]


if __name__ == "__main__":
    print("Test 'generate_bins' function: [5 bins]")
    print(generate_bins(5))

    print("")
    
    print("Test 'generate_bins' function: [10 bins]")
    print(generate_bins(10))