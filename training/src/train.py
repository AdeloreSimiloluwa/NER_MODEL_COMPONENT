def train_spacy(argv=None):
    import json
    import numpy as np
    import plac
    import random
    import warnings
    import argparse
    from pathlib import Path
    import spacy
    import gcsfs
    import logging
    from spacy.util import minibatch, compounding
    from spacy.gold import GoldParse
    from spacy.scorer import Scorer

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir')
    parser.add_argument('--output_dir')
    parser.add_argument('--iteration', type=int)
    parser.add_argument('--output-model-path-file', help='')
    known_args, pipeline_args = parser.parse_known_args(argv)

    fs = gcsfs.GCSFileSystem(project='mlops-kubeflow-00')
    with fs.open(known_args.input_dir, 'r') as f:
        TRAIN_DATA = json.load(f)
        print(TRAIN_DATA)
    # with open('training_data.txt', 'r') as f:
    #     TRAIN_DATA = json.load(f)

    nlp = spacy.blank('en') 
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    for _,annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
          ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes): 
        optimizer = nlp.begin_training()
        for itn in range(known_args.iteration):
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
    
    
    trainer = train_spacy(known_args.input_dir, known_args.output_dir, known_args.iteration)
    trainer.to_disk(known_args.output_dir)
    # Save our trained Model
    Path(known_args.output_model_path_file).write_text(known_args.output_dir)
    Path(known_args.output_dir).parent.mkdir(parents=True, exist_ok=True)
    return nlp

if __name__ == '__main__':
    train_spacy()