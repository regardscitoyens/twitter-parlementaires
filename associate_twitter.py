#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json, re
from datetime import datetime
from itertools import chain
from twitter import Twitter, OAuth
from twitterconfig import KEY, SECRET, OAUTH_TOKEN, OAUTH_SECRET
twitterConn = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, KEY, SECRET))

if len(sys.argv) < 3:
    sys.stderr.write("Please input deputes/senateurs and the path for the Twitter list data\n")
    exit(1)


# Read Parls data
typeparls = sys.argv[1]
typeparl = typeparls.rstrip("s")
goodparls = []

with open(os.path.join(".cache", "%s.json" % typeparls)) as f:
    try:
        parls = dict((parl["slug"], parl) for parl in [p[typeparl] for p in json.load(f)[typeparls]])
    except ValueError:
        sys.stderr.write("Could not open Nos%s.fr parlementaires list" % typeparls)
        exit(1)


# Read Twitter list data
with open(sys.argv[2]) as f:
    twitter = json.load(f)

# Exclude bad accounts
notparls = ["bayrou", "ABachelay"]
groupes = ["crcsenat", "udiuc", "ecolosenat", "senateursps", "senateursump", "lesrep_senat"]
doublons = ["teambouillon", "fdebeauce", "vignal2012", "deputecvautrin", "clergeau2012", "isabellebruneau", "roussetalain", "elubondy", "FLefebvre_UMP", "Gabouty2012", "moniquerabin", "PascalAllizard", "pascalegruny", "sergiocoronado", "audeluquet", # 2012-2017
"Darrieussecq", "MireilleRobert", "tamarelle_marie", "Fdumas2017", "stelladupont2", "karamanli72", "micheldelpon"] # 2017-2022
dead = ["Guy_Delcourt", "ConchitaLacuey", "MichelVERGNIER", "bernardroman59", "AndrSaint", "LucetteLousteau", "CathLEMORTON", "EPhilippe_LH", # 2012-2017
"celiadeputee2017", "davidlorion", "PascalBois2017", "DipompeoChris", "Vincent.Ledoux59", "valeriebeauvais2017", "Josso2017", "ColasRoy2017", "Marc_Delatte", "EricDiardDepute", "bernarddeflesselles", "sttrompille", "pgoulet58", "GCHICHE2017", "obono2017"  # 2017-2022
]
badlinks = ["http://www.facebook.fr/pascalbois2017", "https://fr-fr.facebook.com/GuillaumePeltier", "https://www.facebook.com/valerie.boyer.56", "https://www.facebook.com/Marguerite-Deprez-Audebert-2017-420349688340872", "https://fr-fr.facebook.com/colas.roy.2017", "https://m.facebook.com/ThomasRudigoz2017", "https://www.facebook.com/BSmedoc", "https://fr-fr.facebook.com/sandramarsaudlarepubliquenmarche", "https://fr-fr.facebook.com/profile.php"]

excludes = [t.lower() for t in notparls + groupes + doublons + dead]
for e in excludes:
    if e in twitter:
        twitter.pop(e)


# Logging
def log(msg, typ):
    print("[%s/%s] %s" % (typ.upper(), typeparls, msg))

def log_status():
    log("%s todo, %s parls left, %s good" % (len(twitter), len(parls), len(goodparls)), "info")


# Cleaning regexps
accents = [(re.compile(r), s) for r, s in [
    (u'[àÀâÂ]', 'a'),
    (u'[éÉèÈêÊëË]', 'e'),
    (u'[îÎïÏ]', 'i'),
    (u'[ôÔöÔ]', 'o'),
    (u'[ùÙûÛüÜ]', 'u'),
    (u'[çÇ]', 'c'),
]]
def clean_accents(t):
    if not isinstance(t, unicode):
        t = t.decode('utf-8')
    for r, s in accents:
        t = r.sub(s, t)
    return t

re_clean = re.compile(r'[^a-z]+', re.I)
nospaces = lambda x: re_clean.sub('', x)
clean = lambda x: re_clean.sub(' ', clean_accents(x.lower())).strip()

re_clean_desc = re.compile(r"[\s\n]+")
clean_desc = lambda x: re_clean_desc.sub(" ", x)

re_clean_twiturl = re.compile(r"^.*twitter.com/(?:#!/)*([^/]+).*$", re.I)
clean_twiturl = lambda x: re_clean_twiturl.sub(r"\1", x).strip()

re_clean_url = re.compile(r"^((?:https?://)?(?:(?:www2?|m|fr|fr-fr|deputation)\.)?)(.*?)/?$", re.I)
check_url = lambda x: re_clean_url.sub(r"\2", x.strip().lower())
clean_url = lambda x: re_clean_url.sub(r"\1\2", x.strip())

re_clean_facebook = re.compile(r"(facebook.com/.*?/?(\?id=.*?)?)([?&].*|#.*|/photos/.*)*$", re.I)
re_clean_facebook2 = re.compile(r"(facebook.com/)www.facebook.com/", re.I)
clean_facebook = lambda x: re_clean_facebook.sub(r"\1", re_clean_facebook2.sub(r"\1", x.replace("%C3%A9", u"é")))

re_clean_initiales = re.compile(r"^([A-Z]{1,2}[\. ]+)+(d('|[eus]+ (la )?))?")
clean_initiales = lambda x: nospaces(clean(re_clean_initiales.sub("", x.strip())))

re_reorder = re.compile(r"^(.+)\s+(\S+)$")
reorder = lambda x: re_reorder.sub(r"\2 \1", x.strip())

re_reorder_part = re.compile(r"^(.+)\s+\((d.*)\)$")
reorder_part = lambda x: re_reorder_part.sub(r"\2 \1", x.strip())

re_split = re.compile(r"([A-Z])")
split_twid = lambda x: [clean(w) for w in re_split.sub(r" \1", x).strip().split(" ")]


# Start matching
log_status()

def store_one(twid, parl, slug):
    try:
        tw = twitter.pop(twid.lower())
    except KeyError:
        try:
            tw = twitterConn.users.show(screen_name=twid)
        except:
            return log("Could not get info on Twitter account https://twitter.com/%s" % twid, "warning")
        log("Twitter account %s for %s found in urls but missing from list" % (twid.encode("utf-8"), parl['nom'].encode("utf-8")), "info")
    parl['twitter'] = twid
    parl['twitter_data'] = tw
    goodparls.append(parl)
    parls.pop(slug)

# First try to find twitter urls in each parl websites list
for slug in parls.keys():
    parl = parls[slug]
    found = False
    for url in list(parl["sites_web"]):
        if "senat.fr" in url["site"] or "assemblee-nationale.fr" in url["site"]:
            parl["sites_web"].remove(url)
        elif "twitter" in url["site"] and not found:
            twid = clean_twiturl(url['site'].decode("utf-8"))
            if twid.lower() in excludes:
                parl["sites_web"].remove(url)
                continue
            found = True
            store_one(twid, parl, slug)

if len(goodparls):
    log_status()

# Then try to identify parl from matching his metadata to the name, urls and description from Twitter
urlentities = lambda tw: [u["expanded_url"] for u in tw["entities"].get("url", {"urls": []})["urls"]]
def match_parl(tw):
    twid = tw["screen_name"]
    urls = [check_url(u) for u in urlentities(tw) if u]
    possible = []

    name = clean(tw["name"])
    namenospaces = nospaces(name)
    subnames = set(chain(*[name.split(" ", i) for i in [1,2,3]]))

    for slug in parls.keys():
        parl = parls[slug]

        # Try to match the full name
        check = nospaces(clean(parl["nom"]))
        if namenospaces == check:
            return store_one(twid, parl, slug)

        # Try to replace first name in the right place
        reordname = reorder(name)
        while reordname != name:
            if nospaces(clean(reordname)) == check:
                return store_one(twid, parl, slug)
            reordname = reorder(reordname)

        # Try to find family name matches only
        checkfam = nospaces(clean(reorder_part(parl["nom_de_famille"])))
        if namenospaces == checkfam:
            possible.append(parl)
        else:
            for word in subnames:
                if len(word) > 3 and nospaces(clean(word)) == checkfam:
                    possible.append(parl)

        # Try to remove first name as initiales
        if parl not in possible and clean_initiales(tw["name"]) == checkfam:
            possible.append(parl)

        # Try to search name in twitter id
        if parl not in possible:
            for word in split_twid(twid):
                if len(word) > 3 and word == checkfam:
                    possible.append(parl)

        # Try to match a url
        for url in urls:
            if url in [check_url(u["site"]) for u in parl["sites_web"]] + [check_url(parl.get('url_an', parl.get('url_institution', '')))]:
                return store_one(twid, parl, slug)

    # Check matches by family name found
    if possible:
        if len(possible) == 1:
            return store_one(twid, possible[0], possible[0]["slug"])
        log("Multiple parls found for %s: %s" % (twid, " ".join([p["slug"] for p in possible])), "warning")

for tw in twitter.values():
    match_parl(tw)

log_status()
if len(twitter):
    log("%s Twitter accounts could not be matched to any parl: %s" % (len(twitter), ", ".join(twitter.keys())), "warning")


# Write output data
if not os.path.isdir("data"):
    os.makedirs("data")

formatcsv = lambda x: '"%s"' % x.encode("utf-8").replace('"', '""') if type(x) == unicode else str(x)

headers = ["twitter", "nom", "nom_de_famille", "prenom", "sexe", "twitter_tweets", "twitter_followers", "twitter_following", "twitter_listed", "twitter_favourites", "twitter_verified", "twitter_protected", "twitter_id", "twitter_name", "twitter_description", "twitter_created_at", "sites_web", "url_institution", "slug", "url_nos%s_api" % typeparls]

orderparls = sorted(goodparls, key=lambda x: "%s - %s" % (x["nom_de_famille"], x["prenom"]))
with open(os.path.join("data", "%s.csv" % typeparls), "w") as f:
    print >> f, ",".join(headers)
    for parl in orderparls:
        tw = parl["twitter_data"]
        parl["twitter_id"] = tw["id"]
        parl["twitter_name"] = tw["name"]
        parl["twitter_created_at"] = datetime.strptime(tw["created_at"], '%a %b %d %H:%M:%S +0000 %Y').isoformat()
        parl["twitter_description"] = clean_desc(tw["description"])
        parl["twitter_tweets"] = tw["statuses_count"]
        parl["twitter_favourites"] = tw["favourites_count"]
        parl["twitter_followers"] = tw["followers_count"]
        parl["twitter_following"] = tw["friends_count"]
        parl["twitter_listed"] = tw["listed_count"]
        parl["twitter_verified"] = tw["verified"]
        parl["twitter_protected"] = tw["protected"]
        sites_web = set([clean_url(u) for u in [s["site"] for s in parl["sites_web"] if s] + [u for u in urlentities(tw) if u and "senat.fr" not in u and "assemblee-nationale.fr" not in u]])
        clean_sites = []
        done_sites = [check_url(u) for u in badlinks]
        for site in sorted(sites_web, key=lambda x: len(x)):
            if not site.startswith("http"):
                site = "http://" + site.lstrip("/")
            site = clean_facebook(site)
            cleaned = check_url(site)
            if cleaned not in done_sites:
                clean_sites.append(site)
                done_sites.append(cleaned)
        parl["sites_web"] = "|".join(clean_sites)
        if "url_institution" not in parl:
            parl["url_institution"] = parl["url_an"]
        parl["url_nos%s_api" % typeparls] = parl["url_nos%s_api" % typeparls].replace("/json", "/csv")
        print >> f, ",".join([formatcsv(parl[k]) for k in headers])
        parl["url_nos%s_api" % typeparls] = parl["url_nos%s_api" % typeparls].replace("/csv", "/json")
        parl["sites_web"] = parl["sites_web"].split("|")

with open(os.path.join("data", "%s.json" % typeparls), "w") as f:
    json.dump(orderparls, f, indent=2, sort_keys=True)
