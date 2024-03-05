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

L'avantage de cette solution est qu'elle permet de contourner le problème d'expiration de l'autorisation d'accès à l'API de Pôle Emploi et fait en sorte que n'importe qui puisse utiliser notre code avec les données de Pôle Emploi, et ce y compris dans plusieurs mois. 

L'inconvénient est que du coup nous n'avons pas des données qui s'actualisent en permanence avec les nouvelles offres d'emploi comme lorsque l'on passe directement par l'API, car on crée une base de données à un instant t qui après n'est plus modifiée. Malheureusement, nous n'avons pas trop d'autres solutions si l'on veut pouvoir industrialiser le projet. On pourra simplement faire attention à réactualiser manuellement régulièrement la base de données en refaisant tourner le code "Cree_db_pole_emploi.py" pour fournir à l'utilisateur une base de données qui ne date pas trop.

## I. Le matching du CV avec les offres d'emploi
La première grosse partie de notre code doit nous permettre, à partir d'un CV sous format PDF, de trouver les 10 offres d'emploi de Pôle Emploi qui correspondent le plus à un utilisateur. 

Les grandes étapes sont les suivantes : 

### 1. Récupération des informations clés sur les offres d'emploi
On commence par récupérer uniquement les descriptions et les intitulés des offres de la base de données de Pôle Emploi, qui sont les inforamtions essentielles à recuillir pour pouvoir ensuite voir quelles offres matchent avec le CV. 
```ruby
def data_offres(db):

    import json

    with open(db, "r") as file:
      data = json.load(file)

    # Liste pour stocker les tuples (ID, description)
    Offres = []

    # Parcourir chaque emploi dans les résultats
    for emploi_resultat in data['resultats']:
        emploi_idV = emploi_resultat.get('id', None)
        emploi_id = emploi_resultat.get('intitule', None)
        description = emploi_resultat.get('description', None)

        if emploi_id is not None and description is not None:
            Offres.append([emploi_idV, emploi_id, description])

    return Offres
```

### 2. Convertir le CV en texte 
Ensuite, il nous a fallu trouver un algorithme permettant de convertir le CV passé en entré comme fichier PDF en texte facilement manipulable sous python. C'est ainsi que nous avons trouvé la librairie PyPDF2, qui nous permet de transformer tout le texte contenu dans le fichier PDF en une liste de mots.
> [!NOTE]
> PyPDF2 est une bibliothèque Python open-source qui permet de manipuler des fichiers PDF. Elle fournit des fonctionnalités permettant par exemple d'extraire du texte, defusionner ou diviser des fichiers PDF, ou encore d'extraire des
> métadonnées d'un texte. Vous pouvez retrouver la documentation ici : https://pypdf2.readthedocs.io/en/3.0.0/
```ruby
def extract_text_from_pdf(pdf_file: str) -> [str]:
    import PyPDF2
    import json
    import http.client
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader (pdf, strict=False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append (content)
        return pdf_text
```
### 3. Analyse du contenu du CV
Tout au long de ce projet, lorsqu'il était question d'analyser du texte, nous avons fait le choix d'utiliser la méthode de Machine Learning LDA. 

> [!NOTE]
> **LDA (Latent Dirichlet Allocation)** est une des techniques de Natural Language Processing les plus connues. C’est une méthode probabiliste qui repose sur de l’apprentissage non supervisé, basée sur l'hypothèse que les documents sont générés à
> partir d'un mélange de sujets, et chaque sujet est une distribution de mots. Son objectif est alors d’extraire les sujets et thèmes principaux, représentés par un ensemble de mots, qui apparaissent dans un texte. Elle fonctionne globalement
> ainsi :
> 1. Données d'entrée : Un ensemble de documents texte.
> 2. Prétraitement : Les documents sont prétraités pour la tokenisation, la suppression des mots vides, la normalisation, etc.
> 3. Construction d'un vocabulaire : Tous les mots uniques dans les documents sont collectés pour former un vocabulaire.
> 4. Création de la matrice de documents-termes : Chaque document est représenté sous forme d'un vecteur de la taille du vocabulaire, où chaque élément représente la fréquence d'un mot dans le document.
> 5. Entraînement du modèle LDA : L'algorithme LDA est utilisé pour trouver un certain nombre de sujets dans les documents et leur distribution respective.
> 6. Interprétation des sujets : Les mots les plus probables pour chaque sujet sont extraits, permettant d'interpréter le sujet.
> 7. Application du modèle : Une fois entraîné, le modèle peut être utilisé pour classifier de nouveaux documents en fonction de leur distribution de sujets.

Ainsi, une fois le CV transformé en texte, nous commençons par le nettoyer et le présenter sous la forme d'une unique chaîne de caractères, pour être sûrs que le modèle LDA puisse ensuite être correctement appliqué.
```ruby
def convert_CV(lien):
    import re

    extracted_text = extract_text_from_pdf(lien)
    CV_List = []

    for text in extracted_text:
        CV_List.append(text)

    CV_List_s = CV_List[0].splitlines()

    #Cette partie de l'algorithme est présente pour spliter les informations directement
    texte_seul = ' '.join(CV_List_s)  # Convertir la liste en une seule chaîne de texte
    texte_seul = re.sub(r'[^a-zA-ZÀ-ÖØ-öø-ÿ\s]', '', texte_seul)
    texte_seul = texte_seul.split()
    return texte_seul)
```
Puis cette chaîne de texte est tokenisée pour ne garder que les éléments importants présents dans le CV, et on crée un dictionnaire qui va permettre de stocker les topics identifiés dans le texte grâce au modèle LDA. 
```ruby
def biblio_CV(lien):

    from gensim import corpora
    from gensim.models import LdaModel
    from pprint import pprint

    # Exemple de corpus de documents
    documents = convert_CV(lien)

    # Tokenisation des documents en mots
    tokenized_documents = [doc.split() for doc in documents]

    # Création d'un dictionnaire à partir du corpus
    dictionary = corpora.Dictionary(tokenized_documents)

    # Création de la représentation du corpus en tant que sac de mots (BoW)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]

    # Création d'un modèle LDA
    lda_model = LdaModel(corpus, num_topics=3, id2word=dictionary)

    return lda_model, dictionary
```

### 4. Classement des offres d'emploi les plus pertinentes
Pour finir, la dernière étape de cette partie du code consiste à établir le classement des offres d'emploi qui matchent le plus avec le contenu du CV analyse grâce à la LDA. Pour cela, une fois que nous avons trouvé les topics les plus importants du CV, nous notons les descriptions des offres de Pôle Emploi suivant ces topics. On fait ensuite pour chaque offre une moyenne des scores obtenus sur les différents topics, et on classe alors toutes les offres d'emploi selon ce score. Les 10 offres d'emploi avec le meilleur score sont ainsi enregistrées dans un fichier en format JSON (top_offres), qui sera renvoyé à l'utilisateur. La fonction nous renvoie également la liste des ID des 10 offres du classement (resultats_id), car nous en aurons besoin par la suite pour récupérer les compétences requises pour chacun de ces emplois.

```ruby
def classifier_offres_lda(lien, top_n, db):

    import json

    # Liste pour stocker les résultats
    Offres=data_offres(db)
    resultats_classification = []
    resultats_id=[]

    lda_model, dictionary = biblio_CV(lien)

    # Parcourir chaque offre dans la liste Offres
    for offre_idV, offre_id, offre_description in Offres:
        # Tokenisation du document
        tokenized_doc = offre_description.split()

        # Convertir le document en une représentation BoW à l'aide du dictionnaire existant
        doc_bow = dictionary.doc2bow(tokenized_doc)

        # Obtention de la distribution des topics pour le document
        topic_distribution = lda_model.get_document_topics(doc_bow)

        # Calcul de la moyenne des scores pour chaque topic
        moyenne_scores = sum(score for topic, score in topic_distribution) / len(topic_distribution)

        # Ajout du tuple (ID de l'offre, moyenne des scores) à la liste des résultats
        resultats_classification.append({
            "Classement": 0,
            "ID de l'offre": offre_idV,
            "Intitulé de l'offre": offre_id,
            "Score": moyenne_scores
        })

    # Trier les offres par score de la meilleure à la moins bonne
    top_offres = sorted(resultats_classification, key=lambda x: x["Score"], reverse=True)[:top_n]

    for i, offre in enumerate(top_offres, start=1):
        offre["Classement"] = i
        resultats_id.append(offre["ID de l'offre"])

    # Enregistrer la liste des offres au format JSON
    nom_fichier_sortie_json = "classement_offres.json"
    with open(nom_fichier_sortie_json, 'w', encoding='utf-8') as fichier_sortie_json:
        json.dump(top_offres, fichier_sortie_json, ensure_ascii=False, indent=2)

    return resultats_id, top_offres
```

> [!NOTE]
> Nous avons pensé notre projet comme étant à destination des travailleurs en quête de reconversion profesionnelle. Ainsi, nous avons fait le choix de réaliser un classement des 10 offres d'emploi les plus pertinentes pour le profil de l'utilisateur, car nous nous sommes dit
> que cela laissait suffisamment de choix à celui-ci pour qu'il ne puisse garder ensuite parmi ces 10 propositions que les offres qui l'intéressent vraiment et lui plaisent personnellement le plus.

### 5. Test
Voici le classement que l'on peut obtenir à la suite de l'appel de la dernière fonction :
```ruby
resultats = classifier_offres_lda('/Users/menuebaptiste/Desktop/CV_Baptiste_MENUE.pdf', data_offres(), 10, database) # La database est celle contenant les offres de Pole Emploi
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

On peut voir que le résultat est cohérent car le CV passé en entrée est celui d'un élève ingénieur généraliste avec un profil orienté data, et donc que les offres qui ressortent sont totalement en accord avec ce profil. 

## II. Trouver les compétences manquantes 

La deuxième partie de notre code consiste à récupérer les compétences demandées pour les 10 offres d'emploi renvoyées à l'étape précédente, puis à analyser de nouveau le contenu du CV pour identifier quelles compétences sont manquantes dans le profil de l'utilisateur. Cette partie est très similaire à celle précédente, excepté qu'ici on se concentre uniquement sur les compétences mentionnées dans les offres d'emploi, et qu'on cherche à faire une analyse de dissimilarité entre celles-ci et le CV plutôt qu'une analyse de simialrité. 

### 1. Récupération des compétences requises 
On commence par de nouveau explorer la base de données des offres de Pôle Emploi, sauf que cette fois-ci on se concentre sur les 10 offres que nous avons retenues dans la première partie du code. Cela est possible grâce à la fonction "classifier_offres_lda" présentées au I.4. qui nous renvoie la liste des ID des offres du classement et que nous pouvons ici passer en entrée. Nous pouvons alors récupérer, pour chacune des offres, toutes les compétences qui sont mentionnées et les stocker dans une liste.
```ruby
def data_competence(id_emploi, db):
    import json

    with open(db, "r") as file:
      data = json.load(file)

    # Liste pour stocker les tuples (ID, description)
    Competences = []

    # Parcourir chaque emploi dans les résultats
    for id in id_emploi:
        Comp1=[id]
        for emploi_resultat in data['resultats']:
            emploi_id = emploi_resultat.get('id', None)
            if emploi_id == id:
                emploi_competences = emploi_resultat.get('competences', None)
                if emploi_competences is not None:
                    for emploi_libelle in emploi_competences:
                        if 'libelle' in emploi_libelle:
                            Comp1.append(emploi_libelle['libelle'])
        if len(Comp1)>1:
            Competences.append(Comp1)
    return Competences
```
### 2. Classement des compétences qui sont le moins présentes dans le CV
Dans la mesure où les fonctions permettant de convertir le CV et d'analyser son contenu grâce à la méthode LDA ont déjà été définies dans la partie I, on peut ici directement les réutiliser. Nous avons alors uniquement à reprendre l'algorithme utilisé pour réaliser le classement des offres d'emploi les plus pertinentes, mais en appliquant la logique inverse : en effet, on veut cette fois, parmi la liste des compétences requises, trouver celles qui ont le score le plus faible en fonction des topics identifiés dans le CV. Ce seront alors ces compétences-ci qui sont les moins similaires au contenu du CV, et donc qui manquent à l'utilisateur pour répondre au mieux aux offres d'emploi qui lui sont proposées.
```ruby
def classifier_competence_lda(lien, Competences):
    # Liste pour stocker les résultats
    resultats_classification = []

    lda_model, dictionary = biblio_CV(lien)

    # Parcourir chaque competence dans la liste Competences
    for competence in Competences:
        id_offre=competence[0]
        liste_par_offre=[]
        liste_comp=competence[1:]
        for comp in liste_comp:
            # Tokenisation de la chaîne de texte
            tokenized_doc = comp.split()

            # Convertir le document en une représentation BoW à l'aide du dictionnaire existant
            doc_bow = dictionary.doc2bow(tokenized_doc)

            # Obtention de la distribution des topics pour le document
            topic_distribution = lda_model.get_document_topics(doc_bow)

            # Calcul de la moyenne des scores pour chaque topic
            moyenne_scores = sum(score for topic, score in topic_distribution) / len(topic_distribution)

            # Ajout du tuple (nom de la compétence, moyenne des scores) à la liste des résultats pour cette offre
            liste_par_offre.append((comp, moyenne_scores))

        # Tri des tuples selon le score croissant
        sorted_tuples = sorted(liste_par_offre, key=lambda x: x[1])

        # Select the first two tuples and remove the score
        top_two_tuples = [t[0] for t in sorted_tuples[:2]]

        # Ajout des résultats obtenus pour cette offre à la liste de tous les résultats
        resultats_classification.append([[id_offre] + top_two_tuples])

    return(resultats_classification)
```
Cette fonction renvoie une liste de 10 listes (ou moins si certaines offres ne demandant pas de compétences particulières), chaque sous-liste contenant l'ID de l'offre d'emploi en question et les 2 compétences qui ont obtenu le plus petit score lors du matching avec le CV.
> [!NOTE]
> Nous avons fait le choix pour chaque offre d'emploi de ne renvoyer que 2 compétences manquantes à l'utilisateur. En effet, comme il y a 10 offres d'emploi proposées, cela faisait très vite monter le nombre de formations professionnelles à proposer à l'utilisateur si l'on augmentait le
> nombre de compétences manquantes pour chaque offre, et donnait des résultats peu lisibles. De plus, nous avons estimé que 2 compétences à acquérir, et donc potentiellement 2 formations professionnelles à suivre, était un effort déjà important à fournir pour l'utilisateur et suffisant
> pour augmenter son employabilité.

### 3. Test

On teste l'algorithme en passant en entrée un CV d'étudiante ingénieure qui a déjà travaillé en banque et en centre aéré. On obtient pour le classement des offres d'emploi le résultat suivant : 
```ruby
[{'Classement': 1, "ID de l'offre": '162MCBY', "Intitulé de l'offre": 'Comptable fournisseurs (H/F)',  'Score': 0.333333358168602},
 {'Classement': 2, "ID de l'offre": '162LVZW', "Intitulé de l'offre": 'Projeteur Electrotechnique (H/F)', 'Score': 0.3333333532015483},
 {'Classement': 3, "ID de l'offre": '162KTDX', "Intitulé de l'offre": 'Chauffeur / Chauffeuse de poids lourd', 'Score': 0.3333333532015483},
 {'Classement': 4, "ID de l'offre": '162GTNV', "Intitulé de l'offre": 'Tailleur / Tailleuse de pierre (H/F)', 'Score': 0.3333333532015483},
 {'Classement': 5, "ID de l'offre": '162FVCC', "Intitulé de l'offre": 'Manipulateur / Manipulatrice en imagerie médicale', 'Score': 0.3333333532015483},
 {'Classement': 6, "ID de l'offre": '162KSZN', "Intitulé de l'offre": 'Ouvrier / Ouvrière Voiries et Réseaux Divers -VRD-', 'Score': 0.3333333507180214},
 {'Classement': 7, "ID de l'offre": '162LZHP', "Intitulé de l'offre": "Ouvrier polyvalent / Ouvrière polyvalente d'entretien des bâtiments", 'Score': 0.33333335009713966},
 {'Classement': 8, "ID de l'offre": '162MFHM', "Intitulé de l'offre": 'DIRECTEUR MICRO CRECHE (H/F)', 'Score': 0.3333333482344945},
 {'Classement': 9, "ID de l'offre": '162MCXY', "Intitulé de l'offre": 'Comptable clientèle (H/F)', 'Score': 0.3333333482344945},
 {'Classement': 10, "ID de l'offre": '162LQWR', "Intitulé de l'offre": "Apporteur d'Affaires Matériels Agricoles (H/F)", 'Score': 0.3333333482344945}]
```
La deuxième partie du code nous permet alors d'identifier les compétences manquantes suivantes :
```ruby
[[['162MCBY',
   'Établir un état de rapprochement bancaire',
   'Organiser et contrôler un approvisionnement']],
 [['162LVZW',
   'Comprendre, interpréter des données et documents techniques',
   'Relever, contrôler, ajuster des mesures et dosages']],
 [['162KTDX',
   'Organiser le chargement des marchandises dans le véhicule',
   'Définir un itinéraire en fonction des consignes de livraison']],
 [['162GTNV',
   'Déterminer le positionnement des pierres',
   "Sélectionner des blocs de pierre selon les caractéristiques de l'objet à tailler"]],
 [['162FVCC',
   'Développer un cliché médical',
   "Préparer les accessoires (films, caches, matériel médicochirurgical, ...) et informer la personne sur le déroulement de l'examen"]],
 [['162KSZN',
   "Sécuriser le périmètre d'intervention",
   "Positionner des repères d'ouvrages sur un chantier"]],
 [['162LZHP',
   'Préparer un support, une matière',
   "Entretenir l'installation sanitaire, de chauffage et de production d'eau chaude"]],
 [['162MFHM',
   "Recueillir les informations sur l'environnement de vie et l'état de santé de l'enfant",
   'Organiser des formations en prévention des risques']],
 [['162MCXY',
   'Chiffrage/calcul de coût',
   'Établir, mettre à jour un dossier, une base de données']],
 [['162LQWR',
   'Établir un plan de tournée de prospection (ciblage, interlocuteurs, préparation de dossiers techniques)',
   'Conseiller, accompagner une personne']]]
```
Le résultat des compétences est cohérent avec les offres d'emploi, et ces compétences sont effectivement des compétences qui sont manquantes dans le profil de la personne dont on a utilisé le CV (exceptées peut-être les compétences renvoyées pour l'offre n°9 de Comptable clientèle, ID 162MCXY).

## III. Proposer des formations professionnelles adaptées 

La dernière grande partie du code doit nous permettre de renvoyer les formations professionnelles qui vont permettre à l'utilisateur d'acquérir les compétences manquantes identifiées dans la partie II. 

> [!NOTE]
> Nous n'avons pas trouvé sur le site des données Pôle Emploi ou sur data.gouv d'API pour les formations professionnelles. Cela nous aurait permis d'avoir des données actualisées en permanence, mais nous avons malheureusement uniquement trouvé des données statiques téléchargeables sous
> format csv. Nous avons donc fait le choix d'utiliser comme base de données des formations celle disponible sur data.gouv.fr contenant les formations professionnelles pouvant être financées à l'aide du Compte personnel de formation (CPF). Cela nous a semblé être un bon choix car l'offre
> de formations est très large, tout le monde y a droit grâce à son CPF et les données sont mises à jour de manière quasiment quotidienne. Le fichier csv des formations professionnelles que nous utiliserons a ainsi été téléchargé le 10/01/2024 depuis le lien suivant :
> https://www.data.gouv.fr/fr/datasets/moncompteformation-loffre-de-formation/#/resources.  
> Pour une meilleure pertinence des résultats, il faudrait re-télécharger régulièrement cette base de données afin d'en fournir une plus actualisée lors de l'utilisation de notre code. 

### 1. L'algortihme de matching des compétences manquantes avec les formations

Une fois de plus, il s'agit essentiellement de faire du Natural Language Processing, mais cette fois non pas sur un document PDF (le CV) mais sur un document CSV (la liste des formations professionnelles). Nous avons fait le choix cette fois de varier nos méthodes et de ne pas utiliser la librairie PyPDF2 et la technique de LDA mais plutôt une vectorisation de texte par la méthode TF-IDF et une analyse de similarité cosinus, grâce aux fonctions de la libraire sklearn.

> [!NOTE]
> La **vectorisation TF-IDF (Term Frequency - Inverse Document Frequency)** est une technique de pondération utilisée en traitement du langage naturel (NLP) pour évaluer l'importance d'un mot dans un document par rapport à un ensemble de documents. Le calcul de TF-IDF se base sur deux
> composantes :
> 1. La fréquence d'un terme dans un document (TF): Plus le mot m apparait dans le document d, plus sa valeur TF est élevée.  La formule de base est : **TF(m, d) = nb_occurrences(m, d) / nb_mots_total(d)**.
> 2. La rareté d'un terme dans un ensemble de documents (IDF): Plus le mot m est rare dans l'ensemble de documents D, plus sa valeur IDF est élevée. La formule de base est : **IDF(m, D) = log(nb_documents(D) / nb_documents_contenant(m, D))**.
> 3. Le calcul de TF-IDF est ainsi le produit de TF et IDF : **TF-IDF(m, d, D) = TF(m, d) * IDF(m, D)**. Cette pondération permet de donner plus d'importance aux mots fréquents dans un document mais rares dans l'ensemble des documents.

> [!NOTE]
> La **similarité cosinus** est une mesure utilisée en analyse de texte et en traitement du langage naturel pour évaluer la similitude entre deux vecteurs de caractéristiques. Elle consiste à calculer le cosinus de l'angle entre deux vecteurs A et B :  
> **Similarité cosinus (A,B) = produit scalaire entre A et B /( Normme euclidienne de A * Norme euclidienne de B )**  
> Le résultat ainsi obtenu est compris entre -1 et 1. Une similarité de 1 indique que les vecteurs sont identiques, 0 indique une indépendance linéaire (pas de similitude), et -1 indique une dissimilarité parfaite.  

La méthode utilisée ici est ainsi la suivante :
1. On crée une liste de phrases avec les informations qui nous intéressent concernant toutes les formations professionnelles proposées.  
2. Pour chaque offre d'emploi, on ajoute chaque compétence manquante dans la liste précédente sous forme d'une phrase également.  
3. On crée alors une matrice TF-IDF pour convertir ces phrases en une matrice de caractéristiques, une des dimensions de la matrice étant les formations et l'autre la compétence manquante en question.
4. On calcule ensuite la similarité cosinus entre la compétence cherchée et les formations grâce à la matrice précédente.  
5. On classe les formations en fonction de leur similairité avec la compétence et on ne garde que les 3 meilleures.

```ruby
def formation(liste_comp, catalogue_formations):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import json

    df = pd.read_csv(catalogue_formations, on_bad_lines='skip', sep=';', low_memory=False)

    desired_columns = ['numero_formation', 'intitule_formation', 'points_forts']
    df_selected = df[desired_columns]

    resultat_du_dictionnaire = df_selected.to_dict(orient='records')

    nom_fichier_sortie = "resultats_formations.json"

    # Liste pour stocker les résultats au format JSON
    resultats_json = []

    for comp_par_emploi1 in liste_comp:
        comp_par_emploi2 = comp_par_emploi1[0]
        id_offre, competence_cherche_list = comp_par_emploi2[0], comp_par_emploi2[1:]

        # Dictionnaire pour stocker les résultats
        resultat_par_competence = {"Id de l'offre d'emploi": id_offre, "Competences": []}

        for competence_cherche in competence_cherche_list:
            # Liste des phrases dans resultat_du_dictionnaire
            phrases = [str(item.get('points_forts', [])) for item in resultat_du_dictionnaire]

            # Ajout de la phrase d'intérêt à la liste
            phrases.append(competence_cherche)

            # Création de la matrice TF-IDF
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(phrases)

            # Calcul de la similarité du cosinus entre les phrases
            similarites = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

            # Obtenir les indices triés des phrases les plus similaires
            indices_similaires = similarites.argsort()[0][::-1]

            # Limiter le nombre de correspondances à ajouter à la liste de formations
            limite_correspondances = 3
            formations = [resultat_du_dictionnaire[i] for i in indices_similaires[:limite_correspondances]]

            # Stocker les résultats dans le dictionnaire
            resultat_competence = {"Competence": competence_cherche, "Formations": []}

            for formacao in formations:
                formation_dict = {
                    "Numéro formation": formacao['numero_formation'],
                    "Intitulé": formacao['intitule_formation'],
                    "Points forts": formacao['points_forts']
                }
                resultat_competence["Formations"].append(formation_dict)

            resultat_par_competence["Competences"].append(resultat_competence)

        resultats_json.append(resultat_par_competence)

    # Enregistrer la liste des résultats au format JSON
    with open(nom_fichier_sortie, 'w', encoding='utf-8') as fichier_sortie_json:
        json.dump(resultats_json, fichier_sortie_json, ensure_ascii=False, indent=2)

    return resultats_json
```
Cette fonction prend en entrée la liste des compétences manquantes à l'utilisateur ainsi que la base de données csv contenant le détail des formations professionnelles, et renvoie un document JSON contenant pour chacune des 10 offres et chacune des 2 compétences associées, 3 formations qui devraient permettre d'acquérir cette compétence --> soit au total 60 formations.   
Nous avons fait le choix d'avoir un format JSON en sortie de manière à avoir un résultat plus clair et plus présentable pour l'utilisateur.

> [!NOTE]
> On voit que le nombre de suggestions de formations renvoyé est très important. Toutefois, il s'est avéré nécéssaire pour chaque compétence de fournir plusieurs propositions de formations, car nous nous sommmes rendu compte que les résultats ne sont pas toujours tous pertinents. Cela est
> notamment liés au fait  que les descriptions des formations ne sont pas toujours très complètes et détaillées, ce qui rend le matching plus difficile, ainsi qu'au fait que les mots et phrases utilisées pour décrire les compétences sont parfois très génériques et donc peuvent être
> reliées à une très grande variété de formations (par exemple "personnel", "contrôler", "organiser", "comprendre"...)  
> Nous nous sommes ainsi dit qu'en proposant 3 formations par compétence, cela permettait à l'utilisateur d'avoir suffisamment de choix pour sélectionner la formation qui soit vraiment la plus pertinente en fonction de son profil, de ses besoins, de ses capacités, et des offres d'emploi
> qui l'intéressent le plus.

### 2. Test

## Finalisation 

