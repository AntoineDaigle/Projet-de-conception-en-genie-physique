"""Classe utilisé pour les unittests. Valide que les fonctions font bien se qu'elles sont supposées faire."""


import unittest
from Triangulation import Triangulation
import numpy as np


class TestTriangulation(unittest.TestCase):
    """Classe permettant de faire des tests unitaires. Ce test permet de valider si les fonctions fabriqué sont valide ou non. Faire attention, les tests ne gèrent peut être pas tout les cas, l'objectif est juste de flag le plus vite possible les erreurs.

    Args:
        unittest (_type_): Instance de classe.
    """

    def test_position_faisceau(self):
        """Test l'intersection des cercles
        """
        Out = Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Position_faisceau((0,0), (6,0), 4, 4)
        self.assertSequenceEqual((round(Out[0],3), round(Out[1], 3)), (3.0, 2.646))

        Out = Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Position_faisceau((0,0), (6,0), 3, 4)
        self.assertSequenceEqual((round(Out[0],3), round(Out[1], 3)), (2.417, 1.778))

        Out = Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Position_faisceau((0,0), (6,0), 4, 7)
        self.assertSequenceEqual((round(Out[0],3), round(Out[1], 3)), (0.25, 3.992))

        Out = Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Position_faisceau((0,0), (6,0), 3, 7)
        self.assertSequenceEqual((round(Out[0],3), round(Out[1], 3)), (-0.333, 2.981))

        Out = Triangulation((1, 2), (6,0), (3,3), 46, 24, 82).Position_faisceau((1,2), (6,0), 4, 4)
        self.assertSequenceEqual((round(Out[0],3), round(Out[1], 3)), (4.599, 3.746))





    def test_distance_capteur_faisceau(self):
        """Test la distance entre le capteur et le faisceau. Make sense?"""
        self.assertAlmostEqual(Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Distance_rayon_a_faisceau(50, 100), 3.625532686983476)

        self.assertAlmostEqual(Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Distance_rayon_a_faisceau(24, 50), 6.630305650971852)

        self.assertAlmostEqual(Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Distance_rayon_a_faisceau(45.796, 400), 6.0861430555152785)


    def test_rayon_max(self):
        """MÉthode qui calcul si le rayon maximum fait du sens."""
        out = round(Triangulation((0,0), (6,0), (3,3), 46, 24, 82).Rayon_max(),3)
        self.assertAlmostEqual(out, round(6+3*np.sqrt(2),3))

        out = round(Triangulation((0,0), (7,0), (3,3), 46, 24, 82).Rayon_max(),3)
        self.assertAlmostEqual(out, round(7+3*np.sqrt(2),3))

        out = round(Triangulation((0,0), (6.4,0), (2,4), 46, 24, 82).Rayon_max(),3)
        self.assertAlmostEqual(out, round(6.4+2*np.sqrt(5),3))





if __name__ == "__main__":
    unittest.main()