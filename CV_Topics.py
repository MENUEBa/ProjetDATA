# Mettre en place les variables
documents = texte_seul

# Tokenisation des documents en mots
tokenized_documents = [doc.split() for doc in documents]

# Création d'un dictionnaire à partir du corpus
dictionary = corpora.Dictionary(tokenized_documents)

# Création de la représentation du corpus en tant que sac de mots (BoW)
corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]

# Création d'un modèle LDA
lda_model = LdaModel(corpus, num_topics=3, id2word=dictionary)

# Affichage des topics générés par le modèle
pprint(lda_model.print_topics())