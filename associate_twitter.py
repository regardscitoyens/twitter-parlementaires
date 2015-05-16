#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json

if len(sys.argv) < 3:
    sys.stderr.write("Please input both files for the Twitter list data and the NosDéputés/NosSénateurs data\n")
    exit(1)

with open(sys.argv[1]) as f:
    twitter = json.load(f)
with open(sys.argv[2]) as f:
    parls = json.load(f)


