def convert_doccano_fomart_to_spacy(argv=None):
    import os
    import json
    import numpy as np
    import plac
    import gcsfs
    import random
    import warnings
    from pathlib import Path
    import spacy
    import argparse
    from tensorflow.python.lib.io import file_io

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path')
    parser.add_argument('--output_dir')

    parser.add_argument('--output-model-path-file', help='')
    known_args, pipeline_args = parser.parse_known_args(argv)
    #read from gcs bucket

    fs = gcsfs.GCSFileSystem(project='mlops-kubeflow-00')
    with fs.open(known_args.input_path, 'rb') as f:
        data = f.readlines()
        print(data)
        
        
    training_data = []
    for record in data:
        entities = []
        read_record = json.loads(record)
        text = read_record['text']
        entities_record = read_record['labels']

        for start, end, label in entities_record:
            entities.append((start, end, label))

        training_data.append((text, {"entities": entities}))
        #print(training_data)
        #with file_io.FileIO(os.path.join(known_args.output_dir, "training_data.txt"), mode = 'w') as f:
    with fs.open(os.path.join(known_args.output_dir), 'w') as f:
        json.dump(training_data, f)
        #return training_data

    Path(known_args.output_model_path_file).parent.mkdir(parents=True, exist_ok=True)
    Path(known_args.output_model_path_file).write_text(known_args.output_dir)
    # return training_data

if __name__ == '__main__':
   convert_doccano_fomart_to_spacy()
