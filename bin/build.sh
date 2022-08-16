#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

echo "Downloading..."
echo "--------------"
#source /usr/local/bin/virtualenvwrapper.sh
#workon twitter-parls

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"    # if `pyenv` is not already on PATH
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
pyenv activate twitter-parls

#./download_twitter.py "AssembleeNat" "les-députés"
#./download_twitter.py "lcp" "d-put-s-xve-l-gislature"
./download_twitter.py "ivalerio" "1536014130506866689"
#./download_twitter.py "Senat" "senateurs"
./download_twitter.py "Senat" "comloiss-nat"
./download_twitter.py "Senat" "comfins-nat"
./download_twitter.py "Senat" "comdevdurs-nat"
./download_twitter.py "Senat" "comd-fenses-nat"
./download_twitter.py "Senat" "comcults-nat"
./download_twitter.py "Senat" "comafsocs-nat"
./download_twitter.py "Senat" "comafecos-nat"
./download_twitter.py "Senat" "collterrs-nat-18321"
#curl -sL "http://www.nosdeputes.fr/deputes/json" > .cache/deputes.json
curl -sL "https://2022.nosdeputes.fr/deputes/json?$$$RANDOM" > .cache/deputes.json
curl -sL "http://www.nossenateurs.fr/senateurs/json?$$$RANDOM" > .cache/senateurs.json

echo
echo "Associating..."
echo "--------------"
#./associate_twitter.py deputes .cache/twitter-AssembleeNat.json
#./associate_twitter.py deputes .cache/twitter-d-put-s-xve-l-gislature.json
#./associate_twitter.py 2022-deputes-elus+ND.csv .cache/twitter-1536014130506866689.json
./associate_twitter.py deputes .cache/twitter-1536014130506866689.json
./search_missing_twitter.py deputes data/deputes.csv

./associate_twitter.py senateurs .cache/twitter-comloiss-nat.json .cache/twitter-comfins-nat.json .cache/twitter-comdevdurs-nat.json .cache/twitter-comd-fenses-nat.json .cache/twitter-comcults-nat.json .cache/twitter-comafsocs-nat.json .cache/twitter-comafecos-nat.json .cache/twitter-collterrs-nat-18321.json
echo

