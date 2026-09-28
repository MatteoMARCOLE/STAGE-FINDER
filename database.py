import sqlite3

class Database:
    def __init__(self, nom_bdd):
        self.nom_bdd = nom_bdd

    def connexion_bdd(self):
        return sqlite3.connect(self.nom_bdd)


    def creer_bdd(self):
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
                url TEXT
            )
        """)

        connexion.commit()
        connexion.close()


    def ajouter_offre(self,id_offre, titre, entreprise, lieu, contrat, description, date_creation, url):
        connexion = self.connexion_bdd()
        curseur = connexion.cursor()

        curseur.execute("""
            INSERT OR IGNORE INTO offres (
                id_offre,
                titre,
                entreprise,
                lieu,
                contrat,
                description,
                date_creation,
                url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_offre,
            titre,
            entreprise,
            lieu,
            contrat,
            description,
            date_creation,
            url
        ))

        connexion.commit()
        connexion.close()


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
        curseur = connexion.cursor()

        curseur.execute("DELETE FROM offres")

        connexion.commit()
        connexion.close()


    def supprimer_offre(self, id_offre):
        connexion = self.connexion_bdd()
        curseur = connexion.cursor()

        curseur.execute(
            "DELETE FROM offres WHERE id_offre = ?",
            (id_offre,)
        )

        connexion.commit()
        connexion.close()

bdd = Database("stages.db")

bdd.creer_bdd()

print(bdd.compter_offres())
print(bdd.recuperer_offres())