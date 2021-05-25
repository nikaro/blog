---
title: "Comment créer un rootfs CentOS depuis Fedora"
date: "2018-08-01"
---

Ma distribution du moment est Fedora pour mon ordinateur, et CentOS pour les serveurs. Et j'ai besoin de faire joujou avec des environnements virtuels pour tester des installations, notamment via Ansible. Jusque-là pour ce besoin j'ai utilisé VirtualBox ou LXC, mais je me suis mis en tête de tester systemd-nspawn. Pourquoi ? Déjà parce que ça existe, donc ça a le mérite d'être testé. Ensuite parce que VirtualBox même en utilisant Vagrant c'est vachement lourd. Et LXC, bah j'ai rien à lui reprocher, mais étant donné que systemd est déjà présent par défaut sur tous mes systèmes pourquoi y ajouter LXC qui fait plus ou moins la même chose ?

Et donc avec systemd-nspawn pour lancer des conteneurs il faut soit une image soit un rootfs.

Voilà pour le contexte. Et voilà donc comment j'ai procédé.

En premier lieu on créer un fichier de configuration de dépôt pour CentOS, par exemple dans `~/centos7.repo` :

```
[centos7-base]
name=CentOS-7-Base
baseurl=http://mirror.centos.org/centos/7/os/x86_64
gpgcheck=0
```

Ensuite on créer un dossier dans lequel dnf va installer tout ce qui est nécessaire, disons dans `~/centos` :

```
mkdir ~/centos
sudo dnf -c centos.repo --disablerepo=* --enablerepo=centos7-base --installroot=/home/nicolas/centos/ groups install 'Minimal Install'
```

Pour terminer on se « chroot » dans le dossier et on lance la commande `passwd` pour définir un mot de passe au compte root :

```
sudo systemd-nspawn -D ~/centos/
```

Après ça on peut démarrer le conteneur normalement et s'authentifier avec le mot de passe précédemment défini :

```
sudo systemd-nspawn -bD ~/centos/ --network-bridge virbr0
```

Et une fois que vous avez fait tout ça et que vous vous dites que c'est quand-même un peu galère juste pour lancer un conteneur, vous pouvez utiliser [mkosi](http://0pointer.net/blog/mkosi-a-tool-for-generating-os-images.html) qui le fait pour vous, plus simplement, probablement beaucoup plus proprement et pour d'autres systèmes d'exploitation.

```
sudo mkosi -d centos --password topsecret
sudo systemd-nspawn -bi image.raw --network-bridge virbr0
```
