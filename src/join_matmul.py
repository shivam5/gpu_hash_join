from abc import ABC, abstractmethod
from typing import List, Union
import pandas as pd
import utils
from join import TableJoin
import numpy as np

class TableJoinMatmul(TableJoin):

    @abstractmethod
    def matmul(self, mat_a : np.ndarray, mat_b : np.ndarray) -> np.ndarray:
        print("This is an abstract method. Implementation not found.")

    def inner_join(self, join_key: Union[str, tuple], return_keys: List[str]) -> dict:
        if isinstance(join_key, tuple) and len(join_key) == 2:
            raise NotImplementedError

        elif isinstance(join_key, str):
            domain = list(set(self.table_a[join_key].values).union(set(self.table_b[join_key].values)))

            mat_a = utils.d2mat(self.table_a, join_key, domain)
            mat_b = utils.d2mat(self.table_b, join_key, domain)

            mult = self.matmul(mat_a, mat_b.T)
            ai, bj = np.nonzero(mult)

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
