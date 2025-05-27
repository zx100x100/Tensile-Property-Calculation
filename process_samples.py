from calculate_properties import calculate_properties
import pandas as pd

df = pd.read_csv('..\DAQ- Crosshead, … - (Timed).csv',header=6,skiprows=[7])
df.head()

###### SAMPLE SIZE ######
width = 6 # mm
thickness = 3 # mm
gauge_length = 25.0 #mm
A = width*thickness # mm^2

stress_data = (df['Load ']/A)*1000.0 # 1000 * kN / mm^2 -> MPa
strain_data = df['Extensometer ']/gauge_length # mm/mm
calculate_properties(stress_data, strain_data)
