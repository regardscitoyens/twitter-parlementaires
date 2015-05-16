#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

echo "Downloading..."
echo "--------------"
source /usr/local/bin/virtualenvwrapper.sh
workon twitter-parls
./get_twitter.py "AssembleeNat" "les-députés"
./get_twitter.py "Senat_Info" "senateurs"
wget -q "http://www.nosdeputes.fr/deputes/json" -O .cache/deputes.json
wget -q "http://www.nossenateurs.fr/senateurs/json" -O .cache/senateurs.json

echo
echo "Associating..."
echo "--------------"
./associate_twitter.py data/twitter-AssembleeNat.json .cache/deputes.json
./associate_twitter.py data/twitter-Senat_Info.json .cache/senateurs.json

