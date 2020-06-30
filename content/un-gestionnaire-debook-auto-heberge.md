Title: Un gestionnaire d'eBook auto-hébergé
Date: 2016-06-27 09:11
Author: Nicolas Karolak
Category: Articles
Tags: auto-hébergement, floss, informatique, livres
Slug: un-gestionnaire-debook-auto-heberge
Status: published

Alors que je cherchais quelques bouquins de la collection « [3 minutes pour comprendre](http://www.editions-tredaniel.com/minutes-pour-comprendre-c-32_1266.html) », j'ai vu que certains étaient disponibles au [format eBook](http://www.decitre.fr/rechercher/result/index?category=3770&q=3+minutes+pour+comprendre). Bon je vais aller sur la version papier pour le moment car je préfère avoir un livre entre les mains et tourner les pages, puis je ne suis pas sûr du rendu de l'eBook sur un liseuse… Mais avoir tous ses livres à portée sur sa liseuse/tablette/smartphone c'est plutôt pratique.

Le « problème » c'est que sur ma tablette et mon smartphone j'utilise l'application [Google Play Livre](https://play.google.com/store/apps/details?id=com.google.android.apps.books&hl=fr), du coup je me suis demandé s'il existait une alternative libre et auto-hébergée. En cherchant un peu je suis donc tombé sur [COPS](http://blog.slucas.fr/en/oss/calibre-opds-php-server) (Calibre OPDS PHP Server), comme son nom l'indique il s'agit d'un serveur [OPDS](http://opds-france.org/) (standard pour la distribution de contenus numériques) qui semble-t-il s'appuie sur une base de données [Calibre](http://calibre-ebook.com/) et permet de lire ses eBooks via un client OPDS ou une interface Web.

Pour ceux qui veulent tester, il y a une instance de démonstration :

-   interface Web : http://cops-demo.slucas.fr/index.php
-   URL pour client OPDS : http://cops-demo.slucas.fr/feed.php

Bon ce n'est pas ce qui se fait de plus joli et ergonomique, mais pour les libristes intègres (il faudrait dire intégristes plutôt, non ? :-D) ça devrait faire l'affaire. Après en dehors de l'interface Web ça dépend du client utilisé, il y en a qui ont l'air pas mal notamment [FBReader](https://fbreader.org/FBReaderJ) qui n'a aucun lien avec Facebook et est disponible sur F-Droid. Et pour les plus motivés, le code est sur [GitHub](https://github.com/seblucas/cops), donc rien ne vous empêche de contribuer.

Pour ma part je reste avec mes livres papiers pour le moment, mais quand j'aurais sauté le pas de la lecture de livres numériques je pense que je me tenterais une installation.
