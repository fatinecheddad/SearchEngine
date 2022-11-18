import numpy as np
import spacy
from typing import Dict
from sys import argv, exit


nlp = spacy.load("en_core_web.md")

def lecture_fichier(nom_fichier,taille_vocab,nb_doc):  #tab est le tableau de tableaux tokenizé
    text=open(nom_fichier,"r+")

    nbligne=0
    resultat=[[0 for i in range(taille_vocab)] for i in range(nb_doc)] #tableau n*m avec n le nombre de document et m la taille du vocabulaire
    for i in text.readlines():
            
  
            regexp=re.compile(r"D(\d)+:([0-9]+\.+?[0-9]+)")

            res=regexp.findall(i)
            if res!=None:

                for k in res:
                    numDoc=int(k[0])
                    freq=float(k[1])
                    resultat[numDoc-1][nbligne]=freq


                
            nbligne=nbligne+1
    return resultat

def cosSim(v1,v2):
  return np.dot(v1,v2)#/(np.linalg.norm(v1)*np.linalg.norm(v2))



def sortingParam(vectorTuple):
  return vectorTuple[1]


def rating(queryVec, vectors):    
  res = []
  for i, document in enumerate(vectors):
    res.append((i+1,cosSim(queryVec,document)))
  res.sort(reverse = True, key=sortingParam)
  return res


def saveResult(savePath, ratings):
  lines = []
  with open(savePath, "w") as saveFile:
    for rating in ratings:
      lines.append(f"D{str(rating[0])} {str(rating[1])}\n")
    saveFile.writelines(lines)
    saveFile.close()


def save_result_file(saveFile,query_vectors, document_vectors, threshold ):


  saveFile = open(saveFile, "w")

  for query_index ,query_vector in enumerate(query_vectors):

    ratings = rating(query_vector , document_vectors)
    rating_index = 0
    while ratings[rating_index][1] > threshold:
      saveFile.write(f"{query_index} {ratings[rating_index][0]} {ratings[rating_index][1]}")
      rating_index += 1

  saveFile.close()


def chain(data, *funcs):
    for func in funcs:
        data = func(data)
    return data


def theodoro_boost(query , word_frequencies : Dict[str : Dict[str: float]] ):
    for query_word in query:
        for doc_word ,doc_freq in word_frequencies.items():
            if doc_word != query_word:
                doc_freq = doc_freq/(1.01 - nlp[query_word].similarty(nlp.vocab[doc_word]))
            

if __name__ == "__main__":
    pass