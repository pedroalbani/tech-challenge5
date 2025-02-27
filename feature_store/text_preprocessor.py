import nltk
import re

nltk.download('stopwords')

def pre_proccess(full_text):
  
    # escolhe apenas as palavras, sem potuação e as retorna em minusculo
    words =  re.findall(r'\b[A-zÀ-úü]+\b', full_text.lower())

    # remove stopwords
    stopwords = nltk.corpus.stopwords.words('portuguese')
    stop = set(stopwords)
    no_stopwords = [w for w in words if w not in stop]

    # juntando os tokens novamente em formato de texto
    texto_limpo = " ".join(no_stopwords)

    return texto_limpo