# -*- coding: utf-8 -*-
"""to_run.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vg1dZ_oFPkNyQpYAJQYpZHlXRbLovB-P
"""

pip install PyPDF2

CV='CV-Zoe_Butti_Garnier.pdf'
database='database.json'
csv_formations='moncompteformation_catalogueformation.csv'

# Pour récupérer les offres d'emploi qui matchent avec mon CV
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
    return texte_seul

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

id_emploi_resultat, classement_offres = classifier_offres_lda(input, 10, database)

id_emploi_resultat

classement_offres

# Pour identifier les compétences qui me manquent pour ces offres d'emploi

# data_competence recupère les compétences associées aux offres d'emploi qui me sont proposées
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

# Parmi les compétences nécéssaires, identifie celles qui me manquent
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

test=data_competence(id_emploi_resultat, database)
test

liste_comp=classifier_competence_lda(input, test)
liste_comp

# Identifier les formations qui permettent d'acquérir ces compétences

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

formation(liste_comp)

def final(CV, database, catalogue_formations):
  id_emploi_resultat, classement_offres = classifier_offres_lda(CV, 10, database)
  liste_comp=data_competence(id_emploi_resultat, database)
  liste_comp_manquantes=classifier_competence_lda(CV, liste_comp)
  resultats_formations=formation(liste_comp_manquantes, catalogue_formations)
  return classement_offres, resultats_formations

classement_offres, resultats_formations=final(input, database)

classement_offres

resultats_formations

pip install gradio

import gradio as gr
import json
import http.client
from io import BytesIO
import tempfile

iface = gr.Interface(fn=final, inputs=["file", "file", "file"], outputs=["json", "json"])
iface.launch()