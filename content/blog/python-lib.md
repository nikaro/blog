---
title: "Installer des bibliothèques tierces pour Python"
date: 2023-01-14T15:60:23+01:00
---

En Python, comme dans la plupart des langages de programmation, il est possible
d'utiliser des "bibliothèques". On parle aussi le "library" (en anglais), "lib"
en abgrégé, et "librairie" en franglais. Ces bibliotheques sont des programmes
qui vont venir étendre les fonctionnalités de base du langage. En Python il y a
ce qu'on appelle la *bibliothèque standard*, et les *bibliothèques tierces*.

## La bibliothèque standard

Il s'agit des bibliothèques qui sont livrées avec Python par défaut. On
l'appelle aussi la "stdlib", pour "standard library" en anglais. Vous pouvez
retrouver la liste des bibliothèques disponibles ici:
<https://docs.python.org/fr/3/library/>

Elles sont directement accessible à l'interpréteur Python, sans avoir à être
installées séparément.

Exemple:

```python
from pathlib import Path

if not Path("monfichier.txt").exists():
    print("le fichier n'existe pas")
```

Dans cet exemple on a utilisé la fonction `Path` fournie par la bibliothèques
standard `pathlib`.

## Les bibliothèques tierces

La stdlib Python est déjà très vaste, mais on a aussi la possibilité d'utiliser
les bibliothèques créées par des personnes extérieures au projet Python
officiel. On parle alors de "bibliothèques tierces", ou "third-party libraries"
en anglais.

Dans un projet vous allez pouvoir utiliser des bibliothèques créées par vos
soins, ou des bibliothèque créées par d'autres.

### Créer et utiliser sa propre biliothèque

Imaginons que vous avez un simple projet qui consiste en un seul fichier
`main.py` :

```python
#!/usr/bin/env python3

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

Vous voulez ajouter une fonction pour demander le nom de la personne, et vous
savez que allez la réutiliser par la suite dans d'autres endroits (d'autres
fichiers) de votre projet quand il aura grandit. Pour cela vous aller
créer votre bibliothèque en créant simplement un autre fichier, par exemple
`mylib.py` :

```python
def prompt_ask_name(prompt: str = "What's your name? ") -> str:
    return input(prompt)
```

Vous pouvez ensuite l'utiliser dans `main.py`:

```python
#!/usr/bin/env python3

from mylib import prompt_ask_name

def main():
    name = prompt_ask_name()
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

### Installer et utiliser une bibliothèque tierce

Pour vous faciliter les travail est aussi possible d'utiliser des bibliothèques
créées par d'autres.

Imaginons que dans votre projet vous vouliez faire des requêtes HTTP, il est
possible d'utiliser la bibliothèque standard
[`urllib`](https://docs.python.org/fr/3/library/urllib.html), mais celle-ci
n'est pas forcément très simple à utiliser. Nous pouvons alors chercher sur
PyPI si une bibliothèque répond à notre besoin.

[PyPI](https://pypi.org) est un dépôt, géré par le projet Python, où n'importe
qui peut mettre à disposition sa bibliothèque.

Pour installer une bibliothèque depuis PyPI il faut utiliser l'utilitaire
[pip](https://pip.pypa.io/en/stable/). Sous Windows et MacOS il est installé
par défaut lorsque vous installez Python. Sous Linux il est probable qu'il
faille installer un paquet supplémentaire, par exemple
[`python3-pip`](https://tracker.debian.org/pkg/python3-pip) sous Debian.

Pour installer la bibliothèque [HTTPX](https://pypi.org/project/httpx/),
qui simplifie l'utilisation de HTTP en Python, nous pouvons donc exécuter la
commande suivante :

```shell
python3 -m pip install httpx
```

Et ensuite l'utiliser comme ceci :

```python
import httpx

httpx.get("https://api.example.org/endpoint")
```

Il convient de faire attention dans le choix des bibliothèques tierces qu'on
utilise, afin de s'assurer qu'elles ne sont pas malicieuses par exemple.

## Environnement virtuels

Quand on commence à utiliser des bibliothèques tierces, on peut s'exposer à
des problèmes de conflits de version entre les bibliothèques du système ou
entre les différents projets.

Par exemple, sous Debian quand on installe une bibliothèque, il y a plusieurs
endroits où elle peut venir se mettre en fonction de la méthode utilisée :

* `~/.local/lib/python3.9/site-packages/httpx` si on l'installe avec pip
* `/usr/local/lib/python3.9/dist-packages/` si on l'installe avec pip en `root`
* `/usr/lib/python3/dist-packages/httpx` si on l'installe avec APT

Et ça peut vite devenir un joyeux bordel, ne sachant plus quelle version
est utilisée à quelle endroit, et même jusqu'à rendre instable le système.

C'est pourquoi quand on travaille sur des projets, à moins d'utiliser des
machines virtuelles dédiées ou des conteneurs, il est conseillé d'utiliser la
fonctionnalité d'environnement virtuel de Python, fournit par la bibliothèque
standard [`venv`](https://docs.python.org/fr/3/library/venv.html).

On parle aussi de *virtualenv* ou *venv* pour aller plus vite.

Lorsqu'on créer un environnement virtuel on va créer un dossier, à l'endroit
fournit, qui va contenir l'exécutable Python et éventuellement quelques outils
de base (comme pip). Et lorsqu'on va charger cet environnement virtuel, les
bibliothèques vont par exemple s'installer à l'intérieur de celui-ci, évitant
ainsi de *polluer* le système avec nos dépendances.

Par la suite, avant chaque utilisation du projet il faudra penser à charger
l'environnement virtuel, sinon le programme ne trouvera pas ses bibliothèques.
Et la fin, il faut également penser à désactiver l'environnement virtuel.

### Création et utilisation d'un environnement virtuel

Sous Linux il faut également installer un paquet, par exemple `python3-venv`
sous Debian.

Pour créer un environnement virtuel il faudra utiliser la commande `python3 -m
venv <dossier-venv>`, par exemple :

```shell
python3 -m venv ~/.cache/pyvenv/mon-projet
```

Pour charger l'environnement virtuel :

```shell
source ~/.cache/pyvenv/mon-projet/bin/activate
```

Vous pouvez ensuite vérifier avec la commande `which` le chemin que votre shell
va utiliser pour l'exécutable Python :

```shell
(mon-projet) nicolas@local ~/P/g/n/mon-projet > which python3
~/.cache/pyvenv/mon-projet/bin/python3
```

À partir de là, toutes vos bibliothèques vont s'installer dans
`~/.cache/pyvenv/mon-projet/lib/python3.10/site-packages/` sans *contaminer*
votre système.

Pour sortir de l'environnement virtuel il suffit d'utiliser la commande :

```shell
deactivate
```

## Quelques commandes pip

* Afficher l'aide : `python3 -m pip --help` ou `python3 -m pip <commande> --help`
* Installer un paquet : `python3 -m pip install <paquet>`
* Désinstaller un paquet : `python3 -m pip uninstall <paquet>`
* Lister les paquets installés : `python3 -m pip freeze`
* Installer les paquets à partir d'un fichier : `python3 -m pip install -r <fichier>`
