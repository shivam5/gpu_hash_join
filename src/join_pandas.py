from typing import List, Union
import pandas as pd
from join import TableJoin
import time


class TableJoinPandas(TableJoin):
    def inner_join(self, join_key: Union[str, tuple], return_keys: List[str]) -> tuple[dict, float]:

        t0 = time.time()
        if isinstance(join_key, tuple) and len(join_key) == 2:
            left_key, right_key = join_key
            result = self.table_a.merge(self.table_b, left_on=left_key, right_on=right_key, how='inner')

        elif isinstance(join_key, str):
            result = self.table_a.merge(self.table_b, on=join_key, how='inner')

        else:
            raise TypeError
        t1 = time.time()

        return result[return_keys].to_dict(), t1 - t0