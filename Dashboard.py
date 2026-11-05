import streamlit as st
import pandas as pd
from Database import Database

bdd = Database("fichier.db")

offres = bdd.recuperer_offres()

df = pd.DataFrame(
    offres,
    columns=[
        "id", "id_offre", "titre", "entreprise",
        "lieu", "contrat", "description",
        "date_creation", "url"
    ]
)

lieux = df["lieu"].dropna().unique()
lieux = sorted(lieux)

lieu_selectionne = st.selectbox(
    "Choisissez un lieu pour filtrer les offres",
    ["Tous les lieux"] + lieux,
    index=0
)

## dfNancy = df[df["lieu"].str.contains("54")]

st.title("STAGE FINDER")

st.metric("Nombres d'offres d'alternance dans le departement 54", bdd.compter_offres())
st.title("Offres à Nancy")

if lieu_selectionne == "Tous les lieux":
    offres_filtrees = df
else:
    offres_filtrees = df[df["lieu"] == lieu_selectionne]

st.dataframe(offres_filtrees)

df.to_csv("resultatsCSV/offresNancyAlternance.csv", index=False)