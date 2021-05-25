---
title: "Apache, mode Event et PHP-FPM"
date: "2016-03-14"
---

Suite à mon article sur [les raisons de mon retour sous Apache](https://blog.karolak.fr/2016/03/14/pourquoi-je-reviens-a-apache-apres-etre-passe-a-nginx/), voici comme promis un tuto sur l'installation de Apache en [mode Event](https://httpd.apache.org/docs/current/mod/event.html) avec PHP-FPM. Mais avant la pratique, un peu de théorie.

### Explications

Qu'est-ce que le mode « *event* » de Apache ? Pourquoi l'utiliser ? Et pourquoi *PHP-FPM* ? Pour répondre à ces questions, il faut comprendre comment Apache fonctionne.

> **TL;DR :** Le mode *event* est plus performant que le mode *prefork* utilisé par défaut, ceci grâce à une meilleure gestion de la mémoire. *PHP-FPM* permet de faire tourner PHP dans un processus séparé, sous des utilisateurs différents, et puis toute façon on a pas le choix de l'utiliser ou non à cause du mode *event* qui nous l'impose.

Historiquement, et dans la plupart des cas aujourd'hui encore, Apache est utilisé par défaut en mode *prefork*. Dans ce mode, un [processus](https://fr.wikipedia.org/wiki/Processus_%28informatique%29) parent Apache est lancé, et il lance à son tour un nombre limité de processus enfants. Chaque processus enfant est plus ou moins une instance à part entière de Apache, qui chacun charge toute la configuration, les modules, etc. Ainsi, lorsqu'un client fait une requête HTTP, celle-ci est prise en charge par un processus qui va lui être entièrement dédié. Si un autre client fait une requête, celle-ci va être assignée à un autre processus, ou alors attendre qu'il y en ai un qui se libère s'ils sont tous occupés. Ce fonctionnement est très consommateur en mémoire vive, et pas forcément ce qui fait de plus réactif.

Une autre approche, plus intéressante, est d'utiliser le mode *worker*. Celui-ci, en plus de lancer plusieurs processus comme le mode *prefork*, va permettre l'utilisation de plusieurs *[threads](https://fr.wikipedia.org/wiki/Thread_%28informatique%29)* (fils d'exécution, ou unités de traitement) dans chaque processus. L'avantage des *threads* sur les processus est que ceux-ci se lancent beaucoup plus rapidement, et du fait qu'ils partagent entre-eux le même espace d'adressage (et partagent donc les variables, etc.) la communication entre les différents *threads* est plus rapide et consomme moins de mémoire. Les processus quant à eux sont totalement isolés les uns des autres. Ainsi, chaque communication HTTP est attribuée à un *thread* différent, plutôt qu'à un processus. (Cf. cet article [Les processus sous Linux](http://www.it-connect.fr/les-processus-sous-linux/) qui explique très bien le fonctionnement des processus et la différence avec les threads.)

Il y a mieux encore ! Depuis Apache 2.4, le mode *event* est disponible. Celui-ci fonctionne exactement de la même manière que le mode *worker*, à la différence près qu'un *thread* ne va traiter qu'une requête HTTP au lieu de toute une session HTTP. Une fois la requête exécutée, le *thread* est immédiatement libéré. Moins de *threads*, moins de mémoire.

Il nous reste à répondre à la question : pourquoi PHP-FPM plutôt que mod\_php ?

En mode *prefork* PHP est chargé via le module Apache *mod\_php* (le fameux paquet `libapache2-mod-php5`), il fait ainsi partie intégrante du processus Apache, il est entièrement géré par lui et en est indissociable. Il hérite donc des problèmes du mode *prefork*.

En mode *worker* ou *event*, on a pas le choix d'utiliser PHP-FPM, car mod\_php (ou plutôt ses diverses bibliothèques) n'est pas « thread-safe ». En gros ça signifie qu'il ne sait pas gérer le multi-threading. Avec PHP-FPM, le problème ne se pose pas, vu que l'exécution des scripts PHP est sous-traitée à un processus extérieur à Apache via [FastCGI](https://fr.wikipedia.org/wiki/FastCGI).

Bien sûr, il ne s'agit pas uniquement d'une contrainte, l'exécution des scripts PHP par PHP-FPM permet plus de flexibilité que via mod\_php. Elle permet, par exemple, de répartir la charge de l'exécution des scripts sur différents serveurs, ou encore d'attribuer des ressources limitées ou différents utilisateurs à différents *pools* PHP.

### Installation

***Les instructions ci-dessous sont obsolètes, vous pouvez vous reporter à la version [mise à jour de cet article](/2016/06/24/utiliser-php-fpm-sous-apache/) pour continuer l'installation.***

Afin de pouvoir installer le module FastCGI de Apache, qui nous sera nécessaire pour faire fonctionner PHP-FPM, il nous faut d'abord activer les dépôts `contrib` et `non-free` dans le ficher `/etc/apt/sources.list` :

```
deb http://security.debian.org/ jessie/updates main contrib non-free
deb http://debian.mirrors.ovh.net/debian/ jessie-updates main contrib non-free
deb http://debian.mirrors.ovh.net/debian/ jessie main contrib non-free
```

Ensuite on met à jour la liste de paquets, et on installe Apache2 et PHP5-FPM :

```
apt update
apt install apache2-mpm-event libapache2-mod-fastcgi php5-fpm
```

On devrait dores-et-déjà pouvoir accéder à la page par défaut de Apache2, qui nous donne notamment quelques informations intéressantes sur l'architecture de sa configuration.

Pour un Apache qui était déjà installé, le mode *prefork* doit être désactivé manuellement (et éventuellement mod\_php au passage), pour ensuite activer le mode *event* :

```
a2dismod mpm_prefork php5
a2enmod mpm_event
systemctl restart apache2
```

### Configuration Apache2

#### Résoudre l'erreur de FQDN

Si on regarde les logs de Apache (`journalctl -u apache2 -e`), on a déjà une erreur :

```
apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName
```

Elle n'est pas problématique dans le sens où elle n'empêche le processus de démarrer correctement. Cependant on va tout de même tâcher de s'en débarrasser pour éviter de polluer les logs.

On créer donc un fichier `/etc/apache2/conf-available/fqdn.conf` dans lequel on va mettre :

```
ServerName localhost
```

On peut éventuellement remplacer `localhost` par le nom du serveur, `srv.example.net`.

Ensuite on active notre fichier de configuration et on recharge le service :

```
a2enconf fqdn
systemctl reload apache2
```

#### Activer PHP5-FPM

Pour le moment PHP ne fonctionne pas sur notre serveur, et pour cause, il n'a pas été activé et configuré.

On peut le vérifier en créant un fichier `/var/www/html/info.php` avec pour contenu :

```
<?php phpinfo(); ?>
```

Si on essaie d'y accéder (`http://srv.example.net/info.php`) on se retrouve avec une belle page blanche et des erreurs dans les logs (`/var/log/apache2/error.log`).

On va donc activer les modules suivants :

-   `fastcgi` : qui va nous permettre de sous-traiter l'exécution de scripts à des processus externes (PHP à PHP-FPM dans notre cas, mais ce pourrait tout aussi bien être du Python, Perl, C, etc.) ;
-   `actions` : qui va nous permettre de rediriger les requêtes PHP vers FastCGI ;
-   `alias` : qui va nous permettre de mapper nos requêtes pour FastCGI vers le processus correspondant.

```
a2enmod fastcgi actions alias
```

Ensuite on créer le fichier `/etc/apache2/conf-available/php5-fpm.conf` :

```
<IfModule mod_fastcgi.c>
    AddHandler php5-fpm .php
    Action php5-fpm /php5-fpm
    Alias /php5-fpm /usr/lib/cgi-bin/php5-fpm
    FastCgiExternalServer /usr/lib/cgi-bin/php5-fpm -socket /var/run/php5-fpm.sock -pass-header Authorization

    <Directory /usr/lib/cgi-bin>
        AllowOverride All
        Require all granted
    </Directory>
</IfModule>
```

Si on veut que PHP soit fonctionnel pour tous les sites de notre serveur, on active globalement cette configuration et on redémarre le service Apache2 :

```
a2enconf php5-fpm
systemctl restart apache2
```

Sinon, si on veut que PHP ne soit actif que pour certains sites, au lieu d'activer globalement la configuration, on peut simplement l'ajouter dans le *VirtualHost* qui le nécessite :

```
Include conf-available/php5-fpm.conf
```

De cette manière on peut créer différents *pools* de PHP-FPM qui tournent avec des utilisateurs différents, par exemple un pour chaque site. Ainsi, si il y a une faille dans le script PHP de l'un des sites, les risques seraient limités aux fichiers sur lesquels l'utilisateur spécifié dans le *pool* a les droits.

En attendant d'explorer cette possibilité, si on rafraîchit notre page `info.php` dans le navigateur on devrait pouvoir voir le contenu de celle-ci ! :-)

#### Configurer des pools dans PHP-FPM

Pour terminer on va donc créer un *pool* qui tournera avec un utilisateur spécifique. Ceci, comme on le disait, dans le but d'améliorer la sécurité de notre serveur.

Avant de créer notre utilisateur, on va modifier le fichier `/etc/skel/.profile` pour lui indiquer d'utiliser le [umask](https://fr.wikipedia.org/wiki/Umask) 027 :

```
sed -i 's/#umask 022/umask 027/' /etc/skel/.profile
```

Ça va permettre à ce que tous les fichiers et dossiers créés par nos nouveaux utilisateurs ne soient pas accessible depuis les autres utilisateurs.

On peut maintenant créer notre nouvel utilisateur :

```
adduser myuser1
```

On ajoute ensuite l'utilisateur `www-data` au groupe de notre nouvel utilisateur, sans quoi Apache ne pourra pas lire les fichiers statiques (html, images, css, js, etc.) du site de notre utilisateur :

```
adduser www-data myuser1
```

Maintenant on se connecte à la session de notre nouvel utilisateur :

```
su - myuser1
```

On créer un répertoire `www` dans lequel on placera les fichiers de son site, on peut d'ailleurs y créer le même fichier de test que précédemment :

```
mkdir www
echo '<?php phpinfo(); ?>' > www/info.php
```

On se déconnecte maintenant de notre utilisateur, en faisant *Ctrl + D* ou `exit`, pour revenir en `root`. Et on va maintenant créer notre *pool* dans le fichier `/etc/php5/fpm/pool.d/myuser1.conf` :

```
[myuser1]

user = myuser1
group = myuser1

listen = /var/run/php5-fpm_myuser1.sock

listen.owner = www-data
listen.group = www-data

pm = dynamic
pm.max_children = 5
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3

chdir = /
```

On va lui créer la configuration Apache associée, c'est à dire qui utilise son *socket*. Par exemple dans le fichier `/etc/apache2/conf-available/php5-fpm_myuser1.conf` :

```
<IfModule mod_fastcgi.c>
    AddHandler php5-fpm .php
    Action php5-fpm /php5-fpm
    Alias /php5-fpm /usr/lib/cgi-bin/php5-fpm_myuser1
    FastCgiExternalServer /usr/lib/cgi-bin/php5-fpm_myuser1 -socket /var/run/php5-fpm_myuser1.sock -pass-header Authorization

    <Directory /usr/lib/cgi-bin>
        AllowOverride All
        Require all granted
    </Directory>
</IfModule>
```

On l'ajoute dans notre *VirtualHost* via la directive *Include*, exemple :

```
<VirtualHost *:80>
    ServerName myuser1.example.net

    DocumentRoot /home/myuser1/www

    <Directory /home/myuser1/www>
        AllowOverride All
        Require all granted
    </Directory>

    Include conf-available/php5-fpm_myuser1.conf

    ErrorLog  /home/myuser1/error.log
    CustomLog /home/myuser1/access.log combined
</VirtualHost>
```

On recharge PHP-FPM et Apache, et c'est c'est terminé ! :-)

```
systemctl reload php5-fpm
systemctl reload apache2
```

### Références

- [Wikipédia - Apache](https://fr.wikipedia.org/wiki/Apache_HTTP_Server)
- [Wikipédia - Liste des modules Apache](https://en.wikipedia.org/wiki/List_of_Apache_modules)
- [Wikipédia - CGI](https://fr.wikipedia.org/wiki/Common_Gateway_Interface)
- [vps.net - Apache MPMs – Prefork, Worker, and Event](http://www.vps.net/blog/2013/04/08/apache-mpms-prefork-worker-and-event/)
