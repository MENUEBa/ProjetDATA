# Projet DATA

MENUE Baptiste
BUTTI GARNIER Zoe
BARATA Wendel
DE OLIVEIRA Hassan Augusto B.

## Le concept 

### A partir des données de Pôle Emploi, construire un modèle prédictif pour

**Objectif** : Réaliser de bout en bout un projet de Data Science dans un contexte business

1. Prendre conscience de la donnée 

Nous avons beaucoup réfléchi à la question. Nous nous sommes déjà dans un premier temps connecter à l'API de pôle emploi pour voir le type des données que nous allons devoir étudier

Dans un premier temps nous avons trouver le moyen de ne plus passer par l'API et de devoir copier coller l'accès pour pouvoir ensuite le mettre dans notre jupyter NoteBook. C'est en quelque sorte le début de l'automatisation de notre projet 

> [!NOTE]
> Nous avons décider de couper le code en différent partie pour que vous puissez comprendre notre cheminement. Nous avons ensuite récapituler le code final en entier

**Code Requete.py**
> {"resultats":[{"id":"162MRQR","intitule":"Enseignant(e) de la conduite et  de la sécurité routière (H/F)","description":"Nous recherchons un(e) enseignant(e), titulaire du BEPECASER ou du TP ECS avec la mention B et/ou la mention BE et/ou  A serait un plus.\n\nOuverture de l'Auto Ecole du lundi au samedi. Votre p .... etc 

> [!CAUTION]
> Nous avons mis en annexe l'ensemble des chose à installer dans Extension_a_avoir.py. Il faut aussu faire attention les POST et GET doivent peut-être séparer car on peut avoir des problèmes si on fait tout en même temps

**Conclusion** 

Nous avons donc un fichier Json organiser de la manière suivante : 

- Resultats 
    - id 
    - intitulé 
    - description
    - ..

Chaque emplois sont donc organisés de la même manière. Nous comprenons donc que nous allons pouvoir exploiter le texte de la description qui est toujours présente dans chaque emplois. 

2. Le projet 

une fois que nous avons vu comment se disposait les données collectées nous avons réfléchi à une application business. 

Nous avions 2 grandes idées : 
- le matching des CV 
- Faire une application de veille de mail qui permetterait de renvoyer les nouvelles annonces susceptible de convenir à notre CV 

Pour finir nous avons pris une idée un peu mixé de ces deux idées car nous pensions que le matching des CV était plutôt accessible mais que tout le monde aller faire ce type de projet. 

En ce qui concerne le deuxième projet celui-ci était peut-être un pue trop ambitieux

**Conclusion**

Nous voulons faire une application qui suite à un CV propose un matching sur plusieur emplois et par la suite proposer des formation adaptées pour les emplois ou il y aurait des lacunes de compétences

3. Les étapes du code

Dans les grandes lignes le code se décomposera ainsi : 

- Faire la requête pour récuperer facilement les données de l'API
- Transformer les données pour ne récupérer que les descriptions et les intitulés dans le but d'avoir les données sur l'emploi en question et de pouvoir ensuite voir si il matche avec le CV grâce à un algorithme LDA de machine learning
- Une fois les données récupérées nous allons en faire des couples de tuples pour les annonces ((Id,description)) 
- Il faut convertir le fichier PDF en une base de donnée (text) 
- Une fois que nous avons transformé le fichier en texte nous allons le Tokeniser pour ne garder que les éléments important du CV
- Il suffit ensuite de créer un dictionnaire afin de créer des topics grâce au modèle LDA (pour le CV en question)
- Pour finir une fois que nous avons trouvé les Topics du CV nous allons noter suivant ces topics chaque description des emplois. Faire une moyenne des scores pour ensuite en sortir les emplois qui s'en rapproche le plus. 
- L'obejectif final est de faire la même chose dans l'autre sens avec les 10 descriptions qui ont eu le meilleur score, faire ressortir des Topics et voir ce qui ont le moins de matche avec le CV pour voir qu'elle type de formation il manquerait à ces personnes

> [!NOTE]
> LDA(Latent Dirichlet Allocation) est une des techniques de NLP les plus connues. C’est une méthode qui repose sur de l’apprentissage non supervisée, et dont l’objectif est d’extraire les sujets principaux, représentés par un ensemble de mots, qui apparaissent dans une collection de documents.

6. Transformer les offres en Tuples 

Pour rapple la forme de nos données se trouver sous la forme de JSON, il fallait donc trouver un moyen de les rendre plus exploitable 

**Resultat de l'algorithme Offres_Tuple.py**

>[['Enseignant(e) de la conduite et  de la sécurité routière (H/F)', "Nous recherchons un(e) enseignant(e), titulaire du BEPECASER ou du TP ECS avec la mention B et/ou la mention BE et/ou  A serait un plus.\n\nOuverture de l'Auto Ecole du lundi au samedi. Votre planning sera à définir avec l'employeur suivant vos disponibilités lors de l'entretien. 35h/h - pas de temps partiel.\n\nLe taux horaire dépendra des différentes formations dispensées.\n\nAvantages sociaux : mutuelle entreprise, carte restaurant, heures supplémentaires rémunérées, 2 jours de congés consécutifs par semaine, 1 samedi par mois, voiture de service pour déplacement professionnel. Prime occasionnelle."], ['JOB HIVER Réceptionniste en établissement touristique(H/F) (H/F)', 'Réceptionniste en Résidence de Tourisme *** sur la station de LA PLAGNE.\nCheck in - check out / Renseignement client / Réponse téléphonique / Accueil physique en front office.\nSAISON HIVER  2023-24 à partir de DEBUT DECEMBRE 2023.'] ... etc

Nous avons donc une liste de liste avec intitulé et description beaucoup plus facilement parcourable

5. Convertir le PDF en fichier txt  

**Resulat de l'algorithme Convert_PDF.py**

>['COMPTABLE', 'SENIORAdeline', 'Pannier', 'PROFIL', 'PERSONNEL', 'Je', 'suis', 'une', 'comptable', 'de', 'ans', 'avec', 'une', 'expérience', 'en', 'comptabilité', 'dentreprise', 'et', 'en', 'budgétisation', 'financière', 'Je', 'recherche', 'un', 'poste', 'dans', 'un', 'environnement', 'de', 'travail', 'dynamique', 'COMPÉTENCES', 'ESSENTIELLES', 'Comptabilité', 'des', 'salaires', 'et', 'calcul', 'des', 'impôts', 'Prévisions', 'budgétaires', 'Analyse', 'des', 'coûts', 'et', 'automatisation', 'du', 'système', 'Comptes', 'clientscomptes', 'fournisseurs', 'Audit', 'interne', 'CONTACTEZMOI', 'Téléphone', 'Mobile', 'Ad ... etc

Grâce à ces chaine de caractères nous allons pouvoir les tokeniser et pouvoir ensuite faire ressortir des topics à l'aide de l'algorithme de Natural language processing -> LDA 

> [!CAUTION]
> Dans l'agorithme j'ai mis le CV type dans mon Jupyter Notebook, si vous voulez le faire depuis l'ordinateur il suffit de mettre le lien cf **Design.pdf**

6. Créer les topics

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

Nous pouvons donc voir clairement ici les topics que le modèle nous a généré, nous avons fait le choix d'en séléctionner que 3 car en dessous, cela n'était pas pertinent et si nous faisions plus, nous nous retrouvions avec des topics inutiles 

> [!NOTE]
> c'est un CV de comptable

```ruby
# Obtention de la distribution des topics pour la description que nous voudrons par la suite ("doc_bow" représente une description)
topic_distribution = lda_model.get_document_topics(doc_bow)
```

7. Le classement et les résultats

**Resulat de l'algorithme CV_Topics.py**

>Classement 1 - ID de l'offre : Chargé administratif et financier (H/F), Score : 0.3333333532015483
Classement 2 - ID de l'offre : ASM73 Responsable de salle en village vacance (H/F), Score : 0.3333333532015483
Classement 3 - ID de l'offre : Mécanicien / Mécanicienne automobile confirmé(e) (H/F), Score : 0.3333333532015483
Classement 4 - ID de l'offre : éleveur - berger (h/f), Score : 0.3333333532015483
Classement 5 - ID de l'offre : Technicien de maintenance et dépannage chaudière (H/F), Score : 0.3333333532015483
Classement 6 - ID de l'offre : Employé / Employée de rayon libre-service (H/F), Score : 0.3333333532015483
Classement 7 - ID de l'offre : Enseignant(e) de la conduite et de la sécurité routière (H/F), Score : 0.3333333507180214
Classement 8 - ID de l'offre : Conducteur d'engin (H/F), Score : 0.3333333482344945
Classement 9 - ID de l'offre : Mécanicien maintenance des systèmes climatiques (H/F), Score : 0.3333333482344945
Classement 10 - ID de l'offre : Canalisateur (H/F) PLEF63800, Score : 0.3333333482344945

Nous avons donc ici le résultat final de notre matching du CV avec les emplois le 01.12.2023. 
Au final nous pouvoir voir que le matching est assez cohérent avec le poste ici par exemple on peut voir qu'en première position on a **"Chargé administratif et financier"**. Nous avons utilisé ici un CV de comptable