---
title: "J'ai fait pipis"
date: "2018-05-17"
categories: ["Articles"]
tags: ["adminsys", "devops", "floss", "informatique", "python"]
slug: "jai-fait-pipis"
---

Commençons par dire que je suis assez fière de mon titre :-D  
  
Continuons en expliquant ce qu'est pipis.

Que'est-ce que pipis ?
----------------------

> « pipis » signifie « pip isolated » \\  
>   
> je trouvais le nom marrant, mais [pipi](https://pypi.org/project/pipi/) était déjà pris…

[Pipis](https://pypi.org/project/pipis/) est un wrapper autour de venv et pip qui installe les paquets python dans des venvs séparés. Ça permet d'éviter de potentiellement pourrir votre système avec les paquets que vous installez, et ça permet également d'éviter les problèmes de conflit de dépendances entre les différents paquets.

Pour chaque paquet installé ça lui créer un venv dans `~/.local/venvs/`, dans lequel `pip` est mis à jour vers la dernière version, puis le paquet et ses dépendances sont installées. Et pour terminer ça créer un lien symbolique des exécutables du paquet dans `~/.local/bin/` (qui doit être présent dans votre `PATH` pour que ça ai un intérêt).

Pourquoi ne pas utiliser pipsi ?
--------------------------------

[Pipsi](https://pypi.org/project/pipsi/) (`echo pipis | sed 's/is/si/'`) existe déjà et fait déjà le job, pourriez-vous dire. En effet, c'est d'ailleurs de cet outil que je me suis inspiré. On peut même dire que `pipis` est une réécriture de `pipsi`, simplement je me suis cantonné à Linux, Python 3, et `venv` à la place de `virtualenv`.

Pipsi de son côté semble supporter Windows, personnellement je me fiche de Windows, je ne l'utilise pas, et de toute manière il y a maintenant le [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) intégré qui permet d'avoir un ~~vrai~~ shell Linux dans Windows. MacOS ne devrait pas poser de problème, mais je n'en ai pas sous la main pour tester.

Python 2 c'est bientôt déprécié, je ne vois pas l'intérêt de tenter de maintenir une compatibilité avec. Autant le pousser vers la sortie.

Pour ce qui est de `virtualenv`, le truc qui me dérange c'est qu'il copie le binaire de Python dans l'environnement. Ce qui fait qu'on se retrouver avec un binaire Python qui ne sera jamais mis à jour. `venv` à l'élégance de simplement faire un lien symbolique, du coup quand la distribution Python est mise à jour dans le système, c'est à jour dans l'environnement virtuel aussi. Il reste que `pip` est copié statiquement, donc on retrouve le même problème, c'est pourquoi je me le met à jour en premier à chaque fois.

Comment l'installer ?
---------------------

```
python3 -m venv ~/.local/venvs/pipis
source ~/.local/venvs/pipis/bin/activate
pip install -U pip
pip install pipis
deactivate
ln -s ~/.local/venvs/pipis/bin/pipis ~/.local/bin/pipis
```

Comment ça s'utilise ?
----------------------

Pour ça je vous laisse aller voir la [page du projet sur PyPI](https://pypi.org/project/pipis/), mais voilà tout de même un aperçu de ce que ça peut faire.

Bonus
-----

Et en bonus, rien que pour vous, vu que ça utilise la bibliothèque [Click](http://click.pocoo.org/6/) il est possible d'activer la complétion dans le terminal. Il suffit d'ajouter ça dans votre `.bashrc` :

```
eval "$(_PIPIS_COMPLETE=source pipis)"
```
