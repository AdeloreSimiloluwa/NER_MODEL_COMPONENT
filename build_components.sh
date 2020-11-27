#!/bin/sh

echo "\nBuild and push preprocess component"
./preprocess/build_image.sh

echo "\nBuild and push training component"
./training/build_image.sh

echo "\nBuild and push training component"
./prediction/build_image.sh
