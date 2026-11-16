from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parent.parent
DOSSIER_DONNEES = RACINE_PROJET / "data"

TYPE_RECHERCHE = "alternance"
DEPARTEMENT = "54"
LIEU = "Nancy"

CHEMIN_BDD = DOSSIER_DONNEES / f"offres_{TYPE_RECHERCHE}.db"
