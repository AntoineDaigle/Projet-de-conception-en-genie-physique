import Triangulation as Tr
from matplotlib.pyplot import *
from Data_feed import ReadDATA
from seaborn import *
import pandas as pd
import numpy as np



Therms = ReadDATA(r"Python triangulation\Data de tests\Test MAPA 21 avril\Mesure 1.lvm")


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

Power = []

for i in df["T_max"]:
    Power.append(Puissance(i, 793))

df["Puissance"] = Power



# def Rapport(l):

#     NormT = df["T_max"]/max(df["T_max"])  
#     NormP = df["Puissance"]/max(df["Puissance"])

#     xrange = range(len(NormP))

#     plot(xrange, NormP, label="Puissance normalisé")
#     plot(xrange, NormT, label="Température normalisé")
#     xlabel("Mesure")
#     legend()
#     savefig(r"Python triangulation\Data de tests\FIGURE\ExamenChaleur RAPPORT.png", dpi=600)
#     show()


# Rapport(l=793)

# def TempAndPower():

#     fig, ax = subplots(1, 2)
#     ax[0].plot(df["T_max"], label="Température maximale")
#     ax[1].plot(df["Puissance"], label="Puissance")
#     ax[1].legend()
#     ax[0].legend()
#     show()

# TempAndPower()




# y = df["T_max"]

# def PredTemp():
#     T_pred = []
#     itera = []

#     for j in range(0, int(len(t_ech1))-2):
#         y_p_1 = (y[j+2]-y[j+1])/0.21
#         y_p_0 = (y[j+1]-y[j])/0.21
#         tau = -(0.21)/np.log(y_p_1/y_p_0)
#         z1 = (y_p_0*tau) + y[j]
#         #print(tau)
#         itera.append(j*0.21)
#         T_pred.append(z1)
#         #print('\n')
#     return T_pred, itera

# y_p_1 = (y[48]-y[47])/0.21
# y_p_0 = (y[47]-y[46])/0.21
# tau = -(0.21)/np.log(y_p_1/y_p_0)
# z1 = (y_p_0*tau) + y[1]
# print(y_p_0)
# print(y_p_1)
# print(tau)
# print(z1)
# # itera.append(j*0.21)
# # T_pred.append(z1)
# print('\n')


# T_pred, itera=PredTemp()
# scatter(itera, T_pred, label="Tpred")
# plot(t_ech1, df["T_max"], color="red", label="Tmax")
# legend()
# show()

# PowerPred = []

# for i in T_pred:
#     PowerPred.append(Puissance(i, 793))

# df["Puissance Pred"] = PowerPred

def CreateDF(l):
    # fig, ax = subplots(3, figsize=(9, 6))

    x = [i*0.21 for i in range(len(df["T_max"]))]

    fig, ax = subplots()
    # histplot(x=df["PosX"], y=df["PosY"], cbar=True)#, ax=ax[0]
    # ax.set_xlim(0,4.846)
    # ax.set_ylim(-2.423,2.423)
    # axhline(0)
    # axvline(2.423)
    
    # # histplot(df["PosY"], ax=ax[1])
    # ax[1].plot(x, df["T_max"])
    # ax[1].set(ylabel=r"Température [$^\circ$C]", xlabel="Mesure")

    # ax[2].plot(x, Puissance(df["T_max"], l))
    # ax[2].set(ylabel=r"Puissance [W]", xlabel="Mesure")

    plot(x, df["Puissance"], label="Puissance")
    plot([0,30, 30, 53, 53, 80, 80, 105, 105, 130, 130, 157, 157, 182,182,205,205,231,231,256,256,282,282,307,307,320,], [0,0,2,2, 3.7,3.7, 5.4, 5.4, 7.05, 7.05, 8.75, 8.75, 9.6, 9.6, 8.75, 8.75, 7.05, 7.05,5.4, 5.4, 3.7,3.7,2,2,0,0], label="Échellon")
    xlabel("Temps [s]")
    ylabel("Puissance [W]")

    tight_layout()
    savefig(r"Python triangulation\Data de tests\FIGURE\Mesure 1 POWER.png", dpi=800)
    show()


CreateDF(793)