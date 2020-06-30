Title: Utiliser PHP-FPM sous Apache
Date: 2016-06-24 08:55
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, floss, informatique, php, tutoriels, web
Slug: utiliser-php-fpm-sous-apache
Status: published

Comme promis dans l'article précédent « [Oublions mod\_php](https://blog.karolak.fr/2016/06/18/oublions-mod_php-par-remi-collet/) », voici la mise à jour de celui sur [Apache, son mode Event et PHP-FPM](https://blog.karolak.fr/2016/03/14/apache-mode-event-et-php-fpm/). Vous pouvez toujours vous reporter à la partie « Explications » de ce dernier si vous voulez en savoir plus sur le fonctionnement de Apache avec PHP-FPM.

Pour ce qui est de la partie pratique, en somme on remplace l'obsolète mod\_fastcgi par mod\_fcgid avec quelques bricoles dans la configuration.

Installation
------------

On installe donc Apache2 avec le module qui va bien, et PHP-FPM :

```
apt install apache2-mpm-event php5-fpm
```

*Pour PHP7 et les distributions où il est disponible il faut simplement remplacer le 5 par 7.0 dans le nom des paquets, commandes et fichiers de configuration.*

On devrait dores-et-déjà pouvoir accéder à la page par défaut de Apache2, qui nous donne notamment quelques informations intéressantes sur l'architecture de sa configuration.

Pour un Apache qui était déjà installé, le mode *prefork* doit être désactivé et mod\_php désinstallé, pour ensuite activer le mode *event* :

```
a2dismod mpm_prefork php5
a2enmod mpm_event
apt purge libapache2-mod-php5
systemctl restart apache2
```

Activer PHP5-FPM avec mod\_proxy\_fcgi
--------------------------------------

Pour le moment PHP ne fonctionne pas sur notre serveur, et pour cause, il n'a pas été activé et configuré.

On peut le vérifier en créant un fichier `/var/www/html/info.php` avec pour contenu :

```
<?php phpinfo(); ?>
```

Si on essaie d'y accéder (`http://srv.example.net/info.php`) on se retrouve avec une belle page blanche et des erreurs dans les logs (`/var/log/apache2/error.log`).

On va donc activer le module suivant :

- `proxy_fcgi` : qui va nous permettre de rediriger les requêtes PHP vers FastCGI

```
a2enmod proxy_fcgi
```

Ensuite on créer le fichier `/etc/apache2/conf-available/php5-fpm.conf` :

```
# Redirect to local php-fpm if mod_php is not available
<IfModule !mod_php5.c>
<IfModule proxy_fcgi_module>
    # Enable http authorization headers
    <IfModule setenvif_module>
    SetEnvIfNoCase ^Authorization$ "(.+)" HTTP_AUTHORIZATION=$1
    </IfModule>

    <FilesMatch ".+\.ph(p[3457]?|t|tml)$">
        SetHandler "proxy:unix:/run/php5-fpm.sock|fcgi://localhost"
    </FilesMatch>
    <FilesMatch ".+\.phps$">
        # Deny access to raw php sources by default
        # To re-enable it's recommended to enable access to the files
        # only in specific virtual host or directory
        Require all denied
    </FilesMatch>
    # Deny access to files without filename (e.g. '.php')
    <FilesMatch "^\.ph(p[3457]?|t|tml|ps)$">
        Require all denied
    </FilesMatch>
</IfModule>
</IfModule>
```

*Pour PHP7 il faut remplacer `/run/php5-fpm.sock` par `/run/php/php7.0-fpm.sock`.*

Si on veut que PHP soit fonctionnel pour tous les sites de notre serveur, on active globalement cette configuration et on redémarre le service Apache2 :

```
a2enconf php5-fpm
systemctl restart apache2
```

Sinon, si on veut que PHP ne soit actif que pour certains sites, au lieu d'activer globalement la configuration, on peut simplement l'ajouter dans le *VirtualHost* qui le nécessite :

```
Include conf-available/php5-fpm.conf
```

Avec cette méthode on peut créer différents *pools* de PHP-FPM qui tournent avec des utilisateurs différents, par exemple un pour chaque site. Ainsi, si il y a une faille dans le script PHP de l'un des sites, les risques seraient limités aux fichiers sur lesquels l'utilisateur spécifié dans le *pool* a les droits.

En attendant d'explorer cette possibilité, si on rafraîchit notre page `info.php` dans le navigateur on devrait pouvoir voir le contenu de celle-ci ! :-)

Configurer des pools dans PHP-FPM
---------------------------------

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

listen = /run/php5-fpm_myuser1.sock

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
# Redirect to local php-fpm if mod_php is not available
<IfModule !mod_php5.c>
<IfModule proxy_fcgi_module>
    # Enable http authorization headers
    <IfModule setenvif_module>
    SetEnvIfNoCase ^Authorization$ "(.+)" HTTP_AUTHORIZATION=$1
    </IfModule>

    <FilesMatch ".+\.ph(p[3457]?|t|tml)$">
        SetHandler "proxy:unix:/run/php5-fpm_myuser1.sock|fcgi://localhost"
    </FilesMatch>
    <FilesMatch ".+\.phps$">
        # Deny access to raw php sources by default
        # To re-enable it's recommended to enable access to the files
        # only in specific virtual host or directory
        Require all denied
    </FilesMatch>
    # Deny access to files without filename (e.g. '.php')
    <FilesMatch "^\.ph(p[3457]?|t|tml|ps)$">
        Require all denied
    </FilesMatch>
</IfModule>
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
