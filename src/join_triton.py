# Wrapper for triton matrix multplication to implement table join lives here.
# TODO: Create a parent class for `TableJoin` and `TableJoinTriton` to abstract out common code.
# and it should be an abstract class. 
from typing import List
import pandas as pd
import utils
from triton_matmul import matmul
import torch
import numpy as np


class TableJoinTriton:
    def __init__(self, table_a: dict | pd.DataFrame | str, table_b: dict | pd.DataFrame | str):
        """
        Args:
            table_a: Table in dictionary implementation
            table_b: Table in dictionary implementation
        Returns:
            None

        We first use dictionaries to emulate tables. The format is:
        ```
        {
            'id': {0:1, 1:2, 2:3, 3:4},
            'name': {0:'foo', 1:'bar', 2:'baz', 3:'qux'},
            ...
        }
        ```
        which follows how pandas DataFrames are dumped.
        """
        if isinstance(table_a, str) and isinstance(table_b, str):
            self.table_a = pd.read_csv(table_a)
            self.table_b = pd.read_csv(table_b)

        elif isinstance(table_a, dict) and isinstance(table_b, dict):
            self.table_a = pd.DataFrame(table_a)
            self.table_b = pd.DataFrame(table_b)

        elif isinstance(table_a, pd.DataFrame) and isinstance(table_b, pd.DataFrame):
            self.table_a = table_a
            self.table_b = table_b
        else:
            raise TypeError

    def inner_join(self, join_key: str | tuple, return_keys: List[str]) -> dict:
        """
        Args:
            join_key: the key to perform inner join, can be tuple for left and right key
            return_key: list of keys that table_c will contain
        Returns:
            table_c: resulting table of inner join(table_a, table_b)

        if single `join_key` must be present in both `table_a` and `table_b` if given as single string

        The equivalent SQL is to this function is:
            ```SELECT return_keys FROM table_a INNER JOIN table_b ON table_a.join_key = table_b.join_key
        """
        if isinstance(join_key, tuple) and len(join_key) == 2:
            raise NotImplementedError

        elif isinstance(join_key, str):
            domain = list(set(self.table_a[join_key].values).union(set(self.table_b[join_key].values)))

            mat_a = utils.d2mat(self.table_a, domain)
            mat_b = utils.d2mat(self.table_b, domain)

            # Convert mat_a, mat_b (np.ndarray) to torch tensors
            # Perform matrix multiplication
            torch_mat_a = torch.tensor(mat_a, dtype=torch.float16, device='cuda')
            torch_mat_b_t = torch.tensor(mat_b.T, dtype=torch.float16, device='cuda')
            result = matmul(torch_mat_a, torch_mat_b_t).cpu().numpy()
            ai, bj = np.nonzero(result)

            result = pd.DataFrame()
            for key in return_keys:
                if key in self.table_a.keys():
                    result[key] = self.table_a[key].iloc[ai].values
                else:
                    result[key] = self.table_b[key].iloc[bj].values

            result.reset_index()

        else:
            raise TypeError

        return result.to_dict()
