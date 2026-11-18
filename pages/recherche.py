import streamlit as st

from stagefinder.collecte import collecter_toutes_les_sources
from stagefinder.config import DEPARTEMENT, LIEU


NOMS_SOURCES = {
    "France Travail": "france_travail",
    "Adzuna": "adzuna",
    "Jooble": "jooble",
}

st.title("Nouvelle recherche")
st.caption(
    "Définissez ce que vous cherchez. Les API ne sont appelées "
    "qu'après un clic sur le bouton."
)

with st.form("formulaire_recherche"):
    type_recherche = st.radio(
        "Je recherche",
        ["alternance", "stage"],
        horizontal=True,
    )
    mots_cles = st.text_input(
        "Métier ou compétences",
        placeholder="Python, Data Analyst, communication…",
        help=(
            "Le type d'offre choisi est ajouté automatiquement aux "
            "mots-clés envoyés aux API."
        ),
    )

    colonne_lieu, colonne_departement = st.columns(2)
    with colonne_lieu:
        lieu = st.text_input(
            "Ville ou zone",
            value=LIEU,
            help="Utilisé par Adzuna et Jooble.",
        )
    with colonne_departement:
        departement = st.text_input(
            "Numéro de département",
            value=DEPARTEMENT,
            max_chars=3,
            help="Utilisé par France Travail.",
        )

    sources_choisies = st.multiselect(
        "Sources",
        list(NOMS_SOURCES),
        default=list(NOMS_SOURCES),
    )
    lancer = st.form_submit_button(
        "Rechercher et enregistrer",
        type="primary",
        width="stretch",
    )

if lancer:
    if not sources_choisies:
        st.warning("Choisissez au moins une source.")
    elif not lieu.strip() and not departement.strip():
        st.warning("Renseignez une ville ou un département.")
    else:
        sources = [NOMS_SOURCES[nom] for nom in sources_choisies]
        with st.spinner("Interrogation des API en cours…"):
            st.session_state["resultats_recherche"] = (
                collecter_toutes_les_sources(
                    type_recherche=type_recherche,
                    mots_cles=mots_cles,
                    lieu=lieu.strip(),
                    departement=departement.strip(),
                    sources=sources,
                )
            )
            st.session_state["type_derniere_recherche"] = type_recherche

resultats = st.session_state.get("resultats_recherche")
if resultats:
    st.subheader("Résultat de la dernière collecte")
    total_ajoute = sum(resultat["ajoutees"] for resultat in resultats)
    st.success(
        f"{total_ajoute} nouvelle(s) offre(s) enregistrée(s) "
        f"dans la base {st.session_state['type_derniere_recherche']}."
    )

    colonnes = st.columns(len(resultats))
    for colonne, resultat in zip(colonnes, resultats):
        with colonne:
            st.markdown(f"**{resultat['source']}**")
            if resultat["erreur"]:
                st.error(resultat["erreur"])
            else:
                st.metric("Reçues", resultat["recues"])
                st.metric("Nouvelles", resultat["ajoutees"])

st.info(
    "Utilisez « Offres enregistrées » dans la navigation pour consulter "
    "et filtrer les résultats."
)
