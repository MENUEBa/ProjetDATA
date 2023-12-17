# Projet DATA

MENUE Baptiste
BUTTI GARNIER Zoe
BARATA Wendel
DE OLIVEIRA Hassan Augusto B.

## À partir des données de Pôle Emploi, construire un modèle prédictif pour répondre à un besoin business

**Objectif** : Réaliser de bout en bout un projet de Data Science dans un contexte business

### 0. Comprendre et analyser la donnée 

Avant de réfléchir à un besoin business, et donc au sujet de notre projet, nous avons commencé par nous connecter à l'API de Pôle Emploi et requêter sur celle-ci afin de voir le type des données que nous allions devoir étudier.

Tout d'abord, nous avons souhaité trouver le moyen de ne plus devoir passer par l'API et systématiquement devoir copier coller l'accès pour ensuite le mettre dans notre jupyter NoteBook. C'est en quelque sorte le début de l'automatisation de notre projet.

> [!NOTE]
> Nous avons décidé de couper le code en différentes parties pour que vous puissiez comprendre notre cheminement. Nous avons ensuite récapitulé le code final en entier

**Code Requete.py**
> {"resultats":[{"id":"162MRQR","intitule":"Enseignant(e) de la conduite et  de la sécurité routière (H/F)","description":"Nous recherchons un(e) enseignant(e), titulaire du BEPECASER ou du TP ECS avec la mention B et/ou la mention BE et/ou  A serait un plus.\n\nOuverture de l'Auto Ecole du lundi au samedi. Votre p .... etc 

> [!CAUTION]
> Nous avons mis en annexe l'ensemble des packages à installer dans Extension_a_avoir.py. Il faut aussi faire attention, les POST et GET doivent être séparés car on peut avoir des problèmes si on fait tout en même temps.

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
- En fonction des résultats, proposer des formations professionnelles complémentaires proposées par l'Etat et qui permettraient de mieux correspondre aux résultats
- Faire une application de veille par mail qui permettrait de renvoyer les nouvelles annonces susceptibles de convenir à notre CV et donc les formations professionnelles associées

En effet, le simple matching des CV nous semblait être une idée intéressante et accessible mais peu originale. C'est pour cela que nous souhaitons également complexifier et porter notre projet plus loin en ajoutant la proposition de formations professionnelles complémentaires. En ce qui concerne la dernière idée, après nous être renseignés sur la question, nous sommes arrivés au constat que celle-ci était peut-être un peu trop ambitieuse.

**Conclusion**

Objectif final : faire une application qui, à partir d'un CV, propose un matching sur plusieurs offres d'emploi, puis renvoie vers des formations complémentaires adaptées et proposées par l'Etat pour les emplois où il y aurait des lacunes en termes de compétences notamment.

La démarche consistera donc ici à prédire, à partir des données d'un CV fourni et de celles présentes sur Pôle Emploi, quelles offres d'emploi sont les plus proches du profil d'un professionnel. Ensuite, il faut identifier quelles sont les différences notables, en termes de connaissances et de compétences, entre le CV de la personne fourni et les prérequis demandés dans l'offre d'emploi. Finalement, à partir des différences identifiées, il faudra prédire quelle formation professionnelle existante permettrait de combler ces différences et d'apporter au professionnel les connaissances et compétences manquantes.

### 3. Les étapes du code

Ensuite, nous avons déterminé que pour pouvoir réaliser cette idée business, nous allions devoir procéder en deux temps : dans un premier temps, réaliser le matching de CV, et, dans un second temps, proposer les formations professionnelles pertinentes. 

Pour l'instant, nous nous sommes essentiellement penchés sur la première partie. 

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

#
## I. Le matching de CV

### 1. Transformer les offres en tuples 

Pour rappel, nos données se trouvernt sous format JSON, il fallait donc trouver un moyen de les rendre plus exploitables. 

**Resultat de l'algorithme Offres_Tuple.py**

>[['Enseignant(e) de la conduite et  de la sécurité routière (H/F)', "Nous recherchons un(e) enseignant(e), titulaire du BEPECASER ou du TP ECS avec la mention B et/ou la mention BE et/ou  A serait un plus.\n\nOuverture de l'Auto Ecole du lundi au samedi. Votre planning sera à définir avec l'employeur suivant vos disponibilités lors de l'entretien. 35h/h - pas de temps partiel.\n\nLe taux horaire dépendra des différentes formations dispensées.\n\nAvantages sociaux : mutuelle entreprise, carte restaurant, heures supplémentaires rémunérées, 2 jours de congés consécutifs par semaine, 1 samedi par mois, voiture de service pour déplacement professionnel. Prime occasionnelle."], ['JOB HIVER Réceptionniste en établissement touristique(H/F) (H/F)', 'Réceptionniste en Résidence de Tourisme *** sur la station de LA PLAGNE.\nCheck in - check out / Renseignement client / Réponse téléphonique / Accueil physique en front office.\nSAISON HIVER  2023-24 à partir de DEBUT DECEMBRE 2023.'] ... etc

Nous avons donc une liste de listes avec l'intitulé et la description de chaque offre, beaucoup plus facile à parcourir.

### 2. Convertir le PDF en fichier txt  

**Resulat de l'algorithme Convert_PDF.py**

>['COMPTABLE', 'SENIORAdeline', 'Pannier', 'PROFIL', 'PERSONNEL', 'Je', 'suis', 'une', 'comptable', 'de', 'ans', 'avec', 'une', 'expérience', 'en', 'comptabilité', 'dentreprise', 'et', 'en', 'budgétisation', 'financière', 'Je', 'recherche', 'un', 'poste', 'dans', 'un', 'environnement', 'de', 'travail', 'dynamique', 'COMPÉTENCES', 'ESSENTIELLES', 'Comptabilité', 'des', 'salaires', 'et', 'calcul', 'des', 'impôts', 'Prévisions', 'budgétaires', 'Analyse', 'des', 'coûts', 'et', 'automatisation', 'du', 'système', 'Comptes', 'clientscomptes', 'fournisseurs', 'Audit', 'interne', 'CONTACTEZMOI', 'Téléphone', 'Mobile', 'Ad ... etc

Grâce à ces chaînes de caractères, nous allons pouvoir les tokeniser et ensuite faire ressortir des topics à l'aide de l'algorithme de Natural language processing -> LDA 

> [!NOTE]
> Dans cet exemple, c'est un CV de comptable qui est utilisé.

> [!CAUTION]
> Le CV type a été mis dans le Jupyter Notebook, si vous voulez le faire depuis l'ordinateur il suffit de mettre le lien, cf **Design.pdf**

### 3. Créer les topics

**Resulat de l'algorithme CV_Topics.py**

>[(0,
  '0.077*"et" + 0.033*"les" + 0.018*"avec" + 0.018*"chef" + 0.017*"Domarin" + '
  '0.017*"une" + 0.016*"de" + 0.011*"Licence" + 0.011*"CONTACTEZMOI" + '
  '0.011*"Adresse"'),
 (1,
  '0.062*"des" + 0.055*"en" + 0.024*"la" + 0.018*"de" + 0.018*"dossiers" + '
  '0.017*"un" + 0.016*"Je" + 0.013*"et" + 0.011*"réguliersComptable" + '
  '0.011*"Photographie"'),
 (2,
  '0.125*"de" + 0.035*"du" + 0.023*"comptabilité" + 0.021*"Diplômée" + '
  '0.021*"et" + 0.016*"dhonneur" + 0.015*"Condorcet" + 0.014*"impôts" + '
  '0.010*"transactions" + 0.010*"passif"')]

Nous pouvons donc voir clairement ici les topics que le modèle nous a généré, nous avons fait le choix d'en sélectionner que 3 car en-dessous, cela n'était pas pertinent et si nous faisions plus, nous nous retrouvions avec des topics inutiles 

```ruby
# Obtention de la distribution des topics pour la description que nous voudrons par la suite ("doc_bow" représente une description)
topic_distribution = lda_model.get_document_topics(doc_bow)
```

### 4. Le classement et les résultats

> [!NOTE]
> Cette fois, nous n'utilisons non plus un CV de comptable mais celui de l'un des membres du groupe. 

**Resulat de l'algorithme Classement_offres.py**

```
Classement 1 - ID de l'offre : Chef.fe de Projet Technique en Data & Big Data (H/F), Score : 0.49892330169677734
Classement 2 - ID de l'offre : Data Scientist / Développeur.se Dataiku (H/F), Score : 0.49887265264987946
Classement 3 - ID de l'offre : Coordinateur du Conseil Local de Santé Mentale (H/F), Score : 0.4986680895090103
Classement 4 - ID de l'offre : Chargé administratif et financier (H/F), Score : 0.4985301345586777
Classement 5 - ID de l'offre : Responsable d'Atelier de Production (H/F), Score : 0.49841374158859253
Classement 6 - ID de l'offre : DIRECTEUR MICRO CRECHE (H/F), Score : 0.49832184612751007
Classement 7 - ID de l'offre : Ingénieur.e DevOps / DataOps (H/F), Score : 0.49832025170326233
Classement 8 - ID de l'offre : Chef.fe de projet digital et tech (H/F), Score : 0.4982679784297943
Classement 9 - ID de l'offre : Infirmier / Infirmière (H/F), Score : 0.49826668202877045
Classement 10 - ID de l'offre : CONDUCTEUR DE CHANTIER Electrotechnique Industriel (H/F), Score : 0.49822111427783966
```

Nous avons donc ici le résultat final de notre matching du CV avec les emplois le 01.12.2023.
Au final nous pouvoir voir que le matching est assez cohérent puisque par exemple on peut voir qu'en première position on a **"Chef.fe de Projet Technique en Data & Big Data"**.

### 5. Automatisation

Maintenant que nous avons créé toutes les fonctions nécéssaires au bon fonctionnement de notre algorithme nous n'avons plus qu'à faire appel à celui-ci 

```ruby
# Obtention de notre classement directement à la suite de l'appel de cette fonction
resultats = classifier_offres_lda('Design.pdf', data_offres(), 10)
```

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
