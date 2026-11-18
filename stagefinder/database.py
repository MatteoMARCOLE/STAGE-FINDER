import sqlite3
from pathlib import Path


class Database:
    def __init__(self, nom_bdd):
        self.nom_bdd = str(nom_bdd)

    def connexion_bdd(self):
        return sqlite3.connect(self.nom_bdd)

    def creer_bdd(self):
        Path(self.nom_bdd).parent.mkdir(parents=True, exist_ok=True)
        connexion = self.connexion_bdd()
        curseur = connexion.cursor()

        curseur.execute("""
            CREATE TABLE IF NOT EXISTS offres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_offre TEXT UNIQUE,
                titre TEXT,
                entreprise TEXT,
                lieu TEXT,
                contrat TEXT,
                description TEXT,
                date_creation TEXT,
                url TEXT,
                source TEXT NOT NULL DEFAULT 'france_travail'
            )
        """)

        colonnes = {
            colonne[1]
            for colonne in curseur.execute("PRAGMA table_info(offres)")
        }

        if "source" not in colonnes:
            curseur.execute("""
                ALTER TABLE offres
                ADD COLUMN source TEXT NOT NULL DEFAULT 'france_travail'
            """)

        curseur.execute("""
            UPDATE offres
            SET id_offre = source || ':' || id_offre
            WHERE id_offre NOT LIKE source || ':%'
        """)

        connexion.commit()
        connexion.close()

    def ajouter_offre(
        self,
        id_offre,
        titre,
        entreprise,
        lieu,
        contrat,
        description,
        date_creation,
        url,
        source,
    ):
        connexion = self.connexion_bdd()
        curseur = connexion.cursor()

        offre_existe = curseur.execute(
            "SELECT 1 FROM offres WHERE id_offre = ?",
            (id_offre,),
        ).fetchone() is not None

        curseur.execute("""
            INSERT INTO offres (
                id_offre,
                titre,
                entreprise,
                lieu,
                contrat,
                description,
                date_creation,
                url,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id_offre) DO UPDATE SET
                titre = excluded.titre,
                entreprise = excluded.entreprise,
                lieu = excluded.lieu,
                contrat = excluded.contrat,
                description = excluded.description,
                date_creation = excluded.date_creation,
                url = excluded.url,
                source = excluded.source
        """, (
            id_offre,
            titre,
            entreprise,
            lieu,
            contrat,
            description,
            date_creation,
            url,
            source,
        ))

        connexion.commit()
        connexion.close()
        return not offre_existe

    def recuperer_offres(self):
        connexion = self.connexion_bdd()
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM offres")
        offres = curseur.fetchall()
        connexion.close()
        return offres

    def compter_offres(self):
        connexion = self.connexion_bdd()
        curseur = connexion.cursor()
        curseur.execute("SELECT COUNT(*) FROM offres")
        resultat = curseur.fetchone()
        connexion.close()
        return resultat[0]

    def vider_bdd(self):
        connexion = self.connexion_bdd()
        connexion.execute("DELETE FROM offres")
        connexion.commit()
        connexion.close()

    def supprimer_offre(self, id_offre):
        connexion = self.connexion_bdd()
        connexion.execute(
            "DELETE FROM offres WHERE id_offre = ?",
            (id_offre,),
        )
        connexion.commit()
        connexion.close()
