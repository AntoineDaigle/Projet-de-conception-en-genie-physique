from nptdms import TdmsFile
import numpy as np

def Read_TDMS(Path):
    """Fonction qui permet de déchiffrer le fichier TDMS produit par le logiciel Labview.

    Args:
        Path (regex): Chemin du fichier.

    Returns:
        tuple: (Therm1, Therm2)
    """

    tdms_file = TdmsFile.read(Path)

    Therm1 = []
    Therm2 = []


    for group in tdms_file.groups():
        for channel in group.channels():


            data = channel[:]

            data = np.reshape(data, (int(np.size(data)/2), 2))


            for i in data:
                Therm1.append(i[0])
                Therm2.append(i[1])

    return Therm1, Therm2




Therm1, Therm2 = Read_TDMS(r"C:\Users\Anto\Desktop\Projet-de-conception-en-genie-physique\logg data_2022_04_09_16_21_02.tdms")

print(Therm1)