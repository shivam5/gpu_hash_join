import pandas as pd

input_file = ['1k', '10k']
output_file = ['10', '100', '1k', '10k', '100k']

for ifile in input_file:
    for ofile in output_file:
        f1 = pd.read_csv(f'../data/result_{ifile}_{ofile}.csv')
        f2 = pd.read_csv(f'../data/pred_table1M_id{ofile}_{ifile}.csv')
        if not f1.equals(f2):
            print(ifile, ofile, "Tables are not identical")
        else:
            print(ifile, ofile, "Tables are identical")