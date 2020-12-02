import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import argparse
import os
import json
import numpy as np
import plac
import random
import warnings
from pathlib import Path
import spacy
import gcsfs

argv=None
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir')
parser.add_argument('--output_dir')
parser.add_argument('--model_dir')
parser.add_argument('--output-model-path-file', help='')
known_args, pipeline_args = parser.parse_known_args(argv)

def convert_doccano_fomart_to_spacy(argv=None):
   # read test data from GCS bucket
    fs = gcsfs.GCSFileSystem(project='mlops-kubeflow-00')
    with fs.open(known_args.input_dir, 'rb') as f:
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

    return training_data


# load model from disk or GCS. We can't load files from GCS 
nlp = spacy.load(known_args.model_dir)

test = known_args.input_dir#'test_data.json1'
test = convert_doccano_fomart_to_spacy(test)


def test_spacy(argv=None):
    #test the model and evaluate it
    examples = test
    tp=0
    tr=0
    tf=0

    ta=0
    c=0        

    for text,annot in examples:
      fs = gcsfs.GCSFileSystem(project='mlops-kubeflow-00')
      f=fs.open(os.path.join(known_args.output_dir+"result"+str(c)+".txt"), 'w')
      doc_to_test=nlp(text)
      d={}
      for ent in doc_to_test.ents:
          d[ent.label_]=[]
      for ent in doc_to_test.ents:
          d[ent.label_].append(ent.text)

      for i in set(d.keys()):

          f.write("\n\n")
          f.write(i +":"+"\n")
          for j in set(d[i]):
              f.write(j.replace('\n','')+"\n")
      d={}
      for ent in doc_to_test.ents:
          d[ent.label_]=[0,0,0,0,0,0]
      for ent in doc_to_test.ents:
          doc_gold_text= nlp.make_doc(text)
          gold = GoldParse(doc_gold_text, entities=annot.get("entities"))
          y_true = [ent.label_ if ent.label_ in x else 'Not '+ent.label_ for x in gold.ner]
          y_pred = [x.ent_type_ if x.ent_type_ ==ent.label_ else 'Not '+ent.label_ for x in doc_to_test]  
          if(d[ent.label_][0]==0):
              (p,r,f,s)= precision_recall_fscore_support(y_true,y_pred,average='weighted')
              a=accuracy_score(y_true,y_pred)
              d[ent.label_][0]=1
              d[ent.label_][1]+=p
              d[ent.label_][2]+=r
              d[ent.label_][3]+=f
              d[ent.label_][4]+=a
              d[ent.label_][5]+=1
      c+=1
    for i in d:
      print("\n For Entity "+i+"\n")
      print("Accuracy : "+str((d[i][4]/d[i][5])*100)+"%")
      print("Precision : "+str(d[i][1]/d[i][5]))
      print("Recall : "+str(d[i][2]/d[i][5]))
      print("F-score : "+str(d[i][3]/d[i][5]))

Path(known_args.output_model_path_file).parent.mkdir(parents=True, exist_ok=True)
Path(known_args.output_model_path_file).write_text(known_args.output_dir)

if __name__ == '__main__':
   test_spacy()
