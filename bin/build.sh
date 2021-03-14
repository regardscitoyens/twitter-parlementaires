#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

echo "Downloading..."
echo "--------------"
source /usr/local/bin/virtualenvwrapper.sh
workon twitter-parls
#./download_twitter.py "AssembleeNat" "les-députés"
./download_twitter.py "lcp" "d-put-s-xve-l-gislature"
#./download_twitter.py "Senat" "senateurs"
./download_twitter.py "Senat" "comloiss-nat"
./download_twitter.py "Senat" "comfins-nat"
./download_twitter.py "Senat" "comdevdurs-nat"
./download_twitter.py "Senat" "comd-fenses-nat"
./download_twitter.py "Senat" "comcults-nat"
./download_twitter.py "Senat" "comafsocs-nat"
./download_twitter.py "Senat" "comafecos-nat"
./download_twitter.py "Senat" "collterrs-nat-18321"
curl -sL "http://www.nosdeputes.fr/deputes/json" > .cache/deputes.json
curl -sL "http://www.nossenateurs.fr/senateurs/json" > .cache/senateurs.json

echo
echo "Associating..."
echo "--------------"
#./associate_twitter.py deputes .cache/twitter-AssembleeNat.json
./associate_twitter.py deputes .cache/twitter-lcp.json
./associate_twitter.py senateurs .cache/twitter-Senat.json
echo

