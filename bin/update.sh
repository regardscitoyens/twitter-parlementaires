#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

git stash && git pull && git stash pop > /tmp/load_twitter_parls.tmp

bin/build.sh >> /tmp/load_twitter_parls.tmp 2>&1

if git status | grep "data" > /dev/null; then
  cat /tmp/load_twitter_parls.tmp
  git commit data -m "autoupdate"
  git push
fi

