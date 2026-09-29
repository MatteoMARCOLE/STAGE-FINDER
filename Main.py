import os
from Database import Database
import requests
import subprocess

from dotenv import load_dotenv

bdd = Database("fichier.db")
bdd.creer_bdd()

# URLs France Travail
URL_AUTH = (
    "https://entreprise.francetravail.fr/"
    "connexion/oauth2/access_token?realm=/partenaire"
)

URL_OFFRES = (
    "https://api.francetravail.io/"
    "partenaire/offresdemploi/v2/offres/search"
)


# Charger les variables d'environnement
load_dotenv()

client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

if not client_id or not client_secret:
    raise Exception("Identifiants France Travail manquants")


# Récupération du jeton OAuth
parametres_auth = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "api_offresdemploiv2 o2dsoffre",
}

reponse_auth = requests.post(
    URL_AUTH,
    data=parametres_auth,
    timeout=10,
)

if reponse_auth.status_code != 200:
    raise Exception(
        f"Erreur d'authentification : HTTP {reponse_auth.status_code}"
    )

donnees_auth = reponse_auth.json()
token = donnees_auth.get("access_token")

subprocess.run(
    ["clip.exe"],
    input=token,
    text=True,
    check=True
)

print("Token copié dans le presse-papiers")

if not token:
    raise Exception("Jeton d'accès manquant ou vide")

print("Authentification réussie")


# Préparation de la requête vers l'API Offres d'emploi
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
}

recherche = {
    "motsCles": "informatique",
    "departement": "54",
}


# Récupération des offres
reponse_offres = requests.get(
    URL_OFFRES,
    headers=headers,
    params=recherche,
    timeout=10,
)

if reponse_offres.status_code != 200:
    raise Exception(
        f"Erreur API Offres : HTTP {reponse_offres.status_code}"
    )

donnees_offres = reponse_offres.json()
offres = donnees_offres.get("resultats", [])

print(f"{len(offres)} offres récupérées")


# Affichage de quelques offres

"""for offre in offres:
    bdd.ajouter_offre(
        offre.get("id", ""),
        offre.get("intitule", ""),
        offre.get("entreprise", {}).get("nom", "Entreprise inconnue"),
        offre.get("lieuTravail", {}).get("libelle", ""),
        offre.get("typeContrat", ""),
        offre.get("description", ""),
        offre.get("dateCreation", ""),
        offre.get("origineOffre", {}).get("urlOrigine", "")
    )"""

print(bdd.recuperer_offres())