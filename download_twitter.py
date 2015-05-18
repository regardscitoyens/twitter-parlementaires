#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json
from twitter import Twitter, OAuth
from twitterconfig import KEY, SECRET, OAUTH_TOKEN, OAUTH_SECRET

if len(sys.argv) < 3:
    sys.stderr.write("Please input both Twitter list's owner_screen_name and slug\n")
    exit(1)

LIST_USER, LIST_SLUG = sys.argv[1:3]

if not os.path.isdir(".cache"):
    os.makedirs(".cache")

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, KEY, SECRET))
accounts = {}
page = 1
cursor = -1
while cursor:
    res = t.lists.members(owner_screen_name=LIST_USER, slug=LIST_SLUG, cursor=cursor, include_entities='false', skip_status='true', count=5000)
    with open(os.path.join('.cache', 'twitter-%s-%s.json' % (LIST_USER, cursor if cursor != -1 else 0)), 'w') as f:
        json.dump(res, f)
    cursor = res.get('next_cursor', res.get('next_cursor_str', 0))
    new = 0
    for account in res['users']:
        name = account['screen_name'].lower()
        if name not in accounts:
            accounts[name] = account
            new += 1
    print("[INFO/%s] page %s -> %s results including %s new ; new total: %s" % (LIST_SLUG, page, len(res['users']), new, len(accounts)))
    page += 1

with open(os.path.join('.cache', 'twitter-%s.json' % LIST_USER), 'w') as f:
    json.dump(accounts, f)
