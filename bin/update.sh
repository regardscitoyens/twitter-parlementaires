#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')/..

bin/build.sh > /tmp/load_twitter_parls.tmp

if git status | grep "data.*csv" > /dev/null; then
  cat /tmp/load_twitter_parls.tmp
  git commit data -m "autoupdate"
  git push
fi

