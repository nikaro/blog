---
title: "Un serveur de messagerie en moins de 30 minutes avec Modoboa"
date: "2016-10-23"
---

Un court article pour vous présenter une solution que j'ai découvert très recemment alors que je cherchais simplement une alternative à [PostfixAdmin](http://postfixadmin.sourceforge.net/) (qui vient de paraître en version 3.0 soit dit en passant). Il s'agit de [Modoboa](https://modoboa.org/fr/), dont voici ce qu'en dit le site de présentation :

Qu'est ce que c'est ?
---------------------

Modoboa est une plateforme d'hébergement de courriel munie d'une interface web simple et moderne de gestion. Elle fournit des composants utiles tels qu'une console d'administration, une console pour Amavis et un webmail.

Installer Modoboa
-----------------

```
# git clone https://github.com/modoboa/modoboa-installer
# cd modoboa-installer
# sudo ./run.py your.domain.tld
```

Pour avoir testé rapidement l'installation dans un conteneur, celle-ci est réellement aussi simple que ça et est fonctionnelle une fois que l'installateur a terminé de s'exécuter. Autrement dit il n'y a que la configuration d'enregistrements DNS (MX, SPF, DKIM et DMARC) et l'exécution d'un script qui vous sépare de la possibilité d'avoir votre propre serveur de messagerie auto-géré/auto-hébergé.

Le projet est écrit en Python, avec Django, et comme c'est mon joujou du moment ça plaît assez :-) Dernièrement il y a le [support de Let's Encrypt](https://modoboa.org/fr/weblog/2016/10/22/lets-encrypt-support/) qui a été ajouté, donc pas besoin de se casser la tête pour la configuration de TLS non plus. Puis le projet est modulaire, donc il y a la possibilité d'installer ou non certains modules, et d'en rajouter d'autres, comme un [frontend](https://github.com/modoboa/modoboa-radicale) à [Radicale](http://radicale.org/) pour la gestion des contacts et agendas.

Pour ceux qui préfèrent encore installer leur serveur de messagerie brique par brique, afin de comprendre et pouvoir maîtriser le fonctionnement de celui-ci jusque dans ses entrailles, je ne peux que vous recommander la [« recette de cuisine » de Liberasys pour monter son serveur de messagerie collaboratif](http://www.liberasys.com/recette-de-cuisine-serveur-de-messagerie-collaborative-inter-operant-et-sans-extensions-sisi/). Ça prendra juste un peu plus de 30 minutes, mais c'en sera d'autant plus enrichissant :-)
