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
> Nous avons mis en annexe l'ensemble des chose à installer dans Extension_a_avoir.py

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





