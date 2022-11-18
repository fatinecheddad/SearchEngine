import spacy
from typing import Dict

nlp = spacy.load("en_core_web_md")



print(nlp.vocab["door"].similarity(nlp.vocab["apple"]))


def chain(data, *funcs):
    for func in funcs:
        data = func(data)
    return data


def theodoro_boost(query , word_frequencies : Dict[str : Dict[str: float]] ):
    for query_word in query:
        for doc_word ,doc_freq in word_frequencies.items():
            if doc_word != query_word:
                doc_freq = doc_freq/(1.01 - nlp[query_word].similarty(nlp.vocab[doc_word]))
            

