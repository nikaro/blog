Title: Kresus, un gestionnaire Web de finances personnelles
Date: 2016-03-18 07:59
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, auto-hébergement, floss, informatique, tutoriels, web
Slug: kresus-un-gestionnaire-web-de-finances-personnelles
Status: published
Attachments: wp-content/uploads/2019/09/kresus.png

Vous connaissez peut-être déjà [Cozy](https://cozy.io/fr/), si ce n'est pas le cas, il s'agit une application Web de cloud personnel. Et parmi les applications qu'elle propose, il y a [Kresus](https://framagit.org/bnjbvr/kresus.git) qui permet de centraliser ses relevés bancaires, etc. J'aime beaucoup le principe de cette application, car ça me permet d'éviter d'aller me connecter sur le site de ma banque à chaque fois, puis ça me permet de centraliser les informations de mes différents comptes à un seul endroit.

Sauf que j'ai déjà un [NextCloud](https://nextcloud.org/) et que je ne peux pas le remplacer par Cozy, parce que déjà j'en suis très content, et ensuite je n'en suis pas le seul utilisateur. Cozy étant mono-utilisateur, ça ne fera pas l'affaire…

Eh bien bonne nouvelle, Kresus peut fonctionner en mode standalone, sans Cozy ! Voici donc comment faire.

### Pré-requis

On va avoir besoin de NodeJS, pour ma part j'utilise les dépôts de [NodeSource](https://github.com/nodesource/distributions) pour avoir une version à jour sur ma Debian :

```
curl -sL https://deb.nodesource.com/setup_4.x | bash -
apt install nodejs
```

On installe quelques outils nécessaire à l'installation de Kresus :

```
apt install git python-weboob-core python-imaging
```

### Installation Kresus

Pour l'installation de Kresus, on va lui créer un utilisateur dédié, on va cloner le dépôt Git dans son répertoire `~/app` et après s'être placé dans celui-ci on va lancer l'installation des dépendances :

```
adduser kresus --disabled-password --gecos Kresus
su - kresus
mkdir ~/app ~/logs
git clone https://framagit.org/bnjbvr/kresus.git ~/app
cd ~/app
npm install
./scripts/build.sh
```

On teste le lancement de Kresus.

```
node ~/app/bin/kresus.js
```

Si tout va bien, l'installation a du se finaliser et les messages de la console devraient se terminer par :

```
[2016-03-18 19:49:21:873] info - init | Server is ready, let's start the show!
```

### Lancement au démarrage

On va donc créer un service systemd à notre instance de Kresus, afin que celle-ci puisse se lancer tout seul au démarrage du serveur. Pour ceci on créer un fichier `/etc/systemd/system/kresus.service` :

```
[Unit]
Description=Personal finance manager
After=network.target

[Service]
WorkingDirectory=/home/kresus/app
Environment=NODE_ENV=production
ExecStart=/usr/bin/node bin/kresus.js

Type=simple
Restart=always

User=kresus

StandardOutput=journal
StandardError=inherit
SyslogIdentifier=kresus

[Install]
WantedBy=multi-user.target
```

On active notre nouveau service, on le lance, et on vérifie son état pour être sûr que tout va bien :

```
systemctl enable kresus
systemctl start kresus
systemctl status kresus
```

### Configuration de Apache

Je pars du principe que vous avez déjà un Apache fonctionnel, avec du HTTPS, où il n'y aurait plus qu'à activer le module de proxy.

```
a2enmod proxy_http
```

À noter qu'il nous faut également ajouter une couche d'authentification, car initialement Kresus repose sur le mécanisme de connexion de Cozy. Je ne sais pas vous, mais moi ça m'enchante pas spécialement de laisser mes relevés bancaires à la vue de tous.

On créer donc un fichier `.htpasswd` avec, par exemple, l'utilisateur `myusername`.

```
htpasswd -c /home/kresus/.htpasswd myusername
```

Ensuite on créer le `VirtualHost` pour notre Kresus, dans le fichier `/etc/apache2/sites-available/kresus.conf` par exemple. Voici à quoi ressemble le mien, utilisant Let's Encrypt comme autorité de certification :

```
<VirtualHost *:80>
    ServerName  kresus.example.net
    ServerAdmin me@example.net

    Alias /.well-known/acme-challenge /tmp/.well-known/acme-challenge

    <Directory /tmp/.well-known/acme-challenge>
        Options None
        AllowOverride None

        Require all granted
        AddDefaultCharset off

        AuthType None
        Satisfy any
    </Directory>

    Redirect permanent / https://kresus.example.net/

    ErrorLog  /home/kresus/logs/error.log
    CustomLog /home/kresus/logs/access.log combined
</VirtualHost>

<IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerName  kresus.example.net
        ServerAdmin me@example.net

        ProxyPass        "/" "http://127.0.0.1:9876/"
        ProxyPassReverse "/" "http://127.0.0.1:9876/"

        Alias /.well-known/acme-challenge /tmp/.well-known/acme-challenge

        <Directory /tmp/.well-known/acme-challenge>
            Options None
            AllowOverride None

            Require all granted
            AddDefaultCharset off

            AuthType None
            Satisfy any
        </Directory>

        <Location />
            AuthUserFile  /home/kresus/.htpasswd
            AuthName      "Authentification"
            AuthType      Basic
            Require       valid-user
        </Location>

        SSLEngine on

        SSLCertificateKeyFile /etc/letsencrypt/live/kresus.example.net/privkey.pem
        SSLCertificateFile    /etc/letsencrypt/live/kresus.example.net/fullchain.pem

        Header always set Strict-Transport-Security "max-age=15768000"

        <FilesMatch "\.(cgi|shtml|phtml|php)$">
            SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
            SSLOptions +StdEnvVars
        </Directory>

        ErrorLog  /home/kresus/logs/error.log
        CustomLog /home/kresus/logs/access.log combined
    </VirtualHost>
</IfModule>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

Et pour terminer il n'y a plus qu'à activer notre site et relancer Apache :

```
a2ensite kresus
systemctl restart apache2
```
