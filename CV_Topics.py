def biblio_CV(lien):
    # Assure-toi d'avoir gensim installé en utilisant : pip install gensim

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