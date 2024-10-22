# Wrapper for triton matrix multplication to implement table join lives here.
# TODO: Create a parent class for `TableJoin` and `TableJoinTriton` to abstract out common code.
# and it should be an abstract class. 

from typing import List
import pandas as pd


class TableJoin:
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
            left_key, right_key = join_key
            

        elif isinstance(join_key, str):
            left_key = right_key = join_key

        else:
            raise TypeError
        
        # result = self.table_a.merge(self.table_b, left_on=left_key, right_on=right_key, how='inner')
        # Rewrite this in terms of triton matrix multiplication

        return result[return_keys].to_dict()

    def left_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError

    def right_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError

    def full_outer_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError

    def cross_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError
