Title: Utiliser rclone comme client de synchronisation Nextcloud
Date: 2020-08-21 19:18
Author: Nicolas Karolak
Category: Articles
Tags: informatique, webdav, rclone, floss, minimalisme
Slug: utiliser-rclone-comme-client-de-synchronisation-nextcloud
Status: published

Dans une optique minimaliste j'essaie de me passer d'un maximum de logiciels ou de leur trouver des alternatives plus légères, et aujourd'hui c'est le client Nextcloud qui passe à la trape. Et son remplaçant est [rclone](https://rclone.org), un rsync pour le "cloud" qui peut parler avec S3, Swift et plein d'autres services dont WebDAV dans le cas qui m'intéresse.

Il y a quelques limitations à cette approche :

- la synchronisation n'est pas en temps réel mais périodique, toutes les heures dans mon exemple, ça pourrait probablement se faire avec un ["systemd.path unit"](https://www.freedesktop.org/software/systemd/man/systemd.path.html) mais je n'ai pas testé et ça risque de déclencher beaucoup de synchro
- ce n'est pas une vraie synchronisation, les fichiers ne sont pas supprimés localement quand ils sont supprimés côté Nextcloud, rclone n'a pas encore de [synchronisation bi-directionnelle](https://forum.rclone.org/t/semi-rclone-bisync-two-way-sync-with-rclone-copy/8995)

Dans mon cas je ne synchronise mes fichiers qu'avec un seul ordinateur, donc ces limitations ne me bloquent pas. Si c'est bloquant pour vous il y a d'autres moyens de procéder, par exemple en montant le répertoire distant et en utilisant rsync ensuite, mais on perd un peu le côté KISS.

Pour installer rclone, s'il n'est pas présent dans les dépôts de votre distribution, vous pouvez télécharger l'exécutable sur cette page : <https://rclone.org/downloads/>

Pour la configuration, vous pouvez soit utiliser la commande interactive `rclone config`, soit créer le fichier `~/.config/rclone/rclone.conf`, sur ce modèle :

```
$ cat ~/.config/rclone/rclone.conf

[remote]
type = webdav
url = https://nextcloud.example.com/remote.php/webdav/
vendor = nextcloud
user = myuser
pass = yourpassword
```

Ensuite vous pouvez lancer une simulation de synchronisation pour vous assurer que tout fonctionne :

```
$ rclone sync --update --progress --dry-run ~/Documents remote:Documents
```

Si c'est bon, on peut créer le ["systemd.timer unit"](https://www.freedesktop.org/software/systemd/man/systemd.timer.html) :

```
$ cat ~/.config/systemd/user/rclone-nc.service

[Unit]
Description=Rclone Nextcloud

[Service]
ExecStart=/usr/bin/rclone sync --update --progress /home/myuser/Documents remote:Documents
```

```
$ cat ~/.config/systemd/user/rclone-nc.timer

[Unit]
Description=Rclone Nextcloud

[Timer]
OnCalendar=hourly

[Install]
WantedBy=timers.target
```

Reste plus qu'à activer le timer et c'est terminé :

```
$ systemctl --user enable --now rclone-nc.timer
```
