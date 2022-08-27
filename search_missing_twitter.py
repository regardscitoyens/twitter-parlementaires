#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, csv, json
from twitter import Twitter, OAuth
from twitterconfig import KEY, SECRET, OAUTH_TOKEN, OAUTH_SECRET

BLACKLIST = [
    "ATColloque",
    "GNadeauDubois"
]

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, KEY, SECRET))

args = {
    "include_entities": "false",
    "count": 20
}


if len(sys.argv) < 3:
    sys.stderr.write("Please input deputes/senateurs and the path for the Twitter list data\n")
    exit(1)

TYPEPARLS, TWEETS_FILE = sys.argv[1:3]
typeparl = TYPEPARLS.rstrip("s")
searchwords = {
    "depute": [
        u"depute",
        u"deputé",
        u"députe",
        u"député",
        u"deputee",
        u"deputée",
        u"députee",
        u"députée",
        u"assemblee nationale",
        u"assemblée nationale",
        u"@assembleenat"
    ],
    "senateur": [
        u"senateur",
        u"sénateur",
        u"senatrice",
        u"sénatrice",
        u"senat",
        u"sénat",
        u"@senat"
    ]
}[typeparl]

with open(os.path.join(".cache", "%s.json" % TYPEPARLS)) as f:
    try:
        parls = dict((parl["slug"], parl) for parl in [p[typeparl] for p in json.load(f)[TYPEPARLS]])
    except ValueError:
        sys.stderr.write("Could not open Nos%s.fr parlementaires list" % TYPEPARLS)
        exit(1)

known_accounts = set(b.lower() for b in BLACKLIST)
with open(TWEETS_FILE) as f:
    for parl in csv.DictReader(f):
        del(parls[parl["slug"]])
        known_accounts.add(parl["twitter"].lower())

for rab in ["2012-2017", "2017-2022", "2022-2027"]:
    try:
        with open(TWEETS_FILE.replace(".csv", "_%s.csv" % rab)) as f:
            for parl in csv.DictReader(f):
                known_accounts.add(parl["twitter"].lower())
    except IOError:
        pass

missing = sorted(parls.values(), key=lambda x: x["nom_de_famille"])
print "There are still %s %s for which we haven't found a Twitter account." % (len(missing), TYPEPARLS)
print

for parl in missing:

    search = t.users.search(q=parl["nom"], **args)
    search2 = t.users.search(q="%s %s" % (typeparl, parl["nom_de_famille"]), **args)
    search3 = t.users.search(q="%s %s" % (parl["nom_de_famille"], parl["nom_circo"]), **args)

    goodmatches = {}

    for res in search + search2 + search3:
        if res["screen_name"].lower() in known_accounts:
            continue
        desc = res["description"].lower()
        if any(word in desc for word in searchwords):
            goodmatches[res["screen_name"]] = res
            goodmatches[res["screen_name"]]["count"] = goodmatches[res["screen_name"]].get("count", 0) + 1
    matches = sorted(goodmatches.values(), key=lambda x: x["count"], reverse=True)
    if len(matches):
        print " - %s proposals found for %s (%s):" % (len(matches), parl["nom"], parl["url_nos%s" % TYPEPARLS])
        for g in matches:
            print u"   ⋅ @%s:" % g["screen_name"], (g["description"], g.get("url", "") or ""), "‑", "https://twitter.com/%s" % g["screen_name"]
        print

