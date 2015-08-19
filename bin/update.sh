#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

git pull > /tmp/load_twitter_parls.tmp

bin/build.sh >> /tmp/load_twitter_parls.tmp

if git status | grep "data" > /dev/null; then
  cat /tmp/load_twitter_parls.tmp
  git commit data -m "autoupdate"
  git push
fi

