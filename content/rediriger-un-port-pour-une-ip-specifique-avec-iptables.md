Title: Rediriger un port pour une IP spécifique avec iptables
Date: 2019-02-07 19:26
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, floss, informatique, sécurité
Slug: rediriger-un-port-pour-une-ip-specifique-avec-iptables
Status: published

Toujours dans une optique de contourner des restrictions de pare-feu, on va voir un truc assez simple pour rediriger un port vers au autre uniquement pour les paquets provenant d'une IP donnée. Deux cas de figure où ça peut s'avérer utile :

- vous êtes au travail, vous avez besoin d'accéder à un service sur votre serveur qui tourne sur un port bloqué par le pare-feu de la boite
- vous avez des machines chez un client, elles doivent pouvoir communiquer entre elles sur un port qui n'a pas été autorisé

C'est tout simple ça se fait avec une seule commande sur le serveur qu'on veut joindre :

```
iptables \
 -t nat \
 -I PREROUTING \
 --src <ip-source> \
 --dst <ip-du-serveur> \
 -p tcp \
 --dport <port-intial> \
 -j REDIRECT \
 --to-ports <port-bloqué>
```

On utilise donc `iptables`, l'outil qui permet de gérer les règle de pare-feu du noyau Linux, avec les arguments suivants :

- `-t nat` : on indique qu'on veut utiliser la table `nat` qui gère donc la [translation d'adresse réseau](https://fr.wikipedia.org/wiki/Network_address_translation), la table par défaut étant `filter`
- `-I PREROUTING` : on insère notre règle dans la chaîne `PREROUTING`, qui permet d'appliquer des actions sur les paquets avant qu'ils ne soient routés vers pour la machine elle-même (et la chaîne `INPUT`) ou vers une autre machine (et la chaîne `FORWARD`)
- `--src <ip-source>` : pour appliquer la règle uniquement en provenance d'une IP donnée
- `--dst <ip-du-serveur>` : pour appliquer la règle uniquement à destination d'une IP donnée
- `-p tcp` : on traite du traffic TCP
- `--dport <port-initial>` : le port de destination du point de vue du client, donc celui qu'on va rediriger vers le « vrai » port de destination
- `-j REDIRECT` : on envoie vers la cible `REDIRECT` qui fait ce que son nom indique :-)
- `--to-ports <port-bloqué>` : le port vers lequel rediriger

Exemple, en admettant que l'IP publique de mon lieu de travail soit 1.2.3.4 et celle de mon serveur 5.6.7.8, et que je veuille faire passer le traffic pour mon serveur OpenVPN à travers le port 443 (initialement dédié au HTTPS) :

```
iptables \
 -t nat \
 -I PREROUTING \
 --src 1.2.3.4 \
 --dst 5.6.7.8 \
 -p tcp \
 --dport 443 \
 -j REDIRECT \
 --to-ports 1194
```

Alors bien évidemment, pour cet exemple il faut que depuis mon lieu de travail je n'ai pas besoin d'accéder au service HTTPS sur mon serveur (adieu la consultation de mon blog perso). Aussi, si le traffic est filtré par un proxy ça risque de ne pas fonctionner. Mais voilà ça peut parfois dépanner.

Pour virer cette règle, on remplace `-I` par `-D`, car on veut `delete` au lieu de `insert` :

```
iptables \
 -t nat \
 -D PREROUTING \
 --src 1.2.3.4 \
 --dst 5.6.7.8 \
 -p tcp \
 --dport 443 \
 -j REDIRECT \
 --to-ports 1194
```

Ou sinon, en utilisant le numéro de la règle :

```
# liste les règles de la table `nat`
iptables -t nat -L --line-numbers

# on supprime la règle `<num>` dans la chaîne `PREROUTING`
iptables -t nat -D PREROUTING <num>
```
