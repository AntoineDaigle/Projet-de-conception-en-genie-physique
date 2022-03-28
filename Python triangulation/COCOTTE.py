"""Code original de cocotte puissance. 
"""

import numpy

def find_r_i(T_max, T_capteur, alpha=0.17586509, n=1.53679005 , T_ambiant=21.1788):#21.1788
    """
    :param T_max: Température maximale au centre du faisceau
    :param T_capteur: Température du capteur i
    :param alpha: Coefficient obtenu grace à la regression
    :param n: Coefficient obtenu grace à la regression
    :param T_ambiant: Température ambiante
    :return: Distance estimée entre le ième capteur et le centre du faisceau
    """
    arg_log = -(T_ambiant - T_capteur)/T_max
    r_i = (-numpy.log(arg_log)/alpha)**(1/n)
    return r_i


def find_theta(r_1, r_2, delta_r):
    """
    Permet de trouver l'angle entre le capteur 1 et la position du faisceau
    :param r_1: distance estimée entre le faisceau et le capteur 1
    :param r_2: distance estimée entre le faisceau et le capteur 2
    :param delta_r: distance entre le capteur 1 et 2
    :return: angle formé au sommet du capteur 1 du t
    riangle formé par le capteur 1, le capteur 2 et le centre du faisceau
    """
    arg = (r_2**2 - r_1**2 - delta_r**2)/ (-2*delta_r*r_1)
    theta = numpy.arccos(arg)
    return theta


def radial_to_cartesian(r, theta):
    """
    :param r: distance radiale
    :param theta: angle
    :return: coordonnées cartésiennes
    """
    x = r * numpy.cos(theta)
    y = r * numpy.sin(theta)
    arr = numpy.array([x, y])
    return arr


# T_1, T_2, T_3 = 50, 50, 50 # Température des capteurs telles que fournies par
# T_1, T_2, T_3 = 49.8764, 26.9092, 82.522 # Température des capteurs pour obtenir une position de (x,y) = (-2,2)
T_1, T_2, T_3 = 45.796, 23.575, 81.817 # Température des capteurs pour obtenir une position de (x,y) = (-2,2)
R = 6 # Distance radiale des capteurs du centre du filtre.
POS_1 = numpy.array([-5.1961524, -3.0]) # Position des capteurs
POS_2 = numpy.array([5.1961524, -3.0])
POS_3 = numpy.array([0.0, 6.0])
DELTA_R = numpy.linalg.norm((POS_1 - POS_2)) # Distance entre deux capteurs
T_MAX = 400 # On fait une supposition sur la température maximale
DELTA_R_3 = 1 # Initialisation



while abs(DELTA_R_3) > 1e-2: # Tant qu'il y a une différence entre le R3 estimé et le R3 réel
    R_1 = find_r_i(T_MAX, T_1)
    R_2 = find_r_i(T_MAX, T_2)
    R_3 = find_r_i(T_MAX, T_3)
    GUESSED_THETA = find_theta(R_1, R_2, DELTA_R)
    GUESSED_POS = POS_1 + radial_to_cartesian(R_1, GUESSED_THETA)
    GUESSED_R_3 = numpy.linalg.norm((POS_3 - GUESSED_POS))
    DELTA_R_3 = R_3 - GUESSED_R_3
    if GUESSED_R_3 < R_3:
        T_MAX = T_MAX * 0.90
    elif GUESSED_R_3 > R_3:
        T_MAX = T_MAX * 1.10

print(GUESSED_POS, T_MAX+22)
