from __future__ import unicode_literals, print_function

TRAIN_DATA = training_data
OUTPUT_PATH = '/content/custom_ner_model'

################### Train Spacy NER.###########
def train_spacy(TRAIN_DATA, OUTPUT_PATH, iterations):

    #Converting JSON1 file to Spacy tuples format
    import sys, subprocess;
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'spacy==2.0.18'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'spacy download en'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'kfp'])
    import json
    import numpy as np
    import plac
    import random
    import warnings
    from pathlib import Path
    import spacy
    import logging
    from spacy.util import minibatch, compounding
    from spacy.gold import GoldParse
    from spacy.scorer import Scorer
    from kfp.components import create_component_from_func

    TRAIN_DATA = TRAIN_DATA
    nlp = spacy.blank('en') 
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes): 
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                try:
                    nlp.update(
                        [text],  
                        [annotations],  
                        drop=0.2,  
                        sgd=optimizer,  
                        losses=losses)
                except Exception as error:
                    print(error)
                    continue
            print(losses)
    return nlp


trainer = train_spacy(TRAIN_DATA, OUTPUT_PATH, 20)

    # Save our trained Model
#Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
trainer.to_disk(OUTPUT_PATH)

if __name__ == '__main__':
    ocr_conversion = create_component_from_func(
        train_spacy,
        output_component_file='components.yaml',
        base_image='python:3.7')
