import re
import unicodedata

import pandas as pd


NOMS_SOURCES = {
    "france_travail": "France Travail",
    "adzuna": "Adzuna",
    "jooble": "Jooble",
}

PRIORITE_SOURCES = {
    "france_travail": 0,
    "adzuna": 1,
    "jooble": 2,
}

CODES_POSTAUX = {
    "54000": "Nancy",
    "54100": "Nancy",
    "54200": "Toul",
    "54300": "Lunéville",
    "54400": "Longwy",
    "54500": "Vandœuvre-lès-Nancy",
    "54520": "Laxou",
    "54600": "Villers-lès-Nancy",
    "54700": "Pont-à-Mousson",
}


def nettoyer_lieu(lieu):
    if pd.isna(lieu) or not str(lieu).strip():
        return "Non précisé"

    lieu = str(lieu).strip()
    ville = lieu.split(",", maxsplit=1)[0].strip()

    if ville in CODES_POSTAUX:
        return CODES_POSTAUX[ville]
    if ville.isdigit():
        return f"Secteur {ville}"

    return ville


def nettoyer_contrat(contrat):
    if pd.isna(contrat) or not str(contrat).strip():
        return "Non précisé"

    contrat = re.sub(
        r",?\s*srJobType\d+",
        "",
        str(contrat),
        flags=re.IGNORECASE,
    ).strip(" ,")
    contrat_minuscule = contrat.casefold()

    if "stage" in contrat_minuscule:
        return "Stage"
    if "cdi" in contrat_minuscule or "permanent" in contrat_minuscule:
        return "CDI / permanent"
    if "cdd" in contrat_minuscule or contrat_minuscule == "contract":
        return "CDD / contrat"
    if "intér" in contrat_minuscule:
        return "Intérim"
    if "temps plein" in contrat_minuscule:
        return "Temps plein"

    return contrat


def normaliser_texte(texte):
    texte = unicodedata.normalize("NFKD", str(texte or ""))
    texte = "".join(
        caractere
        for caractere in texte
        if not unicodedata.combining(caractere)
    )
    return re.sub(r"[^a-z0-9]+", " ", texte.casefold()).strip()


def preparer_offres(df):
    offres = df.copy()
    offres["Titre"] = offres["titre"].fillna("Sans titre")
    offres["Entreprise"] = offres["entreprise"].fillna("Non précisée")
    offres["Lieu"] = offres["lieu"].apply(nettoyer_lieu)
    offres["Contrat"] = offres["contrat"].apply(nettoyer_contrat)
    offres["Source"] = offres["source"].map(NOMS_SOURCES).fillna(
        offres["source"]
    )
    offres["_date"] = pd.to_datetime(
        offres["date_creation"],
        errors="coerce",
        utc=True,
    )
    offres["Publié le"] = offres["_date"].dt.strftime("%d/%m/%Y")
    offres["Publié le"] = offres["Publié le"].fillna("Non précisée")
    offres["_priorite_source"] = offres["source"].map(
        PRIORITE_SOURCES
    ).fillna(99)

    offres["_cle_doublon"] = offres.apply(
        lambda ligne: "|".join((
            normaliser_texte(ligne["Titre"]),
            normaliser_texte(ligne["Entreprise"]),
            normaliser_texte(ligne["Lieu"]),
        ))
        if ligne["Entreprise"] != "Non précisée"
        else ligne["id_offre"],
        axis=1,
    )
    return offres


def masquer_doublons(df):
    return (
        df.sort_values(
            ["_priorite_source", "_date"],
            ascending=[True, False],
            na_position="last",
        )
        .drop_duplicates("_cle_doublon", keep="first")
    )
