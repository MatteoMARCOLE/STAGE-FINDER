from Database import Database
from FranceTravailAPI import FranceTravailAPI

bdd = Database("fichier.db")
bdd.creer_bdd()

FranceTravailAPI = FranceTravailAPI()

offres = FranceTravailAPI.rechercher_offres_departement("54")

bdd.vider_bdd()
for offre in offres:
    if offre.get("alternance") is True:
        bdd.ajouter_offre(
            offre.get("id"),
            offre.get("intitule"),
            offre.get("entreprise", {}).get("nom"),
            offre.get("lieuTravail", {}).get("codePostal"),
            offre.get("typeContrat"),
            offre.get("description"),
            offre.get("dateCreation"),
            offre.get("origineOffre", {}).get("urlOrigine"),
        )

