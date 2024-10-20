import random

def generate_random_dict(size=100, max_id=10, max_val=100, seed=42):
    """
    Generates a dictionary with 'id' and 'name' keys. Each key maps to a dictionary where the 
    keys are consecutive integers starting from 0 and the values are random integers.

    :param size: The number of entries to generate.
    :return: A dictionary with the given format.
    """
    random.seed(seed)

    random_dict = {
        'id': {i: random.randint(1, max_id) for i in range(size)},
        'value': {i: random.randint(1, max_val) for i in range(size)}
    }

    return random_dict
