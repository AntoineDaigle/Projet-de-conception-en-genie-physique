"""Cette classe est le code de cocotte puissance, mais transformée en classe et mieux documenté. Il s'agit de ma tentative de l'améliorer directement à l'aide de leur méthode. Attention à la température ambiante.
"""
from math import log, acos, sin, cos
import numpy as np


class Triangulation_cocotte:

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



    def Angle(self, Rayon1:float, Rayon2:float) -> float:
        """Méthode qui retourne l'angle entre le premier capteur et le faisceau en formant un triangle à l'aide de deuxième capteur. La démonstratio

        Args:
            Rayon1 (float): Distance entre le faisceau et le premier capteur, calculé selon la méthode Distance_rayon_a_faisceau.
            Rayon2 (float): Distance entre le faisceau et le deuxième capteur, calculé selon la méthode Distance_rayon_a_faisceau.

        Returns:
            float: Angle entre le capteur 1 et le centre du faisceau.
        """

        Distance_C1_C2 = abs(self.C1[0] - self.C2[0])   # Distance physique entre les deux capteurs

        return acos((Rayon2**2 - Rayon1**2 - (Distance_C1_C2)**2)/(-2*Distance_C1_C2*Rayon1))

        


    def Conversion(self, Rayon:float, Theta:float):
        """Méthode qui permet de faire la conversion en coordonné cartésienne

        Args:
            Rayon (float): Rayon calculé
            Theta (float): Angle

        Returns:
            np.array: Coordonnés de la position
        """

        x = Rayon * cos(Theta)
        y = Rayon * sin(Theta)

        return np.array([x, y])


    def Itération(self):

        # C'est le bout le plus wack, tu calculs tes rayons selon une température supposé (init à 400) et ensuite tu regarde si ca fit avec les rayons. Ensuite tu fais un ajustement sur l'hypothèse de départ and again until la différence entre calculé et mesuré est minime.

        T_max = 400
        Delta_R3 = 1


        while abs(Delta_R3) > 0.01:

            R1 = self.Distance_rayon_a_faisceau(self.T1, T_max)
            R2 = self.Distance_rayon_a_faisceau(self.T2, T_max)
            R3 = self.Distance_rayon_a_faisceau(self.T3, T_max)


            Guessed_Theta = self.Angle(R1, R2)
            Guessed_Pos = self.C1 + self.Conversion(R1, Guessed_Theta)


            Guessed_R3 = np.linalg.norm(self.C3 - Guessed_Pos)
            Delta_R3 = R3 - Guessed_R3


            if Guessed_R3 < R3:
                T_max = T_max *0.9
            elif Guessed_R3 > R3:
                T_max = T_max *1.10

        print(Guessed_Pos, T_max+self.T_amb)



Triangulation_cocotte(np.array([-5.1961524, -3.0]), np.array([5.1961524, -3.0]), np.array([0.0, 6.0]), 45.796, 23.575, 81.817).Itération()

# print(Triangulation_cocotte(np.array([-5.1961524, -3.0]), np.array([5.1961524, -3.0]), np.array([0.0, 6.0]), 45.796, 23.575, 81.817).Distance_rayon_a_faisceau(45.796, 400))
