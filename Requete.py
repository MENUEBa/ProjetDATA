def acces():
    import json
    import http.client
    
    conn = http.client.HTTPSConnection("entreprise.pole-emploi.fr")
    payload = "client_id=PAR_projetdatabm_6c38332c3b9ad65a426b8497e0517c0ca60f859b82c91b61537dba22351af31c&client_secret=1f38dcd0b94365e8159c0ed051ad124e9af14d9a75bc96b363265fed58c8da06&scope=api_offresdemploiv2%20application_PAR_projetdatabm_6c38332c3b9ad65a426b8497e0517c0ca60f859b82c91b61537dba22351af31c%20o2dsoffre&grant_type=client_credentials"
    headers = {
    'cookie': "so007-peame-affinity-prod-p=a9f8402749805557; BIGipServerPOOL_PROD02-SDDC-K8S_HTTPS=!CZLZdbzdUC0otKfGs4t8wMAtY5XJdQbCTKXrEvxLEYwITeobaBoVFreqmeQBUTUhoPkhCRjQ9MeJwA%3D%3D; TS0188135e=01b3abf0a21a986869f7dfb32e16316f2a44096734d6d2aa76bb20005e1c6a44b73cfcf16c5e8f49dab64b881a493548cd0eeff0b8",
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "insomnia/8.2.0"
    }
    conn.request("POST", "/connexion/oauth2/access_token?realm=%2Fpartenaire", payload, headers)
    res = conn.getresponse()
    data = res.read()
    donnee = data.decode("utf-8")
    # Récupérez le token
    donnee_JSON = json.loads(donnee)
    access_token = donnee_JSON.get('access_token')
    return access_token
