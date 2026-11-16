import os
import subprocess

import requests
from dotenv import load_dotenv


load_dotenv()

URL_AUTH = (
    "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    "?realm=/partenaire"
)
URL_OFFRES = (
    "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
)


class FranceTravailAPI:
    def __init__(self):
        self.client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
        self.client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("Identifiants France Travail manquants")

        self.token = self.obtenir_token()

    def obtenir_token(self):
        parametres_auth = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre",
        }

        reponse = requests.post(
            URL_AUTH,
            data=parametres_auth,
            timeout=10,
        )

        if reponse.status_code != 200:
            raise Exception(
                f"Erreur d'authentification : HTTP {reponse.status_code}"
            )

        token = reponse.json().get("access_token")
        if not token:
            raise Exception("Jeton d'accès manquant ou vide")

        if os.name == "nt":
            subprocess.run(
                ["clip.exe"],
                input=token,
                text=True,
                check=True,
            )
            print("Token copié dans le presse-papiers")

        print("Authentification France Travail réussie")
        return token

    def rechercher_offres_departement(self, departement):
        reponse = requests.get(
            URL_OFFRES,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            },
            params={"departement": departement},
            timeout=10,
        )
        reponse.raise_for_status()
        return reponse.json().get("resultats", [])

    def rechercher_offres_contrat(self, contrat):
        reponse = requests.get(
            URL_OFFRES,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            },
            params={"typeContrat": contrat},
            timeout=10,
        )
        reponse.raise_for_status()
        return reponse.json().get("resultats", [])
