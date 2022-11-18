#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:30:37 2022

@author: mac
"""

import re
import nltk
nltk.download("punkt")
import numpy as np
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer 
from nltk.stem import PorterStemmer
from os import terminal_size
from collections import Counter
from nltk.corpus import stopwords
porter=PorterStemmer()
lemmatizer = WordNetLemmatizer()


#Stem les mots dans un tableau
def stemmatizer_document(tab):  #prend en parametre un tableau de tableaux de tokens
    result=[]
    for i in tab:
            i=[porter.stem(mot) for mot in i]
            result.append(i)
    return result

#Lemmatize les mots dans un tableau
def lemme(docs_tok):
    lemmatizer = WordNetLemmatizer()
    docs_lem=[]
    for doc in docs_tok:
        doc = [lemmatizer.lemmatize(mot) for mot in doc]
        docs_stem.append(doc)
    return docs_stem

def lemmatizer_document(tab):  #prend en parametre un tableau de tableaux de tokens
    result=[]
    for i in tab:
            i=[lemmatizer.lemmatize(mot) for mot in i]
            result.append(i)
    return result



def stop_words(tab):
    result=[]
    for i in tab:
        i = [word for word in i if word not in stopwords.words('english')]
        result.append(i)
    return result

        


#Sépare les documents entre eux et les retranscrit dans une liste de mots
def split(nom_doc,separateur):
    doc = open(nom_doc,"r") ;
    data = doc.read(); #on separe le text global en lignes
    tab = data.split(separateur)
    return tab

#tokenize les mots contenus dans une liste de mots
def tokenizer_documents(tab):
    resultat=[]
    for i in tab:
        i=i[1:]
        resultat.append(word_tokenize(i))
    return resultat

#Calcule les fréquences de mots dans les documents
def calculateFrequenciesDocs(documents,IdfWeight=1):
      wordFrequencies = {}
      nbrDocs = 0
    
      #TF
      for document in documents:
        nbrDocs += 1
        nbrOfWords = len(document)
        wordCounts = Counter(document)
          
        for word in wordCounts.elements():
            if word in wordFrequencies.keys():
              wordFrequencies[word]["D"+str(nbrDocs)] = wordCounts[word]/nbrOfWords
            else :
              wordFrequencies[word]= {"D"+str(nbrDocs):wordCounts[word]/nbrOfWords}
        
      #IDF 
      for word in wordFrequencies.keys():
        #print(word)
        occurence = len(wordFrequencies[word])
        for doc in wordFrequencies[word].keys():
          wordFrequencies[word][doc] *= (np.log(nbrDocs/occurence+1))**IdfWeight
      
      return nbrDocs, len(wordFrequencies), wordFrequencies, wordFrequencies.keys()

#Calcule les fréquences d'une requête
def liste_voc(dico_voc):
  liste=[]
  for elt in dico_voc:
    liste.append(elt)
  return liste

def vecteurs_queries(queries,vocDoc):
  voc = liste_voc(vocDoc)
  result = [[0 for i in range(len(voc))] for i in range(len(queries)-1)]
  for i in range(1,len(queries)):
    requete=queries[i]
    for mot in requete:
      if mot in voc:
        indice = voc.index(mot)
        result[i-1][indice]=1
  return result
        

  
def calculateFrequenciesQueries(documents, voc): 
        wordFrequencies={}
        nbrDocs=0
        for key in voc:
                wordFrequencies[key]={}
        #TF
        for document in documents:
            nbrDocs += 1
            nbrOfWords = len(document)
            wordCounts = Counter(document)
              
            for word in wordCounts.elements():
                if word in wordFrequencies.keys():
                  wordFrequencies[word]["D"+str(nbrDocs)] = wordCounts[word]/nbrOfWords
                else :
                  pass
          
        return nbrDocs, len(wordFrequencies), wordFrequencies, wordFrequencies.keys()
            
      
#Sauvegarde dans un fichier le TF IDF de chaque mot présents dans les documents 
def saveIndex(path, DocIndex):

  with open(path, "w") as savefile:
    lines = []
    for word in DocIndex.keys():
      line = word + " "
      for doc in DocIndex[word].keys():
        line += doc + ":" + str(DocIndex[word][doc]) + " "
      lines.append(line + "\n")
    savefile.writelines(lines)
    savefile.close()


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
  return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))



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
      saveFile.write(f"{query_index+1} {ratings[rating_index][0]} {ratings[rating_index][1]}\n")
      rating_index += 1

  saveFile.close()
            
#print(lecture_fichier("fichier_test.txt",3,30))
 
#print(tokenizer_documents((split("CISI.ALLnettoye",".I "))   ))

voc_docs = stop_words(lemmatizer_document(tokenizer_documents((split("CISI.ALLnettoye",".I "))   )))
nbrd, nbrw, DocIndex,vocDoc=calculateFrequenciesDocs(voc_docs)
#print(DocIndex,nbrd,nbrw)
saveIndex("doc_test.txt",DocIndex)
DocTab=(lecture_fichier("doc_test.txt",nbrw,nbrd))


voc_queries = stop_words(lemmatizer_document(tokenizer_documents((split("CISI_dev.QRY",".I ")))))
queriesVect = vecteurs_queries(voc_queries,vocDoc)



nbrd2, nbrw2, QryIndex,voc=calculateFrequenciesQueries(voc_queries,vocDoc)
#print(QryIndex,nbrd2,nbrw2)
saveIndex("qry_test.txt",QryIndex)
QryVect = vecteurs_queries(voc_queries, vocDoc)

save_result_file("resultat.txt", QryVect, DocTab, 0.01 )

#print(QryVect)
#print(rating(QryVect[6],DocTab))
#print(voc)





  
        
