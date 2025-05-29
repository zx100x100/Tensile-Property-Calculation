import pandas as pd
import numpy as np
import pingouin as pg

df = pd.read_excel('../tensile testing.xlsx', 'python stats', header=0, skiprows=[1])

aov = pg.anova(dv='Yeild', between=['Thick', 'Orientation', 'Position'], data=df)
print(aov)