import pandas as pd
import streamlit as st

from stagefinder.config import obtenir_chemin_bdd
from stagefinder.database import Database
from stagefinder.presentation import masquer_doublons, preparer_offres


COLONNES_BDD = [
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
]

st.title("Offres enregistrées")
st.caption(
    "Affinez les résultats enregistrés sans rappeler les API. "
    "Cliquez sur une ligne pour lire sa description."
)

type_recherche = st.radio(
    "Type d'offre",
    ["alternance", "stage"],
    horizontal=True,
)

bdd = Database(obtenir_chemin_bdd(type_recherche))
bdd.creer_bdd()
df_brut = pd.DataFrame(bdd.recuperer_offres(), columns=COLONNES_BDD)
df = preparer_offres(df_brut)

with st.sidebar:
    st.subheader("Filtrer les offres")
    recherche = st.text_input(
        "Métier, compétence ou entreprise",
        placeholder="Python, Data, communication…",
    )
    localisation = st.text_input(
        "Ville ou code postal",
        placeholder="Nancy, Laxou, 54000…",
    )
    contrats_choisis = st.multiselect(
        "Type de contrat",
        sorted(df["Contrat"].dropna().unique()),
    )
    sources_choisies = st.multiselect(
        "Source",
        sorted(df["Source"].dropna().unique()),
    )
    periode_choisie = st.selectbox(
        "Date de publication",
        ["Toutes", "7 derniers jours", "30 derniers jours", "90 derniers jours"],
    )
    cacher_doublons = st.checkbox(
        "Masquer les doublons probables",
        value=True,
        help=(
            "Conserve une seule offre lorsque le titre, l'entreprise "
            "et le lieu sont identiques."
        ),
    )
    tri = st.selectbox(
        "Trier par",
        ["Plus récentes", "Titre A à Z", "Entreprise A à Z"],
    )

offres_filtrees = df

if recherche:
    correspondances = (
        offres_filtrees["Titre"].str.contains(
            recherche, case=False, na=False, regex=False
        )
        | offres_filtrees["Entreprise"].str.contains(
            recherche, case=False, na=False, regex=False
        )
        | offres_filtrees["description"].str.contains(
            recherche, case=False, na=False, regex=False
        )
    )
    offres_filtrees = offres_filtrees[correspondances]

if localisation:
    correspondances_lieu = (
        offres_filtrees["Lieu"].str.contains(
            localisation, case=False, na=False, regex=False
        )
        | offres_filtrees["lieu"].str.contains(
            localisation, case=False, na=False, regex=False
        )
    )
    offres_filtrees = offres_filtrees[correspondances_lieu]

if contrats_choisis:
    offres_filtrees = offres_filtrees[
        offres_filtrees["Contrat"].isin(contrats_choisis)
    ]

if sources_choisies:
    offres_filtrees = offres_filtrees[
        offres_filtrees["Source"].isin(sources_choisies)
    ]

periodes = {
    "Toutes": None,
    "7 derniers jours": 7,
    "30 derniers jours": 30,
    "90 derniers jours": 90,
}
nombre_jours = periodes[periode_choisie]
if nombre_jours is not None:
    date_limite = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=nombre_jours)
    offres_filtrees = offres_filtrees[
        offres_filtrees["_date"] >= date_limite
    ]

avant_doublons = len(offres_filtrees)
if cacher_doublons:
    offres_filtrees = masquer_doublons(offres_filtrees)
doublons_masques = avant_doublons - len(offres_filtrees)

if tri == "Plus récentes":
    offres_filtrees = offres_filtrees.sort_values(
        "_date", ascending=False, na_position="last"
    )
elif tri == "Titre A à Z":
    offres_filtrees = offres_filtrees.sort_values("Titre")
else:
    offres_filtrees = offres_filtrees.sort_values("Entreprise")

offres_filtrees = offres_filtrees.reset_index(drop=True)

colonne_total, colonne_affichees, colonne_doublons = st.columns(3)
colonne_total.metric("Enregistrées", len(df))
colonne_affichees.metric("Affichées", len(offres_filtrees))
colonne_doublons.metric("Doublons masqués", doublons_masques)

if offres_filtrees.empty:
    st.info(
        "Aucune offre ne correspond à ces filtres. "
        "Élargissez la période ou retirez un critère."
    )
else:
    colonnes_visibles = [
        "Titre",
        "Entreprise",
        "Lieu",
        "Contrat",
        "Source",
        "Publié le",
        "url",
    ]
    evenement = st.dataframe(
        offres_filtrees[colonnes_visibles],
        hide_index=True,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "url": st.column_config.LinkColumn(
                "Annonce",
                display_text="Ouvrir",
            ),
        },
    )

    if evenement.selection.rows:
        offre = offres_filtrees.iloc[evenement.selection.rows[0]]
        st.subheader(offre["Titre"])
        st.write(
            f"{offre['Entreprise']} · {offre['Lieu']} · "
            f"{offre['Contrat']}"
        )
        st.write(offre["description"] or "Description non disponible.")
        if offre["url"]:
            st.link_button("Consulter l'annonce", offre["url"])

    export = offres_filtrees[colonnes_visibles].rename(
        columns={"url": "Lien"}
    )
    csv = export.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Télécharger les résultats affichés",
        data=csv,
        file_name=f"offres_{type_recherche}.csv",
        mime="text/csv",
    )
