Title: Une autre manière de suivre des flux RSS : les mails
Date: 2020-06-20 08:20
Author: Nicolas Karolak
Category: Articles
Tags: informatique, rss, email
Slug: une-autre-maniere-de-suivre-des-flux-rss-les-mails
Status: published

Je pars du principe que savez déjà ce que sont les flux [RSS](https://fr.wikipedia.org/wiki/RSS) et si vous avez cliqué sur cet article c'est même que vous avez probablement déjà un agrégateur de flux RSS, il se pourrait même que vous le lisiez au travers de celui-ci. Du coup je vais vous présenter une manière alternative de suivre des flux, que j'ai découvert au détour d'une [discussion sur Lobsters](https://lobste.rs/s/hwhptd/which_atom_rss_reader_do_you_use#c_kyyur4) : les mails.

Avantages
---------

Les avantages sont que quel que soit le terminal ou la plateforme sur laquelle vous êtes, vous avez à coup sûr un client mail disponible et probablement même déjà installé. Le cas échéant vous avez donc d'office les fonctions suivantes :

-   recherche
-   archivage
-   favoris
-   synchronisation entre appareils
-   notification
-   consultation hors-ligne

Tout ça sans installer un logiciel supplémentaire.

Comment
-------

Il existe plusieurs solutions. La première utilise le client RSS pour terminal [Newsboat](https://newsboat.org/), qui peut aussi bien fonctionner seul que s'appuyer sur un service que vous utilisez peut-être déjà (The Old Reader, NewsBlur, FeedHQ, Bazqux, TinyTinyRSS, Nextcloud News, Inoreader, ou un simple fichier OPML servi via HTTP). Personnellement c'est le client que j'utilisais pour consulter mes flux, synchronisé avec Nextcloud. En le faisant tourner sur un serveur et en lui adossant [newsboat-sendmail](https://github.com/lenormf/newsboat-sendmail) on reçoit ainsi les nouveaux articles par mail, et on peut gérer les flux soit depuis le client lui-même, soit depuis le service avec lequel il est éventuellement synchronisé.

Je n'ai pas utilisé cette première solution car je la trouve quand-même un peu overkill, malgré qu'elle présente l'avantage de pouvoir gérer les flux via le service ou le client. Du coup je ne vais pas vous expliquer comment installer et configurer.

J'en viens donc à la deuxième solution, plus simple et tout aussi efficace : [rss2email](https://github.com/rss2email/rss2email) (j'y ai même fait un [petit correctif](https://github.com/rss2email/rss2email/pull/114) récemment ^\_^).

Ça s'installe soit via le gestionnaire de paquets de votre distribution, par exemple Debian :

```
# apt-get install rss2email
```

Soit via pip (idéalement dans un "virtualenv") pour avoir une version plus récente :

```
# python3 -m venv /usr/local/venv/rss2email
# /usr/local/venv/rss2email/bin/pip install rss2email
```

Ensuite on configure le compte (si vous avez installé sans virtualenv ce n'est pas la peine de mettre le chemin complet vers le binaire `r2e`) :

```
# /usr/local/venv/rss2email/bin/r2e new adresse.email@exemple.net
```

Ce qui aura pour effet de créer le fichier de configuration dans le `XDG_CONFIG_HOME` de l'utilisateur courant, dans lequel vous pourrez configurer la méthode pour envoyer les mails. Par défaut ça utilisera sendmail, donc si votre machine est déjà configurée pour pouvoir envoyer des mails (et si c'est un serveur ça devrait être le cas) il n'y a rien à faire. Sinon vous pouvez configurer l'envoi via SMTP comme ceci :

```
# cat ~/.config/rss2email.cfg
[DEFAULT]
...
email-protocol = smtp
smtp-server = smtp.exemple.net:587
smtp-auth = True
smtp-username = username
smtp-password = password
...
```

On peut maintenant ajouter des flux :

```
# /usr/local/venv/rss2email/bin/r2e add exemple https://exemple.net/feed.xml
```

Reste plus qu'à faire tourner la machine :

```
# /usr/local/venv/rss2email/bin/r2e run
```

Et pour finaliser le tout on créer un timer systemd qui va lancer cette commande périodiquement.

```
# cat /etc/systemd/system/rss2email.service
[Unit]
Description=rss2email job

[Service]
ExecStart=/usr/local/venv/rss2email/bin/r2e run
```

```
# cat /etc/systemd/system/rss2email.timer
[Unit]
Description=rss2email timer

[Timer]
OnCalendar=hourly

[Install]
WantedBy=timers.target
```

On active le timer :

```
# systemctl enable --now rss2email.timer
```

Et il n'y a plus qu'à attendre que les articles arrivent tout seuls dans la boite de réception.
