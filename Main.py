from Database import Database
from FranceTravailAPI import FranceTravailAPI

type_recherche = "alternance"

bdd = Database(f"offres_{type_recherche}.db")
bdd.creer_bdd()

FranceTravailAPI = FranceTravailAPI()

offres = FranceTravailAPI.rechercher_offres_departement("54")

offres_supplementaires = 0;

for offre in offres:
    if offre.get("alternance") is True:
        offre_ajoutee = bdd.ajouter_offre(
            offre.get("id"),
            offre.get("intitule"),
            offre.get("entreprise", {}).get("nom"),
            offre.get("lieuTravail", {}).get("codePostal"),
            offre.get("typeContrat"),
            offre.get("description"),
            offre.get("dateCreation"),
            offre.get("origineOffre", {}).get("urlOrigine"),
        )

        if offre_ajoutee:
            offres_supplementaires += 1

print(f"{offres_supplementaires} nouvelle(s) offre(s) ajoutée(s)")

        

