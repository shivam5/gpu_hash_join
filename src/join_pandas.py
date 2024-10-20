from typing import List
import pandas as pd

class TableJoin:
    def __init__(self, table_a: dict, table_b: dict):
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
        self.table_a = pd.DataFrame(table_a)
        self.table_b = pd.DataFrame(table_b)

    def inner_join(self, join_key: str, return_keys: List[str]) -> dict:
        """
        Args:
            join_key: the key to perform inner join
            return_key: list of keys that table_c will contain
        Returns:
            table_c: resulting table of inner join(table_a, table_b)

        `join_key` must be present in both `table_a` and `table_b`.

        The equivalent SQL is to this function is:
            ```SELECT return_keys FROM table_a INNER JOIN table_b ON table_a.join_key = table_b.join_key
        """

        result = self.table_a.merge(self.table_b, on=join_key, how='inner')
        result = result[return_keys]

        return result.to_dict()

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