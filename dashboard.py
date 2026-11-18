import streamlit as st


st.set_page_config(
    page_title="StageFinder",
    page_icon="🔎",
    layout="wide",
)

page_recherche = st.Page(
    "pages/recherche.py",
    title="Nouvelle recherche",
    icon="🔍",
)
page_offres = st.Page(
    "pages/offres.py",
    title="Offres enregistrées",
    icon="📋",
)

navigation = st.navigation([page_recherche, page_offres])
navigation.run()
