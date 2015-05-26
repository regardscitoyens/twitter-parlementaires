## Annuaire des comptes Twitter des parlementaires

Des citoyens et associations nous sollicitent souvent pour disposer de la liste de tous les comptes Twitter des députés ou des sénateurs.

L'Assemblée et le Sénat maintenant désormais des listes officielles des comptes de leurs élus, nous récupérons ces listes et réassocions automatiquement les comptes aux identifiants de chaque parlementaire afin de les intégrer aux bases de données de [NosDéputés.fr](http://www.nosdeputes.fr) et [NosSénateurs.fr](http://www.nossenateurs.fr) et donc également à leurs [API](http://cpc.regardscitoyens.org/trac/wiki/API).

Vous pouvez donc télécharger les données aux différentes adresses suivantes (changer csv en json ou xml dans lesurl pour les formats éponymes) :
- pour les députés :
 + [sur ce git](https://github.com/regardscitoyens/twitter-parlementaires/blob/master/data/deputes.csv) (pour avoir les métadonnées twitter associées aux identifiants AN et NosDéputés)
 + [ou via l'API de NosDéputés.fr](http://www.nosdeputes.fr/deputes/csv) (pour avoir les métadonnées parlementaires complétées du seul identifiant twitter)
- pour les sénateurs :
 + [sur ce git](https://github.com/regardscitoyens/twitter-parlementaires/blob/master/data/senateurs.csv) (pour avoir les métadonnées twitter associées aux identifiants AN et NosDéputés)
 + [ou via l'API de NosDéputés.fr](http://www.nossenateurs.fr/senateurs/csv) (pour avoir les métadonnées parlementaires complétées du seul identifiant twitter)

Ces données sont mises-à-jour quotidiennement et redistribuées sous la licence OpenData [ODBL](http://www.vvlibri.org/fr/licence/odbl/10/fr/legalcode).

Pour installer et lancer la collecte :
```bash
bin/install.sh #(will ask for sudo rights to install pip & virtualenv)
bin/build.sh
```

[Regards Citoyens](http://www.regardscitoyens.org)
