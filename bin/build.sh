#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

echo "Downloading..."
echo "--------------"
source /usr/local/bin/virtualenvwrapper.sh
workon twitter-parls
./download_twitter.py "AssembleeNat" "les-députés"
./download_twitter.py "Senat_Info" "senateurs"
curl -sL "http://www.nosdeputes.fr/deputes/json?$$" > .cache/deputes.json
curl -sL "http://www.nossenateurs.fr/senateurs/json?$$" > .cache/senateurs.json

echo
echo "Associating..."
echo "--------------"
./associate_twitter.py deputes data/twitter-AssembleeNat.json
./associate_twitter.py senateurs data/twitter-Senat_Info.json
echo

