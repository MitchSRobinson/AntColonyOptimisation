import random

def generate_items(lower=1, upper=200, quantity=200, scale=False, test=False):
    """This function creates an array of int weights given the parameters."""
    if not scale and not test:
        return [random.randint(lower, upper) for _ in range(quantity)]
    if scale:
        return [(i * random.randint(lower, upper)) / 2 for i in range(1, quantity + 1)]
    return [10 for _ in range(quantity)]

if __name__ == '__main__':
    print("Test 'generate_items' function: [defaults]")
    print(generate_items())

    print("")
    
    print("Test 'generate_items' function: [with scaling]")
    print(generate_items(scale=True))

    print("")

    print("Test 'generate_items' function: [with test]")
    print(generate_items(test=True))
