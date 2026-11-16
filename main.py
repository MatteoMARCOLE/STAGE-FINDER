from stagefinder.collecte import collecter_toutes_les_sources


if __name__ == "__main__":
    nouvelles_offres = collecter_toutes_les_sources()
    print(f"{nouvelles_offres} nouvelle(s) offre(s) ajoutée(s)")
