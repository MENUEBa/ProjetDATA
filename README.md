# Projet DATA

MENUE Baptiste
BUTTI GARNIER Zoe
BARATA Wendel
DE OLIVEIRA Hassan Augusto B.

**Objectif** : À partir des données de Pôle Emploi, réaliser de bout en bout un projet de Data Science pour répondre à un besoin business

## Préambule : Comprendre et analyser la donnée 

Avant de réfléchir à un besoin business, et donc au sujet de notre projet, nous avons commencé par nous connecter à l'API de Pôle Emploi et requêter sur celle-ci afin de voir le type des données que nous allions devoir étudier.

**Code Requete.py**
> {"resultats":[{"id":"162MRQR","intitule":"Enseignant(e) de la conduite et  de la sécurité routière (H/F)","description":"Nous recherchons un(e) enseignant(e), titulaire du BEPECASER ou du TP ECS avec la mention B et/ou la mention BE et/ou  A serait un plus.\n\nOuverture de l'Auto Ecole du lundi au samedi. Votre p .... etc 

**Conclusion** 

L'API nous permet d'obtenir un fichier Json organisé de la manière suivante pour chaque offre d'emploi : 

- Resultats 
    - id 
    - intitulé 
    - description
    - ..

Chaque emploi est ainsi organisé de la même manière. Nous comprenons donc que nous allons pouvoir exploiter en particulier le texte de l'intitulé et de la description de chaque emploi, puisque c'est là que se trouve l'essentiel des informations concernant l'emploi proposé. 

### 1. Définir un besoin business

Après avoir vu comment se disposaient les données collectées par le biais de l'API, nous avons réfléchi à une application business et métier à laquelle celles-ci pourraient servir. 
Très vite, nous avons pensé que ces données, en dehors du simple fait d'aider à trouver un emploi, pourraient également servir dans le domaine de la formation professionnelle. 
Le besoin que nous avons identifié est alors celui d'un professionnel, déjà formé et actif dans le monde du travail, et qui chercherait à se reconvertir. Cela pourrait être le cas d'une personne qui n'arrive plus à trouver d'emploi correspondant précisement à sa formation (parce que le marché du travail pour ce métier précis serait saturé par exemple), ou tout simplement d'une personne qui a envie d'évoluer et de se réorienter vers un nouveau métier, sans non plus avoir à changer totalement de carrière et repartir de zéro. 

Nous avons alors choisi de nous placer dans un contexte business qui ne serait non pas celui d'une entreprise qui vendrait un service de réorientation et de formation professionnelle, mais plutôt dans celui du service public. En effet, il nous a semblé cohérent que le Ministère du Travail, afin de lutter contre le chômage et de promouvoir les nombreuses formations professionnelles qu'il propose et finance, par le biais du Compte Personnel de Formation notamment, puisse chercher à aider en particulier les travailleurs en quête de reconversion professionnelle. Notre projet se destinerait ainsi à servir le Ministère du Travail français. 

### 2. L'objectif de modélisation

Une fois ce besoin identifié, nous avions 3 grandes idées initiales concernant ce que nous voulions réaliser dans la pratique : 
- Un matching de CV avec les offres d'emploi actuellement en ligne sur Pôle Emploi 
- En fonction des résultats, proposer des formations professionnelles complémentaires proposées par l'Etat et qui permettraient de mieux correspondre aux offres d'emploi qui nous sont personnellement proposées
- Faire une application de veille par mail qui permettrait de renvoyer les nouvelles annonces susceptibles de convenir à notre CV et donc les formations professionnelles associées

Le simple matching des CV nous semblait être une idée intéressante et accessible mais peu originale. C'est pour cela que nous souhaitions également complexifier et porter notre projet plus loin en ajoutant la proposition de formations professionnelles complémentaires. En ce qui concerne la dernière idée, après nous être renseignés sur la question, nous sommes arrivés au constat que celle-ci était peut-être un peu trop ambitieuse.

**Conclusion**

Objectif final : faire une application qui, à partir d'un CV, propose un matching sur plusieurs offres d'emploi, puis renvoie vers des formations complémentaires adaptées et proposées par l'Etat pour les emplois où il y aurait des lacunes en termes de compétences.

La démarche consistera donc ici à prédire, à partir des données d'un CV fourni et de celles présentes sur Pôle Emploi, quelles offres d'emploi sont les plus proches du profil d'un professionnel. Ensuite, il faut identifier quelles sont les différences notables, en termes de connaissances et de compétences, entre le CV de la personne et les prérequis demandés dans l'offre d'emploi. Finalement, à partir des différences identifiées, il faudra identifier quelle formation professionnelle existante permettrait de combler ces différences et d'apporter au professionnel les connaissances et compétences manquantes.

### 3. Les étapes du code

Ensuite, nous avons déterminé que pour pouvoir réaliser cette idée business, nous allions devoir procéder en trois temps : 
I. Tout d'abord, réaliser le matching de CV avec les offres présentes sur l'API de Pôle Emploi pour trouver les offres d'emploi qui collent le plus avec le CV en question
II. Dans un second temps, récupérer les compétences requises pour ces offres d'emploi-là et identifier celles qui sont manquantes dans le CV
III. Enfin, proposer des formations professionnelles permettant d'acquérir ces compétences manquantes. 

## 0. la base de données : les offres de Pôle Emploi

Dans un premier temps, nous avions suivi le tutoriel fourni pour nous connecter à l'API. Puis nous avons souhaité trouver le moyen de ne plus devoir passer par l'API et systématiquement devoir copier coller l'accès pour ensuite la mettre dans notre jupyter NoteBook, mais plutôt créé un code python qui vienne de lui-même récupérer l'accès. C'est en quelque sorte le début de l'automatisation de notre projet.

Nous avons donc intégrée la requête directement dans notre code python comme suit :

```ruby
def acces():
    import json
    import http.client

    conn = http.client.HTTPSConnection("entreprise.pole-emploi.fr")
    payload = "client_id=PAR_projetv2_e02793cbd340bab1d37781b12b99e06d25ed9273604c2061d1ad1e5b4f167758&client_secret=92cdb43ccf89844279e6bfc8ffbe1a80e301098cb4ad33978c50db544b57c2db&scope=api_offresdemploiv2%20application_PAR_projetv2_e02793cbd340bab1d37781b12b99e06d25ed9273604c2061d1ad1e5b4f167758%20o2dsoffre&grant_type=client_credentials"
    headers = {
    'cookie': "so007-peame-affinity-prod-p=ab3a188a2c2569a2; BIGipServerPOOL_PROD02-SDDC-K8S_HTTPS=!CZLZdbzdUC0otKfGs4t8wMAtY5XJdQbCTKXrEvxLEYwITeobaBoVFreqmeQBUTUhoPkhCRjQ9MeJwA%3D%3D; TS0188135e=01b3abf0a218d19ca4f52cf0f6e614517b15ec521b0cbb5974a9c19c85b2141c1f3cb60fa064923c42b73b76a9afa4ba184abe84a2",
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
```

Toutefois, après plusieurs mois sur le projet, nous nous sommes rendu compte que les requêtes API sur Pôle Emploi avaient une date d'expiration. Le problème majeur de cela est qu'il faut alors tout recommencer, notamment créer un nouveau compte sur l'API et surtout de devoir refaire une requête insomnia. Cela est donc problématique si l'on veut industrialiser notre projet, car dans quelques semaines/mois notre autorisation d'accès aura expiré et il sera alors impossible de se connecter à l'API et d'utiliser notre service de matching de CV.

Pour pallier à ça, nous avons donc estimé que notre seule solution était de séparer le code de la requête qui permet de récupérer les données de l'API et de le mettre à part. Le but est donc de faire la requête qu'une fois et de stocker ensuite le resultat de la requête dans une base de données sous format JSON, qui pourra elle être ensuite facilement utilisée dans toute les étapes suivantes du code. Le matching de CV et des formations pourra ainsi se faire indépendemment de la requête sur l'API, en prenant simplement en entrée cette base de données.

La fonction utilisée pour créer la database en requêtant les données de l'API est :

```ruby
def cree_db():

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

    # Enregistrer les données dans un fichier JSON
    with open('database.json', 'w') as json_file:
      json.dump(data, json_file, indent=4)  # indent=4 pour une mise en forme plus lisible
```

> [!NOTE]
> L'ensemble du code permettant d'accéder à l'API et de stocker les données dans une base de données est : Cree_db_pole_emploi.py

L'avantage de cette solution est qu'elle permet de contourner le problème d'expiration de l'autorisation d'accès à l'API de Pôle Emploi et fais en sorte que n'importe qui puisse utiliser notre code avec les données de Pôle Emploi, et ce y compris dans plusieurs mois. 

L'inconvénient est que du coup nous n'avons pas des données qui s'actualisent en permanence avec les nouvelles offres d'emploi comme lorsque l'on passe directement par l'API, car on crée une base de données à un instant t qui après n'est plus modifiée. Malheureusement, nous n'avons pas trop d'autres solutions si l'on veut pouvoir industrialiser le projet. On pourra simplement faire attention à réactualiser manuellement régulièrement la base de données en refaisant tourner le code "Cree_db_pole_emploi.py" pour fournir à l'utilisateur une base de données qui ne date pas trop.

/////////

## I. Le matching du CV avec les offres d'emploi

Pour celle-ci, les grandes lignes du code devront se décomposer ainsi : 
- Faire la requête pour récuperer facilement les données de l'API (à ce moment-là du projet, cela avait déjà été fait à l'étape 1 ci-dessus)
- Transformer les données pour ne récupérer que les descriptions et les intitulés dans le but d'avoir les données sur l'emploi en question et de pouvoir ensuite voir s'il matche avec le CV. On fait cela grâce à un algorithme LDA de Machine Learning
- Une fois les données récupérées, nous allons en faire des couples de tuples pour les annonces ((Id,description)) 
- Il faut convertir le fichier PDF en une base de donnée (text) 
- Une fois que nous avons transformé le fichier en texte nous allons le Tokeniser pour ne garder que les éléments importants du CV
- Il suffit ensuite de créer un dictionnaire afin de créer des topics grâce au modèle LDA (pour le CV en question)
- Pour finir, une fois que nous avons trouvé les Topics du CV, nous allons noter suivant ces topics chaque description des emplois. On fait ensuite une moyenne des scores pour en sortir les emplois qui s'en rapprochent le plus. 
- L'objectif final est de faire la même chose dans l'autre sens avec les 10 descriptions qui ont eu le meilleur score, faire ressortir des Topics et voir ceux qui ont le moins de matchs avec le CV. Cela permet de déterminer quel type de formation il manquerait à la personne pour coller parfaitement à l'offre d'emploi.

> [!NOTE]
> LDA (Latent Dirichlet Allocation) est une des techniques de NLP les plus connues. C’est une méthode qui repose sur de l’apprentissage non supervisé, et dont l’objectif est d’extraire les sujets principaux, représentés par un ensemble de mots, qui apparaissent dans une collection de documents.


### 1. Convertir le PDF 

Dans un premier temps le plus important était de trouver un moyen d'avoir un algorithme qui convertit un fichier PDF en une liste de mot pour pouvoir ensuite avoir un algorithme de machine learning sur le natural language 

Nous avons utilisé 
> [!NOTE]
> PyPDF2 est une bibliothèque Python open-source qui permet de manipuler des fichiers PDF. Elle fournit des fonctionnalités permettant par exemple d'extraire du texte, defusionner ou diviser des fichiers PDF, ou encore d'extraire des
> métadonnées d'un texte. Vous pouvez retrouver la documentation ici : https://pypdf2.readthedocs.io/en/3.0.0/ 

### 2. LDA (Latent Dirichlet Allocation)

LDA est une technique de modélisation de sujets largement utilisée en analyse de texte. Elle est basée sur l'hypothèse que les documents sont générés à partir d'un mélange de sujets, et chaque sujet est une distribution de mots. Voici une description de base de son fonctionnement :

1. Données d'entrée : Un ensemble de documents texte.
2. Prétraitement : Les documents sont prétraités pour la tokenisation, la suppression des mots vides, la normalisation, etc.
3. Construction d'un vocabulaire : Tous les mots uniques dans les documents sont collectés pour former un vocabulaire.
4. Création de la matrice de documents-termes : Chaque document est représenté sous forme d'un vecteur de la taille du vocabulaire, où chaque élément représente la fréquence d'un mot dans le document.
5. Entraînement du modèle LDA : L'algorithme LDA est utilisé pour trouver un certain nombre de sujets dans les documents et leur distribution respective.
6. Interprétation des sujets : Les mots les plus probables pour chaque sujet sont extraits, permettant d'interpréter le sujet.
7. Application du modèle : Une fois entraîné, le modèle peut être utilisé pour classifier de nouveaux documents en fonction de leur distribution de sujets.

> [!NOTE]
> LDA est un modèle probabiliste et non supervisé, ce qui signifie qu'il est capable de découvrir les structures cachées (les sujets) dans les données sans étiquettes préalables. Il est largement utilisé dans la fouille de textes, la recommandation de contenu, la classification de documents, etc.

### 6. Exemple

```ruby
# Obtention de notre classement directement à la suite de l'appel de cette fonction
resultats = classifier_offres_lda('/Users/menuebaptiste/Desktop/CV_Baptiste_MENUE.pdf', data_offres(), 10)
```

```
Classement 1 - ID de l'offre : Data Scientist / Développeur.se Dataiku (H/F), Score : 0.4989863187074661
Classement 2 - ID de l'offre : Coordinateur du Conseil Local de Santé Mentale (H/F), Score : 0.498641237616539
Classement 3 - ID de l'offre : CONDUCTEUR DE CHANTIER Electrotechnique Industriel (H/F), Score : 0.4984162598848343
Classement 4 - ID de l'offre : Développeur / Développeuse back-end, Score : 0.49841612577438354
Classement 5 - ID de l'offre : Conducteur de Travaux Electrotechnique Industriel (H/F), Score : 0.4984140172600746
Classement 6 - ID de l'offre : Responsable d'Atelier de Production (H/F), Score : 0.4983827620744705
Classement 7 - ID de l'offre : Infirmier / Infirmière (H/F), Score : 0.4983685538172722
Classement 8 - ID de l'offre : Ingénieur.e DevOps / DataOps (H/F), Score : 0.49829962849617004
Classement 9 - ID de l'offre : Formateur en mathématiques - Sciences physiques - Chimie (H/F), Score : 0.498233437538147
Classement 10 - ID de l'offre : Chef de programmes (H/F), Score : 0.49811629951000214
```

On peut voir que cela fonctionne bien car le CV passé en entrée est typé Data et ingénieur généraliste, et donc que les offres qui ressortent sont en accord avec ce profil. 

## II. Trouver les compétences manquantes 

## III. Le matching des compétences manquantes avec les formations professionnelles 
