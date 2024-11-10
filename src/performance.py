from utils import generate_random_dict
import pandas as pd
import join_triton as jt
import join_pandas as jp
import join_torch as jtch
import os
from typing import List, Optional
import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run join benchmark comparing Triton and Pandas implementations.')

    # Default values
    default_N1 = [
        'data/table1M_id10',
        'data/table1M_id100',
        'data/table1M_id1k',
        'data/table1M_id10k',
        'data/table1M_id100k'
    ]

    default_N2 = [
        'data/table1k',
        'data/table10k'
    ]

    # N1 arguments
    parser.add_argument('--N1', nargs='+', type=str,
                      default=default_N1,
                      help='List of paths for first set of tables')

    # N2 arguments
    parser.add_argument('--N2', nargs='+', type=str,
                      default=default_N2,
                      help='List of paths for second set of tables')

    # Data directory
    parser.add_argument('--data-dir', type=str, default='data',
                      help='Directory to store/read data files. Default: "data"')

    args = parser.parse_args()

    # Print received arguments for debugging
    print(f"Received arguments:")
    print(f"N1: {args.N1}")
    print(f"N2: {args.N2}")
    print(f"data_dir: {args.data_dir}")

    return args


def get_table_config(table_name: str) -> tuple:
    """Get size and max_id configuration for a given table name."""
    configs = {
        'table1M_id10':   (1000000, 10),
        'table1M_id100':  (1000000, 100),
        'table1M_id1k':   (1000000, 1000),
        'table1M_id10k':  (1000000, 10000),
        'table1M_id100k': (1000000, 100000),
        'table1k':  (1000, 1000),
        'table10k': (10000, 1000)
    }

    # Extract base name without path and extension
    base_name = os.path.basename(table_name).split('.')[0]

    if base_name in configs:
        return configs[base_name]
    else:
        raise ValueError(f"Unknown table configuration for {table_name}")


def run_join_benchmark(N1: List[str], N2: List[str], data_dir: str = 'data') -> List[dict]:
    """
    Run join benchmark comparing Triton and Pandas implementations.

    Args:
        N1: List of paths for first set of tables
        N2: List of paths for second set of tables
        data_dir: Directory to store/read data files

    Returns:
        List of dictionaries containing benchmark results
    """
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    results = []
    T1 = []
    T2 = []

    # Process first set of tables
    for name in N1:
        csv_path = f"{name}.csv"
        if not os.path.exists(csv_path):
            print(f'Generating data for {name}')
            size, max_id = get_table_config(name)
            table = generate_random_dict(size, max_id, value_key='v1')
            pd.DataFrame(table).to_csv(csv_path)
            T1.append(table)
        else:
            print(f'Loading pre-generated data for {name}')
            T1.append(pd.read_csv(csv_path).to_dict())

    # Process second set of tables
    for name in N2:
        csv_path = f"{name}.csv"
        if not os.path.exists(csv_path):
            print(f'Generating data for {name}')
            size, max_id = get_table_config(name)
            table = generate_random_dict(size, max_id, value_key='v2')
            pd.DataFrame(table).to_csv(csv_path)
            T2.append(table)
        else:
            print(f'Loading pre-generated data for {name}')
            T2.append(pd.read_csv(csv_path).to_dict())

    # Run benchmarks
    for name1, table1 in zip(N1, T1):
        for name2, table2 in zip(N2, T2):
            print(f'\nJOIN {name1} {name2}')

            # Triton join
            table_join_triton = jt.TableJoinTriton(table1, table2)
            result_triton, triton_time = table_join_triton.inner_join('id', ['id', 'v1', 'v2'])
            print('triton matmul:', triton_time)

            # Pytorch join, just for kernel profiling
            table_join_pytorch = jtch.TableJoinPytorch(table1, table2)
            result_pytorch, torch_time = table_join_pytorch.inner_join('id', ['id', 'v1', 'v2'])
            print('pytorch matmul:', torch_time)

            assert result_triton == result_pytorch

            # Pandas join
            table_join_pandas = jp.TableJoinPandas(table1, table2)
            result_pandas, pandas_time = table_join_pandas.inner_join('id', ['id', 'v1', 'v2'])
            print('pandas join:', pandas_time)

            # Verify results match
            assert result_triton == result_pandas

            # Store results
            results.append({
                'table1': name1,
                'table2': name2,
                'triton_time': triton_time,
                'pandas_time': pandas_time
            })

    return results


if __name__ == '__main__':
    # Parse command line arguments
    args = parse_args()

    os.environ['TRITON_PRINT_AUTOTUNING'] = '1'

    # Run benchmark
    results = run_join_benchmark(args.N1, args.N2, args.data_dir)

    # Print final results summary
    print("\nBenchmark Results Summary:")
    print("-" * 80)
    print(f"{'Table 1':<30} {'Table 2':<20} {'Triton (s)':<12} {'Pandas (s)':<12} {'Speedup':<10}")
    print("-" * 80)
    for result in results:
        speedup = result['pandas_time'] / result['triton_time']
        print(f"{os.path.basename(result['table1']):<30} "
              f"{os.path.basename(result['table2']):<20} "
              f"{result['triton_time']:<12.4f} "
              f"{result['pandas_time']:<12.4f} "
              f"{speedup:<10.2f}x")