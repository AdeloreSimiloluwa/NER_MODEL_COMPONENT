#!/bin/sh

BUCKET="kfsconfig"

echo "\nCopy component specifications to Google Cloud Storage"
gsutil cp preprocess/component.yaml gs://${BUCKET}/componenttt/preprocess/component.yaml
gsutil acl ch -u AllUsers:R gs://${BUCKET}/componenttt/preprocess/component.yaml

echo "\nCopy component specifications to Google Cloud Storage"
gsutil cp training/component.yaml gs://${BUCKET}/componenttsss/training/component.yaml
gsutil acl ch -u AllUsers:R gs://${BUCKET}/componenttsss/training/component.yaml

echo "\nCopy component specifications to Google Cloud Storage"
gsutil cp testing/component.yaml gs://${BUCKET}/componenttt/testing/component.yaml
gsutil acl ch -u AllUsers:R gs://${BUCKET}/componenttt/testing/component.yaml
