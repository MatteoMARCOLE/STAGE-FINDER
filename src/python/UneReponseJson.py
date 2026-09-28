
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

reponse = requests.get(url, timeout=10)

print(reponse.status_code)

if (reponse.status_code == 200):
    donnee = reponse.json()
    print(donnee["title"])
else:
    raise Exception ("Erreur lors de la récupération des données")
    

