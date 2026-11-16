import os

import requests
from dotenv import load_dotenv


load_dotenv()

URL_RECHERCHE = "https://fr.jooble.org/api/{api_key}"


class JoobleAPI:
    @staticmethod
    def est_configuree():
        return bool(os.getenv("JOOBLE_API_KEY"))

    def __init__(self):
        self.api_key = os.getenv("JOOBLE_API_KEY")

        if not self.api_key:
            raise ValueError("Clé API Jooble manquante")

    def rechercher_offres(self, mots_cles, lieu, page=1):
        reponse = requests.post(
            URL_RECHERCHE.format(api_key=self.api_key),
            json={
                "keywords": mots_cles,
                "location": lieu,
                "radius": "40",
                "page": page,
                "ResultOnPage": 50,
            },
            timeout=10,
        )

        if reponse.status_code != 200:
            raise Exception(
                f"Erreur Jooble : HTTP {reponse.status_code}"
            )

        return reponse.json().get("jobs", [])
