import pandas as pd
import streamlit as st

from stagefinder.config import CHEMIN_BDD, TYPE_RECHERCHE
from stagefinder.database import Database


bdd = Database(CHEMIN_BDD)
bdd.creer_bdd()
offres = bdd.recuperer_offres()

df = pd.DataFrame(
    offres,
    columns=[
        "id",
        "id_offre",
        "titre",
        "entreprise",
        "lieu",
        "contrat",
        "description",
        "date_creation",
        "url",
        "source",
    ],
)

lieux = sorted(df["lieu"].dropna().unique())
lieu_selectionne = st.selectbox(
    "Choisissez un lieu pour filtrer les offres",
    ["Tous les lieux"] + lieux,
    index=0,
)

contrats = sorted(df["contrat"].dropna().unique())
contrat_selectionne = st.selectbox(
    "Choisissez un type de contrat",
    ["Tous les contrats"] + contrats,
    index=0,
)

mot_cle = st.text_input(
    "Rechercher dans les offres",
    placeholder="Exemple : Python, Data, SQL…",
)

st.title("STAGE FINDER")
st.metric(
    "Nombre d'offres d'alternance enregistrées",
    bdd.compter_offres(),
)
st.title("Offres d'alternance")

offres_filtrees = df

if lieu_selectionne != "Tous les lieux":
    offres_filtrees = offres_filtrees[
        offres_filtrees["lieu"] == lieu_selectionne
    ]

if contrat_selectionne != "Tous les contrats":
    offres_filtrees = offres_filtrees[
        offres_filtrees["contrat"] == contrat_selectionne
    ]

if mot_cle:
    correspondances = (
        offres_filtrees["titre"].str.contains(
            mot_cle,
            case=False,
            na=False,
            regex=False,
        )
        | offres_filtrees["entreprise"].str.contains(
            mot_cle,
            case=False,
            na=False,
            regex=False,
        )
        | offres_filtrees["description"].str.contains(
            mot_cle,
            case=False,
            na=False,
            regex=False,
        )
    )
    offres_filtrees = offres_filtrees[correspondances]

st.dataframe(offres_filtrees)

csv = offres_filtrees.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Télécharger les offres filtrées",
    data=csv,
    file_name=f"offres_{TYPE_RECHERCHE}.csv",
    mime="text/csv",
)
