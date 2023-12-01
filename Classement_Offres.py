# Liste pour stocker les résultats
resultats_classification = []

# Parcourir chaque offre dans la liste Offres
for offre_id, offre_description in Offres:
    # Tokenisation du document
    tokenized_doc = offre_description.split()

    # Convertir le document en une représentation BoW à l'aide du dictionnaire existant
    doc_bow = dictionary.doc2bow(tokenized_doc)

    # Obtention de la distribution des topics pour le document
    topic_distribution = lda_model.get_document_topics(doc_bow)

    # Calcul de la moyenne des scores pour chaque topic
    moyenne_scores = sum(score for topic, score in topic_distribution) / len(topic_distribution)

    # Ajout du tuple (ID de l'offre, moyenne des scores) à la liste des résultats
    resultats_classification.append((offre_id, moyenne_scores))

# Trier les offres par score de la meilleure à la moins bonne
top_offres = sorted(resultats_classification, key=lambda x: x[1], reverse=True)[:10]

# Afficher les trois meilleures offres
for i, (offre_id, score) in enumerate(top_offres, start=1):
    print(f"Classement {i} - ID de l'offre : {offre_id}, Score : {score}")