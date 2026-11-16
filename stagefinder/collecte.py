from stagefinder.api.adzuna import AdzunaAPI
from stagefinder.api.france_travail import FranceTravailAPI
from stagefinder.api.jooble import JoobleAPI
from stagefinder.config import (
    CHEMIN_BDD,
    DEPARTEMENT,
    LIEU,
    TYPE_RECHERCHE,
)
from stagefinder.database import Database
from stagefinder.normalisation import (
    normaliser_offre_adzuna,
    normaliser_offre_france_travail,
    normaliser_offre_jooble,
)


def enregistrer_offres(bdd, offres, normaliser):
    nouvelles_offres = 0

    for offre in offres:
        offre_normalisee = normaliser(offre)
        if bdd.ajouter_offre(**offre_normalisee):
            nouvelles_offres += 1

    return nouvelles_offres


def collecter_source(bdd, nom_source, rechercher, normaliser):
    try:
        offres = rechercher()
        nouvelles_offres = enregistrer_offres(bdd, offres, normaliser)
        print(
            f"{nom_source} : {len(offres)} offre(s) reçue(s), "
            f"{nouvelles_offres} ajoutée(s)"
        )
        return nouvelles_offres
    except Exception as erreur:
        print(
            f"{nom_source} indisponible : "
            f"{type(erreur).__name__}"
        )
        return 0


def rechercher_france_travail():
    france_travail = FranceTravailAPI()
    offres = france_travail.rechercher_offres_departement(DEPARTEMENT)
    return [
        offre
        for offre in offres
        if offre.get("alternance") is True
    ]


def collecter_toutes_les_sources():
    bdd = Database(CHEMIN_BDD)
    bdd.creer_bdd()
    total_nouvelles_offres = 0

    total_nouvelles_offres += collecter_source(
        bdd,
        "France Travail",
        rechercher_france_travail,
        normaliser_offre_france_travail,
    )

    if AdzunaAPI.est_configuree():
        adzuna = AdzunaAPI()
        total_nouvelles_offres += collecter_source(
            bdd,
            "Adzuna",
            lambda: adzuna.rechercher_offres(TYPE_RECHERCHE, LIEU),
            normaliser_offre_adzuna,
        )
    else:
        print("Adzuna ignorée : identifiants absents du fichier .env")

    if JoobleAPI.est_configuree():
        jooble = JoobleAPI()
        total_nouvelles_offres += collecter_source(
            bdd,
            "Jooble",
            lambda: jooble.rechercher_offres(TYPE_RECHERCHE, LIEU),
            normaliser_offre_jooble,
        )
    else:
        print("Jooble ignorée : clé absente du fichier .env")

    return total_nouvelles_offres
