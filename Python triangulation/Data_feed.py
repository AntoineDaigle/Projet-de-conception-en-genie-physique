import pandas as pd


def ReadDATA(PATH):
    """Fonction qui va chercher les données du test.

    Args:
        PATH (regex): Path du fichier

    Returns:
        list: Liste de liste contenant chaque thermistance.
    """

    df = pd.read_csv(PATH)


    # Va chercher les données PAS TOUCHE GRAND-MÈRE
    Raw_data = df["LabVIEW Measurement\t"][20:]
    Therms = []


    # Split the data de manière élégante et optimisé (LOL PÔ VRAI)
    for i in Raw_data:
        Data = i.split("\t")

        Therms.append(map(float, Data[1:]))
    return Therms



