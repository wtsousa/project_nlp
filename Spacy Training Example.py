# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:38:49 2021

@author: Will
"""
import pandas as pd
import spacy
import random
import pickle
from spacy.matcher import PhraseMatcher

# Create a blank 'en' model
nlp = spacy.blank('pt')

# Create a new entity recognizer and add it to the pipeline
ner = nlp.create_pipe('ner')
nlp.add_pipe(ner)

# Add the label 'GADGET' to the entity recognizer
ner.add_label('PRD')
ner.add_label('QTD')
ner.add_label('MED')
ner.add_label('CMP')


# TRAINING_DATA = [('1 lata de leite condensado', {'entities': [(0, 1, 'QTD'),(2, 6, 'MED'),(10, 26, 'ING')]}),
#  ('1 lata de leite (medida da lata de leite condensado)', {'entities': [(0, 1, 'QTD'),(2, 6, 'MED'),(10, 15, 'ING'),(17, 51, 'MED')]}),
#  ('3 ovos inteiros', {'entities': [(28, 36, 'GADGET')]}),
#  ('1 xícara (chá) de açúcar', {'entities': [(4, 12, 'GADGET')]}),
#  ('1/2 xícara de água', {'entities': [(5, 11, 'GADGET')]}),
#  ('Pudim:', {'entities': []}),
#  ('Calda:', {'entities': []})]

with open('C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP\\training.data', 'rb') as filehandle:
    TRAINING_DATA = pickle.load(filehandle)
with open('C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP\\test.data', 'rb') as filehandle:
    TEST_DATA = pickle.load(filehandle)

# Start the training
nlp.begin_training()

# Loop for 10 iterations
for itn in range(10):
    # Shuffle the training data
    random.shuffle(TRAINING_DATA)
    losses = {}
    
    # Batch the examples and iterate over them
    for batch in spacy.util.minibatch(TRAINING_DATA, size=2):
        texts = [text for text, entities in batch]
        annotations = [entities for text, entities in batch]
        
        # Update the model
        nlp.update(texts, annotations, losses=losses)
        print(losses)
        
        
# TEST_DATA = ['Apple is slowing down the iPhone 8 and iPhone X - how to stop it',
#  "I finally understand what the iPhone X 'notch' is for",
#  'Everything you need to know about the Samsung Galaxy S9',
#  'Looking to compare iPad models? Here’s how the 2018 lineup stacks up',
#  'The iPhone 8 and iPhone 8 Plus are smartphones designed, developed, and marketed by Apple',
#  'what is the cheapest ipad, especially ipad pro???',
#  'Samsung Galaxy is a series of mobile computing devices designed, manufactured and marketed by Samsung Electronics']convert_train_to_test(TRAINING_DATA)

TEST_DATA = [line[0] for line in TRAINING_DATA]

# Process each text in TEST_DATA
entities_list = []

for doc in nlp.pipe(TEST_DATA):
    # Print the document text and entitites
    print(doc.text)
    tuple_dict = dict.fromkeys(['QTD', 'MED', 'PRD', 'CMP', 'TXT'])
    for ent in doc.ents:
        tuple_dict[ent.label_] = ent.text
    tuple_dict['TXT'] = doc.text
    entities_list.append(tuple_dict)
    print(tuple_dict)
    print('\n')
    
DF_ING = pd.DataFrame(entities_list)
DF_ING.PRD.unique()

DF_DIR = 'C:\\Users\\Will\\Documents\\Data Science\\Projeto NLP'
DF_CSV = DF_DIR + '\\Receitas_Produtos.csv'
DF_ING.to_csv(DF_CSV)