import pandas as pd

input_file = ['1k', '10k']
output_file = ['10', '100', '1k', '10k', '100k']

for ifile in input_file:
    for ofile in output_file:
        d1 = pd.read_csv(f'../data/table{ifile}.csv')
        d2 = pd.read_csv(f'../data/table1M_id{ofile}.csv')
        d_result = pd.merge(d1.iloc[:, 1:], d2.iloc[:, 1:], on='id', how='inner')
        d_sorted = d_result.sort_values(by=['id', 'v2', 'v1'], ascending=[True, True, True])
        d_sorted.to_csv(f'../data/result_{ifile}_{ofile}.csv', index=False)