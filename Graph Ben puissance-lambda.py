import matplotlib.pyplot as plt
import numpy as np


x = [500,790,975,1250,1750,2500]
y = [2.45,7.2,9.425,11.275,13.05,13.215]

def func(x):
    return -1e-12*x**4 + 8e-9*x**3 - 3e-5*x**2 + 0.0423*x - 12.887


plt.scatter(x, y)
plt.plot(np.arange(0, 2500), func(np.arange(0, 2500)))
plt.ylabel("")
plt.xlabel("Longueur d'onde [nm]")
plt.show()