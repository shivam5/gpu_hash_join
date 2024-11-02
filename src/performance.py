from utils import generate_random_dict
import pandas as pd
import time
import join_triton as jt
import join_pandas as jp
import os


N1 = ['data/table1M_id10', 'data/table1M_id100', 'data/table1M_id1k', 'data/table1M_id10k', 'data/table1M_id100k']
N2 = ['data/table1k', 'data/table10k']

name = N1[0]+'.csv'
print(f"Check if {name} exists. If not, generate data.")
if not os.path.exists(name):
    print('Generate data!')
    table1M_id10 = generate_random_dict(1000000, 10, value_key='v1')
    table1M_id100 = generate_random_dict(1000000, 100, value_key='v1')
    table1M_id1k = generate_random_dict(1000000, 1000, value_key='v1')
    table1M_id10k = generate_random_dict(1000000, 10000, value_key='v1')
    table1M_id100k = generate_random_dict(1000000, 10000, value_key='v1')

    table1k = generate_random_dict(1000, 1000, value_key='v2')
    table10k = generate_random_dict(1000, 1000, value_key='v2')

    T1 = [table1M_id10, table1M_id100, table1M_id1k, table1M_id10k, table1M_id100k]
    T2 = [table1k, table10k]

    for name, table in zip(N1, T1):
        pd.DataFrame(table).to_csv(name+'.csv')

    for name, table in zip(N2, T2):
        pd.DataFrame(table).to_csv(name+'.csv')
else:
    print('Use pre-generated data!')
    T1 = []
    T2 = []
    for name in N1:
        T1.append(pd.read_csv(name+'.csv').to_dict())
    for name in N2:
        T2.append(pd.read_csv(name+'.csv').to_dict())

for name1, table1 in zip(N1, T1):
    for name2, table2 in zip(N2, T2):
        print('JOIN', name1, name2)

        table_join_triton = jt.TableJoinTriton(table1, table2)

        t0 = time.time()
        result_triton = table_join_triton.inner_join('id', ['id', 'v1', 'v2'])
        t1 = time.time()

        print('triton matmul:', t1 - t0)

        table_join_pandas = jp.TableJoinPandas(table1, table2)
        t0 = time.time()
        result_pandas = table_join_pandas.inner_join('id', ['id', 'v1', 'v2'])
        t1 = time.time()

        print('pandas join:', t1 - t0)
        print('')

        assert result_triton == result_pandas
