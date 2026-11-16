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
dashboard.py           Interface Streamlit
requirements.txt       Dépendances Python
```

Chaque API renvoie un JSON différent. Les fonctions de `normalisation.py`
les convertissent vers le même format avant leur insertion dans la base.
