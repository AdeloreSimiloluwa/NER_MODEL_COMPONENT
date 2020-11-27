FROM python:3.7
RUN pip install --upgrade pip
RUN python3 -m pip install spacy==2.0.18
RUN python3 -m pip install spacy download en
RUN python3 -m pip install gcsfs==0.5.3
RUN python3 -m pip install fsspec==0.6.2
RUN python3 -m pip install google-cloud-storage
RUN python3 -m pip install pyyaml
RUN python3 -m pip install tensorflow
COPY ./src /pipelines/component/src
