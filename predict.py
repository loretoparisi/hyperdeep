#!/usr/bin/python
# -*-coding:Utf-8 -*
'''
Created on 7 déc. 2016

@author: lvanni
'''
from contextlib import closing
import json
import pickle
import sys

import theano

from core.config import EMBEDDING_DICO, DWIN, VECT_SIZE, N_HIDDEN, NLP_PATH
from core.training.lookup import LookUpTrain
from core.training.main import pre_process
import theano.tensor as T

if __name__ == '__main__':
    
    corpus = {}
    if len(sys.argv) >= 4:
        if sys.argv[1][-1] != "/":
            sys.argv += "/"
        metadata = json.load(open(sys.argv[1] + "corpus.json", "r"))
        
        corpus[sys.argv[3]] = []
        for text_id in metadata[sys.argv[2]][sys.argv[3]]:
            corpus[sys.argv[3]].append(sys.argv[1] + text_id + ".tg")
    else:
        corpus["text"] = [sys.argv[1]] 
    
    print corpus
    
    print "Chargement de l'embedding.................",
    try:
        with closing(open(EMBEDDING_DICO, 'rb')) as f:
            dico = pickle.load(f)
    except:
        print "ERR"
        print "missing training files!"
        sys.exit(0)
    
    print  "OK"
    
    print "Chargement du réseau......................",
    # Nb mot dans le dico/corpus
    n_mot = [len(dico[i]) for i in dico.keys()]
    print  "OK"
    
    # Natural Langage Processing
    t_nlp = LookUpTrain(DWIN, n_mot, VECT_SIZE, N_HIDDEN)
    t_nlp.load(NLP_PATH, "network_state_0")
    
    # Preprocessing => découpage du texte
    x_train, x_valid, x_test, tmp, tmp, tmp = pre_process(corpus)

    # concatener des arrays numpy
    #x_cont = numpy.concatenate([x_train, x_valid, x_test], axis=0)
    
    # Input features
    x = T.itensor3('x') 
    
    # probabilites sur un text
    probabilities = theano.function(inputs=[x], outputs=t_nlp.probabilities_text(x), allow_input_downcast=True)
    # A TESTER
    proba_list = probabilities(x_test)
    print proba_list
    
    # sinon
    # np.mean([probabilities(x_cont[index*batch_size:(index+1)*batch_size])])
    
    # Qualité de la prédiction
    #predict_confidency = theano.function(inputs=[x], outputs=t_nlp.predict_confidency(x)[0], allow_input_downcast=True)
    
    # test predict
    # Fonction de prediction : Pour une phrase donnée, quel est le président
    """
    predict = theano.function(inputs=[x], outputs=t_nlp.predict(x), allow_input_downcast=True)
    for test in x_test:
        print "predict :", corpus[predict([test])].replace(CORPUS_PATH, "").split(".")[0]
    """
    
    
