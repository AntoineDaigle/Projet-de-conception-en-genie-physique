# Tu commences par définir la position des capteurs, ensuite tu entre dans une boucle while. Dans cette boucle, tu calcul les rayons de chaque thermistances à une température hypothétique maximale ainsi que l'angle avec la position possible. Assume une décroissance exponentielle.


# TODO Vérifier la documentation


from math import log, sqrt
from numpy.linalg import norm
import numpy as np


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
        """Méthode qui calcule la position du faisceau à l'aide de l'intersection de deux cercles. La méthode a été trouvé sur le web. J'assume aucune position pour les capteurs.

        Args:
            Capteur1 (tuple): Position du premier capteur
            Capteur2 (tuple): Position du second capteur
            R1 (float): Rayon du premier capteur utilisé
            R2 (float): Rayon du second capteur utilisé

        Returns:
            tuple: Coordonnée de la position du faisceau
        """
        



        a = 2*(Capteur2[0] - Capteur1[0]) 
        b = 2*(Capteur2[1] - Capteur1[1]) 
        c = (Capteur2[0] - Capteur1[0])**2 + (Capteur2[1] - Capteur1[1])**2 - R2**2 + R1**2
        d = (2*a*c)**2 - 4*(a**2+b**2)*(c**2 - b**2 * R1**2)


        x = Capteur1[0]+(2*a*c + np.sqrt(d))/(2*(a**2 + b**2))

        if b == 0:
            y = Capteur1[1] + np.sqrt(R2**2 - ((2*c - a**2)/(2*a))**2)

        else:
            y = Capteur1[1] + (c-a*(x-Capteur1[0]))/b


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
        while abs(DiffR) > 0.1:

            SAFE +=1

            R1 = self.Distance_rayon_a_faisceau(self.T1, T_max)            
            R2 = self.Distance_rayon_a_faisceau(self.T2, T_max)
            R3 = self.Distance_rayon_a_faisceau(self.T3, T_max)


            

            R_actuel = R1 + R2 + R3

            DiffR = R_actuel - R_max

            if R_actuel > R_max:
                T_max = T_max*0.95

            elif SAFE == 100:
                print("SAFE")
                break

            else:
                T_max = T_max * 1.05

        print("{}\n{}\n{}\n\n".format(R1, R2, R3))
        print("Pos:", self.Position_faisceau(self.C1, self.C2, R1, R2), "temp:", T_max + self.T_amb)

Triangulation((0,0), (6,0), (3,9), 46, 24, 82).Itération_tentative()
# Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Position_faisceau((0,0), (6,0), 4, 4)



    # def Itération(self):
        

    #     T_max = 400     # Température supposé
    #     DiffR3 = 1

    #     while abs(DiffR3) > 0.01:

    #         R1 = self.Distance_rayon_a_faisceau(self.T1, T_max)            
    #         R2 = self.Distance_rayon_a_faisceau(self.T2, T_max)
    #         R3 = self.Distance_rayon_a_faisceau(self.T3, T_max)


    #         Position_suppose = self.Position_faisceau(R1, R2)

    #         Position_R3_suppose = norm([[self.C3[0]- Position_suppose[0]], [self.C3[1]-Position_suppose[1]]])
    #         DiffR3 = R3 - Position_R3_suppose

    #         if Position_R3_suppose < R3:
    #             T_max = T_max*0.97

    #         else:
    #             T_max = T_max *1.03

    #     print("La position calculé est: {} et la température maximale est de {} Celsius".format(Position_R3_suppose, T_max))








# Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Position_faisceau(6,9)
# Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Itération()

# Triangulation(np.array([-5.1961524, -3.0]), np.array([5.1961524, -3.0]), np.array([0.0, 6.0]), 45.796, 23.575, 81.817).Itération()   # Pas valide, car premier capteur pas à (0,0)
