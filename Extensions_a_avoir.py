#Tout les Pip qu'il faut installer
pip install gensim
pip install httpie
pip install requests

# les import qu'il faut faire pour le code
import PyPDF2
import json
import http.client
import re
from gensim import corpora
from gensim.models import LdaModel
from pprint import pprint