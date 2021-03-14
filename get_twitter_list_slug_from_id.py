#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pprint import pprint
from twitter import Twitter, OAuth
from twitterconfig import KEY, SECRET, OAUTH_TOKEN, OAUTH_SECRET

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, KEY, SECRET))

LIST_ID = sys.argv[1]
res = t.lists.show(list_id=LIST_ID)
res.pop("user")
pprint(res)
