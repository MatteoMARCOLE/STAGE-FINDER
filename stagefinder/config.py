from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parent.parent
DOSSIER_DONNEES = RACINE_PROJET / "data"

TYPE_RECHERCHE = "alternance"
DEPARTEMENT = "54"
LIEU = "Nancy"


def obtenir_chemin_bdd(type_recherche):
    return DOSSIER_DONNEES / f"offres_{type_recherche}.db"


CHEMIN_BDD = obtenir_chemin_bdd(TYPE_RECHERCHE)
