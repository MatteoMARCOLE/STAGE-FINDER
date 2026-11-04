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

## dfNancy = df[df["lieu"].str.contains("54")]

st.title("STAGE FINDER")

st.metric("Nombres d'offres d'alternance dans le departement 54", bdd.compter_offres())
st.title("Offres à Nancy")
st.dataframe(df)

df.to_csv("resultatsCSV/offresNancyAlternance.csv", index=False)