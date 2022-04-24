import Triangulation as Tr
from matplotlib.pyplot import *
from Data_feed import ReadDATA
from seaborn import *
import pandas as pd



Therms = ReadDATA(r"Python triangulation\Data de tests\Échec monumental\ExamenChaleur.lvm")



PosX = []
PosY = []
T_max = []

for i in Therms:

    # Get the data

    liste = list(i)

    Raw = Tr.Triangulation((0,0), (4.846,0), (2.423,2.423), (2.423,-2.423), liste[0],liste[1], liste[2], liste[3]).Itération_tentative()

    if Raw[-1] == 4:
        Pos = (Raw[7][0], -1*Raw[7][1])
    else:
        Pos = (Raw[7][0], Raw[7][1])

    PosX.append(Pos[0])
    PosY.append(Pos[1])
    T_max.append(Raw[9])


d = {"PosX": PosX, "PosY": PosY, "T_max": T_max}
df = pd.DataFrame(data=d)

def Puissance(T_max, l):
    a = (-1e-12)*l**4 + (8e-9)*l**3 - (3e-5)*l**2 + 0.0423*l - 12.887
    return (T_max-21.9)/a

def Rapport():

    NormT = df["T_max"]/max(df["T_max"])

    Power = []

    for i in df["T_max"]:
        Power.append(Puissance(i, 793))

    df["Puissance"] = Power

    NormP = df["Puissance"]/max(df["Puissance"])
    # print(NormT)

    xrange = range(len(NormP))

    plot(xrange, NormP, label="Puissance normalisé")
    plot(xrange, NormT, label="Température normalisé")
    xlabel("Mesure")
    legend()
    savefig(r"Python triangulation\Data de tests\FIGURE\ExamenChaleur RAPPORT.png", dpi=600)
    show()


Rapport()






def CreateDF(l):
    fig, ax = subplots(4)

    x = range(len(df["T_max"]))

    histplot(df["PosX"], ax=ax[0])
    histplot(df["PosY"], ax=ax[1])
    ax[2].plot(x, df["T_max"])
    ax[2].set(ylabel=r"Température [$^\circ$C]", xlabel="Mesure")

    ax[3].plot(x, Puissance(df["T_max"], l))
    ax[3].set(ylabel=r"Puissance [W]", xlabel="Mesure")

    tight_layout()
    # savefig(r"Python triangulation\Data de tests\FIGURE\Mesure 3.png", dpi=600)
    show()


# CreateDF(793)