from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Union

class TableJoin(ABC):

    def __init__(self, table_a: Union[dict, pd.DataFrame, str], table_b: Union[dict, pd.DataFrame, str]):
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

    @abstractmethod
    def inner_join(self, join_key: Union[str, tuple], return_keys: List[str]) -> tuple[dict, float]:
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
        print("This is an abstract method. Implementation not found.")

    # @abstractmethod
    def left_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError

    # @abstractmethod
    def right_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError

    # @abstractmethod
    def full_outer_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError

    # @abstractmethod
    def cross_join(self) -> dict:
        """
        Args:
        Returns:
        """
        raise NotImplementedError