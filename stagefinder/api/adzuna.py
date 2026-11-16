import os

import requests
from dotenv import load_dotenv


load_dotenv()

URL_RECHERCHE = "https://api.adzuna.com/v1/api/jobs/fr/search/{page}"


class AdzunaAPI:
    @staticmethod
    def est_configuree():
        return bool(
            os.getenv("ADZUNA_APP_ID")
            and os.getenv("ADZUNA_APP_KEY")
        )

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")

        if not self.app_id or not self.app_key:
            raise ValueError("Identifiants Adzuna manquants")

    def rechercher_offres(self, mots_cles, lieu, page=1):
        reponse = requests.get(
            URL_RECHERCHE.format(page=page),
            params={
                "app_id": self.app_id,
                "app_key": self.app_key,
                "what": mots_cles,
                "where": lieu,
                "results_per_page": 50,
                "content-type": "application/json",
            },
            timeout=10,
        )

        if reponse.status_code != 200:
            raise Exception(
                f"Erreur Adzuna : HTTP {reponse.status_code}"
            )

        return reponse.json().get("results", [])
