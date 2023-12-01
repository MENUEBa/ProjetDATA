# Projet DATA

MENUE Baptiste/ BUTTI GARNIER Zoe

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





