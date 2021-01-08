Title:
Date: 2020-06-30 00:00
Category: Articles
Tags:
Slug: post
Status: draft

## Concepts

[GlusterFS](https://www.gluster.org/") est un système de fichiers distribué, c'est à dire qu'il permet d'agréger du stockage (des "bricks") reparti sur plusieurs machines dans un "volume" qu'il expose à des clients. Plusieurs clients peuvent monter un même volume et y accéder simultanément.

\Ça permet d'avoir un stockage :

*   extensible
*   hautement disponible
*   distribué

## Volumes

GlusterFS peut créer différent [types de volumes](https://docs.gluster) :

*   [distribué](https://docs.gluster.org/en/latest/Administrator%20Guide/) : équivalent au RAID 0, les données sont réparties sur plusieurs bricks
*   [répliqué](https://docs.gluster.org/en/latest/Administrator%20Guide/) : équivalent au RAID 1, les données sont dupliquées sur plusieurs bricks (généralement 2 ou 3)
*   [distribué et répliqué](https://docs.gluster.org/en/latest/Administrator%20Guide/) : équivalent au RAID 10, une combinaison des deux types précédents
*   [dispersé](https://docs.gluster.org/en/latest/Administrator%20Guide/) : semblable au RAID 6 sur le principe, dans les faits ça utilise un [code de correction d'erreur](https://www.lemagit.fr/definit), les données sont découpées, transformées et réparties sur plusieurs bricks avec un nombre prédéfini de bricks pouvant être perdus
*   [dispersé et distribué](https://docs.gluster.org/en/latest/Administrator%20Guide/) : semblable au RAID 60, il agrège des volumes dispersés

Le type de volume qui nous intéresse est le "distribué et répliqué" (RAID 10) :

![schéma](3fe8c569a9cf0cf70c40faf3148ef=)

Le "dispersé et distribué" (~RAID 60) ferait aussi l'affaire, il a notamment l'avantage de "gâcher" moins d'espace de stockage en contrepartie d'une moindre tolérance aux pannes, mais il est légèrement plus complexe et potentiellement moins performant (je n'ai pas testé donc je ne peux garantir cette dernière affirmation).

Typiquement on commence souvent avec un volume répliqué (ou dispersé), et lorsqu'on l'étend ça devient automatiquement distribué et répliqué (ou dispersé).

## Clients

Côté client, pour accéder à un volume GlusterFS, il existe [différentes méthodes](https://docs.gluster.org/en/latest/Administrator%20Guide/) :

* [Gluster Native Client](https://docs.gluster.org/en/latest/Administrator%20Guide/) : basé sur FUSE, c'est la méthode recommandée et la plus simple
* [NFS](https://access.redhat.com/documentation/en-us/red_hat_glu) : nécessite d'installer et configurer des composants supplémentaires, et notamment de s'assurer soi-même du mécanisme de bascule en cas de problème
* [SMB/CIFS](https://docs.gluster.org/en/latest/Administrator%20Guide/) : pareil que pour le NFS
* [Object Storage](https://docs.gluster.org/en/latest/Administrator%20Guide/) : pareil que pour le NFS
* [libgfapi](https://docs.gluster.org/en/latest/Administrator%20Guide/) : expose une API pour interagir avec le stockage via du code directement

# Installation

[GlusterFS est présent dans les dépôts Debian, en version 5.5, toutefois pour avoir une version plus récente il est possible d'utiliser les](https://docs.gluster.org/en/latest/Administrator%20Guide/) [dépôts du projet](https://download.gluster.org/pub/gluster/g), la dernière version étant la 8.2 :

\20

\# ajout
 des dépôts tiers
wget -O - https://download.gluster.org/pub/gluster/glusterfs/8/rsa.pub | ap
t-key add -
echo 'deb \[arch=amd64\] https://download.gluster.org/pub/gluster/glusterfs
/8/LATEST/Debian/buster/amd64/apt buster main' > /etc/apt/sources.list.d
/gluster.list
apt-get update

# installation de GlusterFS
apt-get install glusterfs-server

# outils pour LVM
apt-get install lvm2 thin-provisionning-tools

# outils pour XFS
apt-get install xfsprogs

\20

# Configuration

## Préparation du stockage

### LVM

L'utilisation de [LVM](https://fr.wikipedia.org/wiki/Gestio) est recommandée, car ça permet de bénéficier de la fonction de [snapshots de GlusterFS, sinon c'est optionnel. Plus spécifiquement, ilfaut utiliser le "thin-provisionning" de LVM pour que ça fonctionne.](https://docs.gluster.org/en/latest/Administrator%20Guide/M)

[

\20

\# création du groupe de volumes LVM
vgcreate data-vg /dev/sdx

# création du groupement destiné à recevoir les volumes
lvcreate --type thin-pool --extents 100%FREE --name data-vg/thin-pool

# création du volume dans le pool
lvcreate --type thin --virtualsize 500G --thinpool data-vg/thin-pool --name
 thin-vol

\20

### Système de fichiers

N'importe quel système de fichiers gérant les attributs POSIX étendus est censé être supporté, XFS est celui recommandé, ext4 ou Btrfs sont également valables.

\20

\# forma
tage du volume en XFS
mkfs.xfs -i size=512 /dev/mapper/data--vg-thin--vol

# montage du volume
mkdir -p /data/brick
echo '/dev/mapper/data--vg-thin--vol /data/brick xfs rw,inode64,noatime,nou
uid 0 2' >> /etc/fstab
mount /data/brick

\20

## Création du cluster

En partant du principe qu'on a trois serveurs, respectivement nommés : gfs01, gfs02 et gfs03. On créer le "trusted pool" avec les nœuds du cluster :

\20

\# sur c
haque nœud, démarrer le service et l'activer au démarrage
systemctl start glusterd
systemctl enable glusterd

# depuis gfs01, sonder les autres nœuds pour les ajouter au pool
gluster peer probe gfs02
gluster peer probe gfs03

\20

On peut ensuite vérifier l'état du pool et la liste des nœuds :

\20

gluster
 peer status
gluster pool list

\20

## Création du volume

On créer un volume `gv1` de type "replica 3", c'est à dire que la donnée sera disponible sur trois nœuds et si l'un des nœuds devient indisponible, la donnée le sera encore sur deux autres nœuds :

\20

gluster
 volume create gv01 replica 3 gfs01:/data/brick/gv01 gfs02:/data/brick/gv01
 gfs03:/data/brick/gv01
gluster volume start gv01

\20

On peut ensuite consulter l'état du volume :

\20

gluster
 volume info

\20

La sortie devrait avoir une ligne indiquant `Status: Started`\sinon il faudra aller consulter le fichier de log, par défaut `/var/log/glusterfs/glusterd.log`, pour comprendre ce qui ne vas pas.

## Montage du volume

Depuis le ou les clients, il faut installer le paquet `glusterfs-client` dans la même version que les serveurs, et simplement monter le volume :

\20

mount -
t glusterfs -o  gfs01:/gv01 /data/gv01

\20

## Tuning

### GlusterFS

](https://docs.gluster.org/en/latest/Administrator%20Guide/M)

[](https://docs.gluster.org/en/latest/Administrator%20Guide/M)[https://www.redhat.com/en/about/videos/architecting-and-performance-tuning-efficient-gluster-storage-pools](https://www.redhat.com/en/about/videos/architecting-and-perfo)

### Noyau Linux

[https://docs.gluster.org/en/latest/Administrator Guide/Linux Kernel Tuning/](https://docs.gluster.org/en/latest/Administrator%20Guide/Linu)

## Sécurisation

*   Restreindre l'écoute à l'interface réseau privée si tous les nœuds sont sur un même LAN
    
*   Créer les règles de pare-feu suivantes :
    
    *   tcp/udp ports 24007:24008 depuis/vers tous les serveurs et clients
        
    *   tcp/udp ports 49152:(49152 + nombre de bricks) depuis/vers tous les serveurs et clients
        
*   [Activation de TLS](https://docs.gluster.org/en/latest/Administrator%20Guide/) (peu d'intérêt si ça reste sur un LAN, et probablement prévoir un impact sur les performances)
    

# Administration

## Extension du stockage

Le nombre de bricks à ajouter doit un multiple du nombre de `replica` choisit, par exemple pour un cluster en `replica 3 il faudra ajouter les nœuds par groupe de 3 (3, 6, 9, 12, ...).`

`

20

# exten
sion du volume
gluster volume add-brick gv01 gfs04:/data/brick/gv01 gfs05:/data/brick/gv01
 gfs06:/data/brick/gv01

# vérifer l'état du volume
gluster volume info gv01

# reabalancement des donnés
gluster volume rebalance gv01 start

# vérifier l'état du rebalacement
gluster volume rebalance gv01 status

20

## Remplacement d'un nœud

## Réintégration d'un nœud

## Mise à jour du cluster

S'il s'agit d'une mise à jour de version majeure, par exemple 5.x vers 8.x, il faut vérifier les éventuels changements importants et incompatibilités dans les [notes de version](https://) et le [guide de mise à jour](https://docs.gluster.org/en/).

[https://docs.gluster.org/en/latest/Upgrade-Guide/Generic_Upgrade_procedure/](https://docs.gluster.org/en/latest/Upgrade-Guide/Generic_Upgr)

Pour terminer il est recommandé mettre à jour l'[op-version](htt) du cluster.

## Supervision

[https://docs.gluster.org/en/latest/Administrator Guide/Monitoring Workload/](https://docs.gluster.org/en/latest/Administrator%20Guide/Moni)

[https://developers.redhat.com/blog/2017/11/20/monitoring-rhgs/](https://developers.redhat.com/blog/2017/11/20/monitoring-rhgs)

## Benchmark

[https://docs.gluster.org/en/latest/Administrator Guide/Performance Testing/](https://docs.gluster.org/en/latest/Administrator%20Guide/Perf)

## Sauvegarde

[https://docs.gluster.org/en/latest/Administrator Guide/Managing Snapshots/](https://docs.gluster.org/en/latest/Administrator%20Guide/Mana)

[https://docs.gluster.org/en/latest/Administrator Guide/Geo Replication/](https://docs.gluster.org/en/latest/Administrator%20Guide/Geo%)

[https://developers.redhat.com/blog/2018/08/14/improving-rsync-performance-with-glusterfs/](https://developers.redhat.com/blog/2018/08/14/improving-rsync)

# Limitations connues

* nombre d'inodes : 2^64
* taille maximale de fichier : 2^64
* taille maximale du système de fichier : 2^64 octets
* longueur maximale de chemin/nom de fichier : 4096 octets
* pas de limite de nombre de fichiers par dossier
* pas de limite de nombre de dossiers créés

Ces limitations s'appliquait à la [version courante de 2008](https://lists.), peut-être que depuis les choses ont évoluées.

# Ressources

* [https://docs.gluster.org/en/latest/](https://docs.gluster.org/en/latest/")
* [https://connect.ed-diamond.com/GNU-Linux-Magazine/GLMF-209/Un-systeme-de-fichiers-haute-disponibilite-avec-GlusterFS](https://connect.ed-diamond.com/GNU-Linux-Magazine/GLMF-20)
* [https://people.redhat.com/dblack/2013-10/gluster_for_sysadmins-advanced-with_demo.pdf](https://people.redhat.com/dblack/2013-10/gluster_for_sysa)

<!--
vim: spell spelllang=fr
-->
