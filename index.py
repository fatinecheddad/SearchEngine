#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:30:37 2022

@author: mac
"""

from ast import arg
import re
import numpy as np
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer 
from nltk.stem import PorterStemmer
from os import terminal_size
from collections import Counter
from sys import argv , exit
porter=PorterStemmer()
lemmatizer=()


        
def stemmatizer_document(tab):  #prend en parametre un tableau de tableaux de tokens
    result=[]
    for i in tab:
            i=[porter.stem(mot) for mot in i]
            result.append(i)
    return result

def lemmatizer_document(tab):  #prend en parametre un tableau de tableaux de tokens
    result=[]
    for i in tab:
            i=[lemmatizer.lemmatize(mot) for mot in i]
            result.append(i)
    return result


"""
def stop_words(tab):
    result=[]
    for i in tab:
        i = [word for word in i if word not in stopwords.words('english')]
        result.append(i)
    return result
        
"""

#Fonction qui prend en entrée le nom d'un document et retourne la liste de mots dont il est composé
def split(nom_doc,separateur):
    doc=open(nom_doc,"r") ; #on ouvre le document
    data=doc.read(); #on separe le fichier global en lignes
    tab=data.split(separateur)
    return tab

#Apllique la tokenisation à tout le document
def tokenizer_documents(tab):
  resultat=[]
  for i in tab:
      i=i[1:]
      resultat.append(word_tokenize(i))
  return resultat

#Calcule la fréquence d'apparition de mots dans un document d'entraînement
#Calcule le TF.IDF

def calculateFrequenciesDocs(documents,IdfWeight=1):
      wordFrequencies = {}
      nbrDocs = 0
    
      #TF - Compter le nombre d'apparitions d'un mot
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
          wordFrequencies[word][doc] *= (np.log(nbrDocs/occurence))**IdfWeight
      
      #retourne nombre de documents, taille du vocabulaire, le dictionnaire associé, le vocabulaire associé
      return nbrDocs, len(wordFrequencies), wordFrequencies, wordFrequencies.keys()
 

#Calcule le TF.IDF associé aux requêtes. Celui-ci se base sur  le vocabulaire généré à l'entraînement
def calculateFrequenciesQueries(documents, voc): 
        wordFrequencies={}
        nbrDocs=0
        #Création d'un dictionnaire associé au vocabulaire
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
            
      
#Enregistrer l'index
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

def chain(data, *funcs):
    for func in funcs:
        data = func(data)
    return data


if __name__ == "__main__":

  if len(argv) != 2:
    print(f"Usage: {argv[0]} <document name>")
    exit()
  else:
    try:
      docname = argv[1]
    except:
      print("Document could not be opened")
      exit()


  nbrd, nbrw, DocIndex,vocDoc=calculateFrequenciesDocs(tokenizer_documents((split(docname,".I "))))
  saveIndex("doc_test.txt",DocIndex)
