import numpy as np

max_dinA_i = 11
__dinA_inch = [46.81, 33.11, 23.39, 16.54, 11.69, 8.27, 5.83, 4.13, 2.91, 2.05, 1.46, 1.02]
dinA_inch = {i: (__dinA_inch[i+1], __dinA_inch[i]) for i in range(max_dinA_i)}

inch2cm = 2.54
cm2inch = 1 / inch2cm

limits_dinA = {i: np.array([[0.0, dinA_inch[i][0]],
                            [0.0, dinA_inch[i][1]]]) for i in range(max_dinA_i)}

