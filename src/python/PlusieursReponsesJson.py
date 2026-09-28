
import requests

url = "https://jsonplaceholder.typicode.com/posts"

rep = requests.get(url, timeout=20)

print(rep.status_code)

if rep.status_code == 200:

    publications = rep.json()

    nbRep = len(publications)
    print("Nombre de publications :", nbRep, "\n")

    for p in publications:
        print(p["id"], p["title"])

    print("\nPublications dont l'identifiant est inférieur ou égal à 5 :")

    for p in publications:
        if p["id"] <= 5:
            print(p["id"], p["title"])

else:
    raise Exception("Erreur lors de la récupération des données")