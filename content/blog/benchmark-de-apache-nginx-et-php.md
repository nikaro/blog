---
title: "Benchmark de Apache, NGINX et PHP"
date: "2016-07-04"
categories: ["Articles"]
tags: ["adminsys", "floss", "informatique", "php", "web"]
slug: "benchmark-de-apache-nginx-et-php"
---

À la suite d'un commentaire de schizorn soulevant qu'il se dit un peu tout et son contraire au sujet des performances de PHP sous Apache avec mod\_php ou PHP-FPM, chose que j'avais également constaté lors de ma rédaction des articles sur le sujet. Je me suis décidé à faire moi-même un benchmark de l'un et l'autre, puis avec NGINX également au passage histoire d'être complet.

Protocole de tests
------------------

Pour réaliser ce benchmark j'ai donc lancé un conteneur LXD pour chaque configuration, sous Ubuntu 16.04. Ce dernier ne proposant que PHP7, j'ai utilisé [ppa:ondrej/php](https://launchpad.net/~ondrej/+archive/ubuntu/php) pour avoir PHP5 également. À chaque fois j'ai laissé la configuration par défaut pour Apache, NGINX et PHP.

J'ai fais mes mesures en attaquant un [script PHP de benchmark](http://www.php-benchmark-script.com/) dans un premier temps. Et ensuite une installation de WordPress, identique sur chaque conteneur (chacun avec son instance de MariaDB en local également).

J'ai utilisé les outils suivants :

- la commande cURL en faisant la moyenne du résultat sur 6 exécutions
- l'outil [ab](https://httpd.apache.org/docs/current/programs/ab.html)

Passons donc aux résultats :-)

Résultats
---------

Commande : `for i in {1..6}; do curl -s -w "%{time_total}\n" -o /dev/null <server>/bench.php; done`

- PHP 5.6

| Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|:----------------:|:----------------:|:---------------:|
| **2.847 sec.**   | 2.946 sec.       | 2.965 sec.      |

- PHP 7.0

| Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|:----------------:|:----------------:|:---------------:|
| 1.062 sec.       | **1.054 sec.**   | 1.103 sec.      |

Commande : `for i in {1..6}; do curl -s -w "%{time_total}\n" -o /dev/null <server>/wordpress; done`

- PHP 5.6

| Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|:----------------:|:----------------:|:---------------:|
| 0.158 sec.       | 0.161 sec.       | **0.156 sec.**  |

- PHP 7.0

| Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|:----------------:|:----------------:|:---------------:|
| **0.076 sec.**   | 0.082 sec.       | 0.089 sec.      |

Commande : `ab -n 100 -c 30 http://<server>/bench.php`

- PHP 5.6

|                | Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|----------------|:----------------:|:----------------:|:---------------:|
| Time           | **74.741 sec.**  |   82.376 sec.    |   79.691 sec.   |
| Requests/sec.  | **1.34**         |   1.21           |   1.25          |

- PHP 7.0

|                | Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|----------------|:----------------:|:----------------:|:---------------:|
| Time           | **26.078 sec.**  | 29.697 sec.      | 31.080 sec.     |
| Requests/sec.  | **3.83**         | 3.37             | 3.22            |

Commande : `ab -n 100000 -c 30 http://<server>/wordpress`

- PHP 5.6

|                | Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|----------------|:----------------:|:----------------:|:---------------:|
| Time           | 5.665 sec.       | 5.667 sec.       | **5.475 sec.**  |
| Requests/sec.  | 17652.05         | 17644.83         | **18263.30**    |

- PHP 7.0

|                | Apache + mod_php | Apache + php-fpm | NGINX + php-fpm |
|----------------|:----------------:|:----------------:|:---------------:|
| Time           | 5.680 sec.       | 5.816 sec.       | **5.436 sec.**  |
| Requests/sec.  | 17606.91         | 17194.01         | **18395.84**    |

Aucun changement constaté si on incrémente le nombre de StartServers dans la configuration du MPM Event.

Conclusion
----------

Commeçons par ce qui est évident et sans surprise. PHP7 coiffe au poteau PHP5 sur l'exécution de scripts PHP pur ou avec l'utilisation de cURL. Cependant, et là c'est une surprise, sur WordPress avec l'outil ab, théoriquement plus proche de ce qu'il se passe dans la réalité, il ne semble pas y avoir d'avantage pour PHP7 (sauf avec NGINX), au contraire ! Toutefois on peut supposer pour le moment WordPress est plutôt optimisé pour PHP5.

Pour ce qui est du match « **mod\_php VS. PHP-FPM** », la différence est très légère et dans la plupart des cas négligeable. Toutefois il faut concéder que mod\_php est le vainqueur en ce qui concerne la rapidité d'éxecution. Ce résultat semble logique dans la mesure où PHP est chargé directement dans le processus du serveur Web, et donc qu'il n'y a pas à faire l'opération supplémentaire de transmettre l'exécution des scripts à un processus extérieur.

À noter que PHP-FPM permet des choses que mod\_php ne permet pas, comme par exemple déléguer l'exécution de PHP à différents utilisateurs (via les pools) ou encore répartir la charge de l'exécution de PHP entre différents serveurs. Donc si mod\_php est effectivement plus performant sur une installation simple, lorsqu'on commence à avoir des besoins de cloisonnement et/ou qu'on travaille sur de grosses infrastructure, l'utilisation de PHP-FPM s'impose d'elle-même.

Pour ce qui est du match « **Apache VS. NGINX** », on constate que pour ce qui est du PHP pur c'est Apache qui s'en sort le mieux, d'autant plus avec mod\_php. Cependant pour ce qui est d'un cas plus proche de la réalité d'usage, comme WordPress, on constate que c'est NGINX s'en sort le mieux. Peut-être n'y a-t-il pas assez de PHP dans la page d'accueil du WordPress pour que ça génère une charge significative, ou peut-être gère-t-il mieux l'appel aux processus FastCGI que ne le fait Apache… Mystère, je ne sais pas trop comment interpréter ce résultat.

Pour terminer, voilà les quelques recommandations que je pourrais faire :

- simplicité --> Apache + mod_php
- sécurité --> Apache + PHP-FPM
- performances --> NGINX

Et le must serait certainement un NGINX avec mise en cache en frontal, et Apache avec mod\_php ou PHP-FPM en backend.
