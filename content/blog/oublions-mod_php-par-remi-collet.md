---
title: "« Oublions mod_php », par Remi Collet"
date: "2016-06-18"
categories: ["Articles"]
tags: ["adminsys", "floss", "informatique", "php", "vidéos", "web"]
slug: "oublions-mod_php-par-remi-collet"
---

Un petit article juste pour nous partager une conférence de [Remi Collet](http://blog.remirepo.net/post/2016/05/27/PHP-Tour-Clermont-Ferrand-2016) sur le thème « [Oublions mod\_php](https://www.youtube.com/watch?v=onSzYyv4yj8) », elle est super intéressante et j'y ai appris pas mal de choses. Notamment que l'utilisation de `mod_fastcgi` et de la directive `AddHandler` dans Apache, que je préconise dans mon article sur [l'utilisation de PHP-FPM dans Apache](https://blog.karolak.fr/2016/03/14/apache-mode-event-et-php-fpm/), sont déconseillés car dépréciés. Il faudrait plutôt utiliser `mod_fcgid` et `SetHandler`. Je tâcherais donc de publier assez rapidement un nouvel article sur le sujet prenant en compte ces informations.

Bon visionnage !

<iframe id='ivplayer' width='640' height='360' src='https://invidious.fdn.fr/embed/onSzYyv4yj8' style='border:none;'></iframe>
