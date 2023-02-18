---
title: "Faire des requêtes HTTP en Python"
date: 2023-01-14T14:40:00+01:00
---

Imaginons que nous voulions faire une requête vers l'API publique de GitHub,
sur l'URL suivante : `https://api.github.com/users/<user>/repos`

Dans un premier temps on peut tester avec `curl` pour voir à quoi ressemble
le résultat :

```shell
curl https://api.github.com/users/nikaro/repos
```

Pour cet exemple on obtient du JSON en réponse, bonne nouvelle Python sait
travailler nativement avec JSON.

## urllib

Si on veut utiliser la bibliothèque standard de Python, on peut utiliser
[`urllib`](https://docs.python.org/fr/3/library/urllib.html) et 
[`json`](https://docs.python.org/fr/3/library/json.html).

```python
import json
import urllib.request

# on fait la requête HTTP
response = urllib.request.urlopen("https://api.github.com/users/nikaro/repos")
# on lit le contenu de la réponse
content_bytes = response.read()
# on décode la réponse au format binaire vers texte
content_string = content_bin.decode()
# on parse le texte en tant que JSON afin de "convertir" en objet Python
data = json.loads(content_text)

print(data[0]["htlm_url"])
```

## httpx

Si on veut se faciliter la vie, surtout quand on commence à faire des choses
plus compliqués, on peut utiliser la bibliothèque tierce
[HTTPX](https://www.python-httpx.org).

```python
import httpx

response = httpx.get("https://api.github.com/users/nikaro/repos")
data = response.json()
```
