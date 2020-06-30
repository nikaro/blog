Title: Réparer un fichier système corrompu sur une Debian
Date: 2020-05-28 15:49
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, debian, informatique
Slug: reparer-un-fichier-systeme-corrompu-sur-une-debian
Status: published

Au boulot je suis tombé sur une machine sur laquelle le fichier `/usr/lib/python2.7/os.py` a visiblement été écrasé lors d'une mauvaise manipulation. Il contenait un extrait de XML, autrement dit pas vraiment le contenu attendu. Voici donc un petit mémo expliquant comment on répare ça.

Dans un premier temps il faut trouver à quel paquet appartient le dit fichier :

```
# dpkg -S /usr/lib/python2.7/os.py
python2.7-minimal: /usr/lib/python2.7/os.py
```

La difficulté ici est qu'il s'agit d'un fichier utilisé par apt-get (ou dpkg ?) lui-même, si ce n'était pas le cas il aurait suffit d'un `apt-get install --reinstall <paquet>` et ça aurait probablement été corrigé. Là ça causait une erreur.

Il faut donc télécharger le paquet :

```
# apt-get download python2.7-minimal
```

Extraire le contenu :

```
# dpkg-deb -xv python2.7-minimal_2.7.3-6+deb7u2_i386.deb ./tmp/
```

Et restaurer le fichier en question :

```
# cp -v ./tmp/usr/lib/python2.7/os.py /usr/lib/python2.7/os.py
```

Ensuite, en cas de doute, vous pouvez vérifier l'intégrité du reste des fichiers avec l'utilitaire `debsums` :

```
# apt-get install debsums
# debsums python2.7-minimal
/usr/bin/python2.7                                                            OK
/usr/include/python2.7/pyconfig.h                                             OK
/usr/lib/python2.7/ConfigParser.py                                            OK
/usr/lib/python2.7/StringIO.py                                                OK
/usr/lib/python2.7/UserDict.py                                                OK
/usr/lib/python2.7/__future__.py                                              OK
[...]
```
