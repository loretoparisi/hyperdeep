# util function : parsing and dictionnary
# @author melanie ducoffe
from contextlib import closing
import copy
import os
import pickle

import numpy as np

# parse a document using dot
# read line by line
def generate_incorrect_sentence(dico, correct_sentence, index):
	incorrect_sentence = copy.copy(correct_sentence)
	nb_words = [len(dico[i].keys()) for i in range(len(dico))]
	new_indices = []
	i=0
	while (i <len(correct_sentence)):
		value = np.random.randint(nb_words[i])
		if value != correct_sentence[i,index]:
			new_indices.append(index)
			incorrect_sentence[i][index]=value
			i+=1
	return incorrect_sentence
		
def sub_line(line, j, dwin):
	line_sub = np.zeros((line.shape[0], dwin))
	for i in range(line.shape[0]):
		line_sub[i]=line[i, j:j+dwin]
	return line_sub

#add_padding
def add_padding(line, paddings):
	return np.concatenate([paddings, line, paddings], axis=1)

def get_input_from_file(repo, filename, dico, padding=[]):
	sentences=[]
	word_sentences=[]
	with closing(open(os.path.join(repo, filename), 'rb')) as f:
		line = []
		rare = [dico[0]['RARE'], dico[1]['RARE'],
			dico[2]['RARE'], dico[3]['RARE']]
		for words in f:
			tags = words.split('\t')[2:]
			tags = [tag.lower() for tag in tags]
			if len(tags)==0:
				continue
			line.append(tags)
			if tags[0]=='.':
				lemme = np.zeros((4, len(line))).astype(int)
				for i in range(len(line)):
					if len(line[i])<4:
						continue
					lemme[0][i] = dico[0].get(line[i][0], rare[0])
					lemme[1][i] = dico[1].get(line[i][1], rare[1])
					lemme[2][i] = dico[2].get(line[i][2], rare[2])
					lemme[3][i] = dico[3].get(line[i][3], rare[3])
				sentences.append(lemme)
				word_sentences.append(line)
				line = []

	return sentences, word_sentences

def get_input_from_files(repo, filenames, dico):
	sentences = []
	for filename in filenames :
		sentences += get_input_from_file(repo, filename, dico)

	return sentences

"""
TOKENIZE TEXT
"""
def get_input_from_line(filename):
	sentences_tags=[]
	
	with closing(open(filename, 'rb')) as f:
		for line in f:
			if len(line) <= 2:
				continue
			sequence = line.split('\t')[2:]
			sequence[3] = sequence[3][0] # Remove endline characters
			# LOWER TEXT
			# @TODO: TEST WITHOUT LOWER  
			sequence = [elem.lower() for elem in sequence]
			sentences_tags.append(sequence)
			
	return sentences_tags

"""
CREATE OCC_DICO FROM TEXT
"""
def build_dico_from_file(filename, dico):
	sentences_tags = get_input_from_line(filename) # open in universal format !!!!
	for line in sentences_tags:
		for i in range(len(dico.keys())):
			if len(line) < len(dico.keys()):
				continue
			if len(line[i]) == 0:
				continue
			if line[i] not in dico[i].keys():
				dico[i][line[i]]= 1
			else:
				dico[i][line[i]]+=1
	return dico

"""
CREATE OCC_DICO FROM CORPUS
"""
def build_dictionnary(corpus):
	dico ={}
	dico[0]={}; dico[1]={}; dico[2]={}; dico[3]={}

	# CREATE OCC_DICO
	print "Corpus:"
	for filename in corpus:
		print "\t", filename
		dico = build_dico_from_file(filename, dico)

	# PICKLE OCC_DICO
	with closing(open(OCC_DICO, 'wb')) as f:
		pickle.dump(dico, f, protocol=pickle.HIGHEST_PROTOCOL)
		
	return dico


def build_dico_from_occ(occ_dico):
	# INIT PARAMETERS
	# seuil pour la conservation des tokens
	# len_data = [nb_forme, nb_lemme, nb_code, nb_fonction]
	len_data = [5, 5, 1, 1]
	
	index = [0, 0, 0, 0]
	dico = {}; dico[0]={}; dico[1]={}; dico[2]={}; dico[3]={}
	
	# RARE PARSING
	for i in range(4):
		dico[i]['RARE'] = index[i]	
		dico[i]['PARSING'] = index[i] + 1
		index[i] = 2
	# index == [2, 2, 2, 2]

	for i in range(4):
		for elem in occ_dico[i]:
			if occ_dico[i][elem] >= len_data[i] and elem not in dico[i]:
				dico[i][elem] = index[i]
				index[i] += 1

	with closing(open(EMBEDDING_DICO, 'wb')) as f:
		pickle.dump(dico, f, protocol = pickle.HIGHEST_PROTOCOL)
			
	return dico

if __name__=="__main__":
	
	corpus = []
	for filename in os.listdir(CORPUS_PATH):
		if ".txt" in filename:
			corpus.append(CORPUS_PATH + filename)
	
	print "#######################"
	print "Creation de l'embedding"
	print "#######################"
	
	occ_dico = build_dictionnary(corpus)
	embedding_dico = build_dico_from_occ(occ_dico)

	print "Taille du corpus (vocabulaire):"
	print "\t", len(occ_dico[0]), "formes"
	print "\t", len(occ_dico[1]), "lemmes"
	print "\t", len(occ_dico[2]), "codes"
	print "\t", len(occ_dico[3]), "fonctions"
	
	print "Taille de l'embedding (les tokens non present sont consideres comme RARE):"
	print "\t", len(embedding_dico[0]) - 2, "formes"
	print "\t", len(embedding_dico[1]) - 2, "lemmes"
	print "\t", len(embedding_dico[2]) - 2, "codes"
	print "\t", len(embedding_dico[3]) - 2, "fonctions"