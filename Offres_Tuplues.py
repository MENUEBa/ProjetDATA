# Charger les données JSON
data = json.loads(data_JSON)

# Liste pour stocker les tuples (ID, description)
Offres = []

# Parcourir chaque emploi dans les résultats
for emploi_resultat in data['resultats']:
    emploi_id = emploi_resultat.get('intitule', None)
    description = emploi_resultat.get('description', None)

    if emploi_id is not None and description is not None:
        Offres.append([emploi_id, description])

print(Offres)