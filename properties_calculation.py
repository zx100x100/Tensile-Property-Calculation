#   Based on: https://professorkazarinoff.github.io/Engineering-Materials-Programming/07-Mechanical-Properties/calculate-yield-strength-programmatically.html

#  imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


#calculates the intersection of two lines defined by 4 points
def intersection_point(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    d = (By2-By1)*(Ax2-Ax1)-(Bx2-Bx1)*(Ay2-Ay1)
    if d:
        uA = ((Bx2-Bx1)*(Ay1-By1)-(By2-By1)*(Ax1-Bx1))/d
        uB = ((Ax2-Ax1)*(Ay1-By1)-(Ay2-Ay1)*(Ax1-Bx1))/d
    else:
        return None
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return None
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)
    
    return x, y

df = pd.read_csv('DAQ- Crosshead, … - (Timed).csv',header=6,skiprows=[7])
df.head()

#print(df_al)

###### SAMPLE SIZE ######
width = 6 # mm
thickness = 3 # mm
gauge_length = 25.0 #mm
A = width*thickness # mm^2

stress_data = (df['Load ']/A)*1000.0 # 1000 * kN / mm^2 -> MPa
strain_data = df['Extensometer ']/gauge_length # mm/mm


def calculate_properties(stress, strain):
    #Plot full stress strain curve
    fig,ax = plt.subplots()
    ax.plot(strain, stress)
    ax.set_xlabel('Strain (mm/mm)')
    ax.set_ylabel('Stress (MPa)')
    ax.set_title('Stress-Strain Curve')

    plt.show()

    # Find the elastic modulus
    # use stress and strain values from stress=0 to stress=150 MPa
    linear_stress_mask = (stress < 100) & (stress > 0)
    linear_strain_mask = strain < 0.02
    linear_stress = stress[linear_stress_mask & linear_strain_mask]
    linear_strain = strain[linear_stress_mask & linear_strain_mask]
    print(linear_strain_mask)


    linear_regression_output = linregress(linear_strain, linear_stress)
    E = linear_regression_output[0]

    print(f'The elastic modulus is {round(E/1000.0, 2)} GPa')

    # calculate the yield strength
    stress_offset = E*(strain-0.002)

    fig, ax = plt.subplots()

    ax.plot(strain,stress,strain,stress_offset)
    ax.set_title('Inset of elastic region')
    ax.set_xlabel('Strain (mm/mm)')
    ax.set_ylabel('Stress (MPa)')
    ax.set_ylim([0,300])
    ax.set_xlim([0,0.01])

    plt.show()

    #calculate yeild strength programatically
    f = np.array(stress)
    g = np.array(stress_offset)
    yield_stress_index = np.argwhere(np.diff(np.sign(f - g)))[0][0]
    yield_strength = stress[yield_stress_index]

    #fig, ax = plt.subplots()

    #ax.plot(strain,stress)
    #ax.plot(strain, stress_offset)
    #ax.plot(strain[yield_stress_index],yield_strength,'go')

    #ax.set_ylim([0,300])
    #ax.set_xlim([0,0.01])

    #plt.show()

    #print(f'The yield strength found programatically is {round(yield_strength,2)} MPa')


    strain_array = np.array(strain)
    stress_array = np.array(stress)

    #calculate yeild strength using the intersection function
    first = yield_stress_index
    second = first + 1
    # A points from the stress strain curve
    Ax1 = strain_array[first]
    Ay1 = stress_array[first]
    Ax2 = strain_array[second]
    Ay2 = stress_array[second]
    # B points from the offset line
    Bx1 = strain_array[first]
    By1 = stress_offset[first]
    Bx2 = strain_array[second]
    By2 = stress_offset[second]

    # run our function that finds the intersection point
    x, Sy = intersection_point(Ax1,Ay1,Ax2,Ay2,Bx1,By1,Bx2,By2)

    #print(x,y)

    fig,ax = plt.subplots()


    ax.plot(strain_array,stress_array)
    ax.plot(strain_array,stress_offset)
    ax.plot(x,Sy,'go')

    ax.set_ylim([0,300])
    ax.set_xlim([0,0.01])

    plt.show()

    print(f'The yield strength calculated programmatically is {round(Sy,2)} MPa')

    UTS = 0
    elongation = 0

    return E, Sy, UTS, elongation    


calculate_properties(stress_data, strain_data)