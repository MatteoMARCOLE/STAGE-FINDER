# STAGE FINDER

STAGE FINDER récupère des offres d'alternance depuis France Travail,
Adzuna et Jooble, les normalise, les enregistre dans SQLite puis les
affiche dans un dashboard Streamlit.

## Installation

Créer et activer un environnement virtuel, puis installer les dépendances :

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Copier `.env.example` vers `.env` et renseigner les identifiants des API :

```env
FRANCE_TRAVAIL_CLIENT_ID=
FRANCE_TRAVAIL_CLIENT_SECRET=
ADZUNA_APP_ID=
ADZUNA_APP_KEY=
JOOBLE_API_KEY=
```

## Utilisation

Lancer la collecte :

```bash
.venv/bin/python main.py
```

Lancer le dashboard :

```bash
.venv/bin/streamlit run dashboard.py
```

## Architecture

```text
stagefinder/
├── api/
│   ├── adzuna.py
│   ├── france_travail.py
│   └── jooble.py
├── collecte.py
├── config.py
├── database.py
└── normalisation.py

data/                  Bases SQLite locales
main.py                Point d'entrée de la collecte
dashboard.py           Navigation de l'interface Streamlit
pages/
├── recherche.py       Formulaire d'appel des API
└── offres.py          Consultation et filtrage des offres
requirements.txt       Dépendances Python
```

Chaque API renvoie un JSON différent. Les fonctions de `normalisation.py`
les convertissent vers le même format avant leur insertion dans la base.

## Limites et perspectives

Les API gratuites utilisées offrent une couverture et des formats de données
hétérogènes. Les critères disponibles diffèrent selon les sources et la
distinction entre stage et alternance n'est pas toujours structurée, ce qui
limite la pertinence de certains résultats.

StageFinder répond en partie à ces difficultés en centralisant, normalisant et
dédoublonnant les offres. Les prochaines améliorations pourraient inclure un
score de pertinence fondé sur les compétences recherchées, la pagination
complète des API et l'intégration de nouvelles sources spécialisées.