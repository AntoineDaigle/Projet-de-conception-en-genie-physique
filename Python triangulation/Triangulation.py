# Tu commences par définir la position des capteurs, ensuite tu entre dans une boucle while. Dans cette boucle, tu calcul les rayons de chaque thermistances à une température hypothétique maximale ainsi que l'angle avec la position possible. Assume une décroissance exponentielle.


# TODO Vérifier la documentation


from math import log
from numpy.linalg import norm
import numpy as np
import matplotlib.pyplot as plt


class Triangulation:

    def __init__(self, C1:tuple, C2:tuple, C3:tuple, T1:float, T2:float, T3:float) -> None:
        """Classe permettant de calculer par triangulation la position du faisceau ainsi que sa température. Cette classe est inspiré du code de l'équipe Cocotte-puissance.

        Args:
            C1 (tuple): Coordonné du premier capteur (x,y).
            C2 (tuple): Coordonné du deuxième capteur (x,y).
            C3 (tuple): Coordonné du troisième capteur (x,y).
            T1 (float): Température du premier capteur en Celsius.
            T2 (float): Température du deuxième capteur en Celsius.
            T3 (float): Température du troisième capteur en Celsius.
        """

        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.T1 = T1
        self.T2 = T2
        self.T3 = T3

        self.T_amb = 22     # Température ambiante supposée [Celsius]



    def Distance_rayon_a_faisceau(self, T_capteur:float, T_max:float, Coeff1:float = 0.17586509, Coeff2:float = 1.53679005) -> float:
        """Méthode qui calcul la distance entre un capteur et la position du faisceau. 
            T_{capteur} = T_{max} e^{-Coeff1 r^{Coeff2}} + T_{amb}
        Les coefficients sont trouvées à l'aide de la simulation thermique.

        Args:
            T_capteur (float): Température du capteur en celsius.
            T_max (float): Température supposé du faisceau à son maximum.
            Coeff1 (float, optional): Premier coefficient de la décroissance exponentielle. Defaults to 1.
            Coeff2 (float, optional): Deuxième coefficient de la décroissance exponentielle. Defaults to 2.

        Returns:
            float: Distance entre le capteur et le faisceau.
        """
        return (log((T_capteur - self.T_amb)/T_max) / -Coeff1)**(1/Coeff2)





    def Position_faisceau(self, Capteur1:tuple, Capteur2:tuple, R1:float, R2:float) -> tuple:
        """Méthode qui calcule la position du faisceau à l'aide de l'intersection de deux cercles. La méthode a été trouvé sur le web. J'assume aucune position pour les capteurs. Cependant, il est toujours supposé avoir une intersection entre les cercles.

        Args:
            Capteur1 (tuple): Position du premier capteur
            Capteur2 (tuple): Position du second capteur
            R1 (float): Rayon du premier capteur utilisé
            R2 (float): Rayon du second capteur utilisé

        Returns:
            tuple: Coordonnée de la position du faisceau
        """
        


        # Paramètre à calculer
        a = 2*(Capteur2[0] - Capteur1[0]) 
        b = 2*(Capteur2[1] - Capteur1[1]) 
        c = (Capteur2[0] - Capteur1[0])**2 + (Capteur2[1] - Capteur1[1])**2 - R2**2 + R1**2
        d = (2*a*c)**2 - 4*(a**2+b**2)*(c**2 - b**2 * R1**2)



        if b == 0:
            X1 = Capteur1[0]+(2*a*c + np.sqrt(d))/(2*(a**2 + b**2))
            x=X1
            
            Y1 = Capteur1[1] + np.sqrt(R2**2 - ((2*c - a**2)/(2*a))**2)
            Y2 = Capteur1[1] - np.sqrt(R2**2 - ((2*c - a**2)/(2*a))**2)

            assert X1 > 0 , "Attention la distance en X n'est pas positive"

            if Y1 > 0:

                y = Y1
                x = X1
            else:
                assert Y2 > 0, "Attention, aucune coord en Y n'est positive"
                y=Y2
                x = X1

        else:
            X1 = Capteur1[0]+(2*a*c + np.sqrt(d))/(2*(a**2 + b**2))
            X2 = Capteur1[0]+(2*a*c - np.sqrt(d))/(2*(a**2 + b**2))

            Y1 = Capteur1[1] + (c-a*(X1-Capteur1[0]))/b
            Y2 = Capteur1[1] + (c-a*(X2-Capteur1[0]))/b

            if X1 < 0 or Y1 < 0:
                assert Y2 > 0 and X2 > 0, "Attention, une des coordonnées sélectionnées n'est pas positive."
                y=Y2
                x=X2
            else:
                y=Y1
                x=X1

        return x, y




    def Rayon_max(self) -> float:
        """Méthode qui calcule le rayon maximal maximum possible.

        Returns:
            float: Rayon maximal possible
        """

        Distance_1_2 = norm(self.C2)
        Distance_1_3 = norm(self.C3)

        return Distance_1_2 + Distance_1_3



    def Itération_tentative(self):
        """Méthode qui calcul de manière itérative la position du faisceau. C'est cette méthode qui est la plus critique. Je sais pas trop comment l'arranger
        """


        T_max = 300

        DiffR = 1

        R_max = self.Rayon_max()

        SAFE=1


        while abs(DiffR) > 0.001:

            SAFE +=1

            R1 = self.Distance_rayon_a_faisceau(self.T1, T_max)            
            R2 = self.Distance_rayon_a_faisceau(self.T2, T_max)
            R3 = self.Distance_rayon_a_faisceau(self.T3, T_max)



            R_actuel = R1 + R2 + R3

            DiffR = R_actuel - R_max

            if R_actuel > R_max:
                T_max = T_max*0.95

            elif SAFE == 1000:
                print("SAFE")
                break

            else:
                T_max = T_max * 1.05

        PositionFinale = self.Position_faisceau(self.C1, self.C2, R1, R2)

        print("­\n- - RESULTS - -\n")
        print("\tRayon 1: {}\n\tRayon 2: {}\n\tRayon 3: {}\n".format(R1, R2, R3))
        print("\tPosition: ({}, {})\n\tTempérature: {} C\n".format(round(PositionFinale[0], 4), round(PositionFinale[1], 4), round(T_max + self.T_amb, 2)))

        return self.C1, self.C2, self.C3, R1, R2, R3, PositionFinale


def PLOT():
    figure, axes = plt.figure(), plt.gca()

    Cir1 = plt.Circle(C1, R1, color="b", fill=False)
    Cir2 = plt.Circle(C2, R2, color="r", fill=False)
    Cir3 = plt.Circle(C3, R3, color="g", fill=False)

    axes.add_patch(Cir1)
    axes.add_patch(Cir2)
    axes.add_patch(Cir3)
    plt.scatter([C1[0], C2[0], C3[0]], [C1[1], C2[1], C3[1]], color="black")
    plt.scatter([Pos[0]], [Pos[1]], color="fuchsia", edgecolors= 'k', s= 150)
    plt.axhline(0, c="black")
    plt.axvline(0, c="black")
    plt.axis('scaled')
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # C1, C2, C3, R1, R2, R3, Pos = Triangulation((0,0), (6,0), (3,9), 46, 35, 82).Itération_tentative()
    C1, C2, C3, R1, R2, R3, Pos = Triangulation((0,0), (6,0), (3,9), 30, 40, 70).Itération_tentative()
    # C1, C2, C3, R1, R2, R3, Pos =Triangulation((0,0), (6,0), (3,9), 45 ,50, 35).Itération_tentative()
    # Triangulation(np.array([0, 0]), np.array([5.1961524*2, 0]), np.array([5.1961524, 9.0]), 45.796, 23.575, 81.817).Itération_tentative()   # Pas valide, car premier capteur pas à (0,0)
    PLOT()

