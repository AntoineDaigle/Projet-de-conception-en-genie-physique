import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

Coeffa = []
Coeffb = []
Coeffc = []
Coeffd = []
Coeffe = []
Coefff = []

r = [1, 4, 5, 6]

# for i in r:
df = pd.read_excel(r"C:\Users\antoi\Desktop\Projet-de-conception-en-genie-physique\Python triangulation\Paramètres gaussienne\courbe profil1.xlsx")

x = df["Longueur [m]"]
x = x - min(x)
y = df["Température (Solide) [K]"]


# Define the function to fit a double gaussian function to the data
def func(x, a, b, c, d):
    return a*np.exp(-b*x**c) + d


# Fit the data to the function
# popt, pcov = curve_fit(func, x, y, maxfev=5000)
# print(popt)

# plt.scatter(x, y)
plt.plot(x, func(x, 25, 1, 2, 293))
plt.show()

# Coeffa.append(popt[0])
# Coeffb.append(popt[1])
# Coeffc.append(popt[2])
# Coeffd.append(popt[3])
# Coeffe.append(popt[4])
# Coefff.append(popt[5])


# print("Param:\nCoeffa:{}\nCoeffb:{}\nCoeffc:{}\nCoeffd:{}\nCoeffe:{}\nCoefff:{}".format(np.mean(Coeffa), np.mean(Coeffb), np.mean(Coeffc), np.mean(Coeffd), np.mean(Coeffe), np.mean(Coefff)))






