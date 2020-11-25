#!/usr/bin/env python
# coding: utf-8

# In[4]:


import kfp
from kfp.components import create_component_from_func

def convert_doccano_fomart_to_spacy(filepath):
    import sys, subprocess;
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'spacy==2.0.18'])
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'spacy download en'])
    import json
    import numpy as np
    import plac
    import random
    import warnings
    from pathlib import Path
    import spacy

    fs = gcsfs.GCSFileSystem(project='mlops-kubeflow-00')
    with fs.open(filepath, 'rb') as f:
         data = f.readlines()

    training_data = []
    for record in data:
        entities = []
        read_record = json.loads(record)
        text = read_record['text']
        entities_record = read_record['labels']

        for start, end, label in entities_record:
            entities.append((start, end, label))

        training_data.append((text, {"entities": entities}))

    return training_data

if __name__ == '__main__':
    ocr_conversion = create_component_from_func(
        convert_doccano_fomart_to_spacy,
        output_component_file='component.yaml',
        base_image='python:3.7')

