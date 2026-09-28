
offre = {
    "titre": "Stage Data Engineer",
    "entreprise": "TechData",
    "ville": "Metz",
    "duree_semaines": 14,
    "competences": [
        "Python",
        "SQL",
        "Docker"
    ]
}
  
t = offre["titre"]
print(t)

v = offre["ville"]
e = offre["entreprise"]
print(v, e)

premiereCompetence = offre["competences"][0]
print(premiereCompetence)

d = offre["duree_semaines"]
dRespecte = True

if not (d >= 8 and d <= 16):
    dRespecte = False

if dRespecte:
    print(d, "Durée compatible")
else:
    print(d, "Durée incompatible")
