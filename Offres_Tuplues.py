def data_offres():
    import json
    import http.client

    conn = http.client.HTTPSConnection("api.emploi-store.fr")

    payload = ""

    headers = {
    'cookie': "BIGipServerVS_EX035-VIPA-A4PMEX_HTTP.app~POOL_EX035-VIPA-A4PMEX_HTTP=251070986.10062.0000; TS01889661=01b3abf0a2b4ced48023543abda8fc722c3107bde676a0b1434950a7e4437ecfb46660c7bf71ae1b7a99a26bce8b45f31035b35f34",
    'Authorization': "Bearer {}".format(acces())
    }

    conn.request("GET", "/partenaire/offresdemploi/v2/offres/search?maxCreationDate=2023-09-30T12%3A00%3A00Z&minCreationDate=2023-09-01T12%3A00%3A00Z", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_JSON = data.decode("utf-8")
    
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
            
    return Offres