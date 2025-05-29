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

# Stress in MPa and strain in mm/mm
def calculate_properties(stress, strain, plot=True, name=''):
    strain_array = np.array(strain)
    stress_array = np.array(stress)

    #Calculate UTS
    UTS_index = np.argmax(stress_array)
    UTS = stress_array[UTS_index]
    UTS_strain = strain_array[UTS_index]

    """ #Plot full stress strain curve
    fig,ax = plt.subplots()
    ax.plot(strain, stress)
    ax.set_xlabel('Strain (mm/mm)')
    ax.set_ylabel('Stress (MPa)')
    ax.set_title('Stress-Strain Curve')

    plt.show() """

    # Find the elastic modulus
    # use stress and strain values from stress=0 to stress= 25% + initial offset of UTS MPa and only at strains < 25% of strain at break
    linear_stress_mask = (stress < (UTS*0.25 + stress[0])) & (stress > 0)
    linear_strain_mask = strain < UTS_strain*0.25
    linear_stress = stress[linear_stress_mask & linear_strain_mask]
    linear_strain = strain[linear_stress_mask & linear_strain_mask]


    linear_regression_output = linregress(linear_strain, linear_stress)
    E = linear_regression_output[0]

    #print(f'The elastic modulus is {round(E/1000.0, 2)} GPa')
    print("test: ")
    print(linear_regression_output)
    print(stress[0])

    # calculate the yield strength. add offset to acount for non-zero stress at start (strain should be zero)
    stress_offset = E*(strain-0.002) + stress[0]
    f = np.array(stress)
    g = np.array(stress_offset)
    yield_stress_index = np.argwhere(np.diff(np.sign(f - g)))[0][0]

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
    Sy_strain, Sy = intersection_point(Ax1,Ay1,Ax2,Ay2,Bx1,By1,Bx2,By2)

    #print(f'The yield strength calculated programmatically is {round(Sy,2)} MPa')

    if(plot):
        fig,ax = plt.subplots()

        ax.plot(strain_array,stress_array) #plot stress vs strain
        ax.plot(linear_strain, linear_stress, 'r')
        ax.plot(strain_array,stress_offset) #plot 2% offset
        ax.plot(Sy_strain,Sy,'go') #Plot yeild point
        ax.plot(UTS_strain, UTS, 'ro') #Plot UTS point

        ax.set_xlabel('Strain (mm/mm)')
        ax.set_ylabel('Stress (MPa)')
        ax.set_title(name + ' Stress-Strain Curve')

        #ax.set_ylim([0,300])
        ax.set_ylim([0,UTS*1.1])
        #ax.set_xlim([0,0.01])

        plt.show()

    elongation = UTS_strain #TODO: does not consider ductile faliure

    return E, Sy, UTS, elongation    
