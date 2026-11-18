from stagefinder.api.adzuna import AdzunaAPI
from stagefinder.api.france_travail import FranceTravailAPI
from stagefinder.api.jooble import JoobleAPI
from stagefinder.config import (
    DEPARTEMENT,
    LIEU,
    TYPE_RECHERCHE,
    obtenir_chemin_bdd,
)
from stagefinder.database import Database
from stagefinder.normalisation import (
    normaliser_offre_adzuna,
    normaliser_offre_france_travail,
    normaliser_offre_jooble,
)


SOURCES_DISPONIBLES = (
    "france_travail",
    "adzuna",
    "jooble",
)


def construire_mots_cles(type_recherche, mots_cles):
    termes = [type_recherche.strip(), mots_cles.strip()]
    return " ".join(terme for terme in termes if terme)


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
        resultat = {
            "source": nom_source,
            "recues": len(offres),
            "ajoutees": nouvelles_offres,
            "erreur": None,
        }
        print(
            f"{nom_source} : {len(offres)} offre(s) reçue(s), "
            f"{nouvelles_offres} ajoutée(s)"
        )
        return resultat
    except Exception as erreur:
        nom_erreur = type(erreur).__name__
        print(f"{nom_source} indisponible : {nom_erreur}")
        return {
            "source": nom_source,
            "recues": 0,
            "ajoutees": 0,
            "erreur": nom_erreur,
        }


def rechercher_france_travail(type_recherche, mots_cles, departement):
    france_travail = FranceTravailAPI()
    termes = construire_mots_cles(type_recherche, mots_cles)
    offres = france_travail.rechercher_offres(
        departement=departement,
        mots_cles=termes,
    )

    if type_recherche == "alternance":
        return [
            offre
            for offre in offres
            if offre.get("alternance") is True
        ]

    return offres


def collecter_toutes_les_sources(
    type_recherche=TYPE_RECHERCHE,
    mots_cles="",
    lieu=LIEU,
    departement=DEPARTEMENT,
    sources=None,
):
    if sources is None:
        sources = SOURCES_DISPONIBLES
    else:
        sources = tuple(sources)
    termes = construire_mots_cles(type_recherche, mots_cles)

    bdd = Database(obtenir_chemin_bdd(type_recherche))
    bdd.creer_bdd()
    resultats = []

    if "france_travail" in sources:
        resultats.append(
            collecter_source(
                bdd,
                "France Travail",
                lambda: rechercher_france_travail(
                    type_recherche,
                    mots_cles,
                    departement,
                ),
                normaliser_offre_france_travail,
            )
        )

    if "adzuna" in sources:
        if AdzunaAPI.est_configuree():
            adzuna = AdzunaAPI()
            resultats.append(
                collecter_source(
                    bdd,
                    "Adzuna",
                    lambda: adzuna.rechercher_offres(termes, lieu),
                    normaliser_offre_adzuna,
                )
            )
        else:
            resultats.append({
                "source": "Adzuna",
                "recues": 0,
                "ajoutees": 0,
                "erreur": "Identifiants absents",
            })

    if "jooble" in sources:
        if JoobleAPI.est_configuree():
            jooble = JoobleAPI()
            resultats.append(
                collecter_source(
                    bdd,
                    "Jooble",
                    lambda: jooble.rechercher_offres(termes, lieu),
                    normaliser_offre_jooble,
                )
            )
        else:
            resultats.append({
                "source": "Jooble",
                "recues": 0,
                "ajoutees": 0,
                "erreur": "Clé absente",
            })

    return resultats
