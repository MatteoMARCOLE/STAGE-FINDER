from stagefinder.collecte import collecter_toutes_les_sources


if __name__ == "__main__":
    resultats = collecter_toutes_les_sources()
    nouvelles_offres = sum(
        resultat["ajoutees"]
        for resultat in resultats
    )
    print(f"{nouvelles_offres} nouvelle(s) offre(s) ajoutée(s)")
