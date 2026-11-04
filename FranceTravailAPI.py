import os
import requests
import subprocess

from dotenv import load_dotenv

# URLs France Travail
URL_AUTH = (
    "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
)

URL_OFFRES = (
    "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
)

# Charger les variables d'environnement
load_dotenv()

client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

class FranceTravailAPI:
    def __init__(self):
        if not client_id or not client_secret:
            raise Exception("Identifiants France Travail manquants")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.obtenir_token()

    def obtenir_token(self):
        # Récupération du jeton OAuth
        parametres_auth = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
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

        if not token:
            raise Exception("Jeton d'accès manquant ou vide")

        subprocess.run(
                    ["clip.exe"],
                    input=token,
                    text=True,
                    check=True
                )
        
        print("Token copié dans le presse-papiers", "\n")

        print("Authentification réussie")

        return token

        
    def rechercher_offres_departement(self, departement):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

        recherche = {
            "departement": departement
        }

        reponse = requests.get(
            URL_OFFRES,
            headers=headers,
            params=recherche,
            timeout=10
        )

        reponse.raise_for_status()

        return reponse.json().get("resultats", [])

    def rechercher_offres_contrat(self, contrat):
        headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json",
                }

        recherche = {
            "typeContrat": contrat
        }

        reponse = requests.get(
            URL_OFFRES,
            headers=headers,
            params=recherche,
            timeout=10
        )

        reponse.raise_for_status()

        return reponse.json().get("resultats", [])

