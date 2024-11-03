import pandas as pd

input_file = ['1k', '10k']
output_file = ['10', '100', '1k', '10k', '100k']

for ifile in input_file:
    for ofile in output_file:
        f1 = pd.read_csv(f'data/benchmark/result_{ifile}_{ofile}.csv')
        f2 = pd.read_csv(f'data/benchmark/pred_{ifile}_{ofile}.csv')
        if not f1.equals(f2):
            print(ifile, ofile, "Tables are not identical")
        else:
            print(ifile, ofile, "Tables are identical")