import random
import pandas as pd
import numpy as np


def generate_random_dict(size=100, max_id=10, max_val=100, seed=42, value_key='value'):
    """
    Generates a dictionary with 'id' and 'name' keys. Each key maps to a dictionary where the
    keys are consecutive integers starting from 0 and the values are random integers.

    Args:
        size: The number of entries to generate.
        max_id: Maximum ID for generated values for key `id`
        max_val: Maximum ID for generated values for `value`
        seed: Random seed
        value_key: key for value given as string
    Returns:
        random_dict: A dictionary with the given format.
    """
    random.seed(seed)

    random_dict = {
        'id': {i: random.randint(1, max_id) for i in range(size)},
        value_key: {i: random.randint(1, max_val) for i in range(size)}
    }

    return random_dict

def d2mat(table: pd.DataFrame | dict, join_key: str, domain: list) -> np.ndarray:
    """
    Args:
        table: Table in dictionary or pandas DataFrame
        join_key: Key used for join given as a string
        domain: Domain of the key represented as a list
    Returns:
        matrix: Matrix representation of table id.

    Returns the matrix representation of index given the table and domain of id.
    If python dictionary is used, the format is:
    ```
    {
        'id': {0:1, 1:2, 2:3, 3:4},
        'name': {0:'foo', 1:'bar', 2:'baz', 3:'qux'},
        ...
    }
    ```
    which follows how pandas DataFrames are dumped.
    """
    if isinstance(table, dict):
        ids = list(table[join_key].values())
    elif isinstance(table, pd.DataFrame):
        ids = list(table[join_key].values)

    rows = len(ids)
    cols = len(domain)
    matrix = np.zeros((rows, cols))

    for i, id_value in enumerate(ids):
        if id_value in domain:
            col_index = domain.index(id_value)
            matrix[i][col_index] = 1

    return matrix.astype(np.int8)
