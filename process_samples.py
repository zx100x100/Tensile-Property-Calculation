from unicodedata import name
from calculate_properties import calculate_properties
import pandas as pd
import numpy as np
from glob import glob

gauge_length = 25.0 #mm

sample_file = pd.read_excel('../tensile testing.xlsx', 'for python', header=0, skiprows=[1])

#janky but try writing to the file now to make sure it isn't open
sample_file.to_excel('../tensile testing python results.xlsx')

sample_file['E'] = np.zeros(len(sample_file))
sample_file['Yeild'] = np.zeros(len(sample_file))
sample_file['UTS'] = np.zeros(len(sample_file))
sample_file['elongation'] = np.zeros(len(sample_file))

for index, row in sample_file.iterrows():
    name = row['Name']
    print('Processing ', name, ' . . .')

    filepath = glob('../Test Data/*'+ str(name) + '/*.csv', recursive=True)[0]
    print(filepath)
    test_data = pd.read_csv(filepath,header=6,skiprows=[7])

    area = row['Area'] # mm^2

    stress_data = (test_data['Load ']/area)*1000.0 # 1000 * kN / mm^2 -> MPa
    strain_data = test_data['Extensometer ']/gauge_length # mm/mm
    E, Sy, UTS, elongation = calculate_properties(stress_data, strain_data, plot=False)

    print(f'The elastic modulus is {round(E/1000.0, 2)} GPa')
    print(f'The yield strength is {round(Sy, 2)} MPa')
    print(f'The ultimate tensile strength is {round(UTS, 2)} MPa')
    print(f'The elongation at break is {round(elongation, 3)}')

    sample_file.loc[index, 'E'] = E
    sample_file.loc[index, 'Yeild'] = Sy
    sample_file.loc[index, 'UTS'] = UTS
    sample_file.loc[index, 'elongation'] = elongation

sample_file.to_excel('../tensile testing python results.xlsx')