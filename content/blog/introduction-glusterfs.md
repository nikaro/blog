---
title: "Introduction à GlusterFS"
date: "2021-05-13"
categories: ["Articles"]
tags: ["adminsys", "floss", "glusterfs", "informatique"]
slug: "introduction-glusterfs"
---

## Concepts

GlusterFS est un système de fichiers distribué, c'est à dire qu'il permet
d'agréger du stockage (des "bricks") reparti sur une grappe de machines dans un
"volume" qu'il expose à des clients. Plusieurs clients peuvent monter un même
volume et y accéder simultanément.

Ça permet d'avoir un stockage :

* extensible
* hautement disponible
* distribué

=> <https://www.gluster.org/>

### Volumes

GlusterFS peut créer différent types de volumes :

* **distribué :** équivalent au RAID 0, les données sont réparties sur plusieurs
  bricks pour fournir de l'extensibilité
* **répliqué :** équivalent au RAID 1, les données sont dupliquées sur plusieurs
  bricks (généralement 2 ou 3) pour garantir de la disponibilité
* **distribué et répliqué :** équivalent au RAID 10, une combinaison des deux types
  précédents
* **dispersé :** semblable au RAID 6 sur le principe, dans les faits ça utilise un
  code de correction d'erreur ("ECC"), les données sont découpées, transformées
  et réparties sur plusieurs bricks avec un nombre prédéfini de bricks pouvant
  être perdus
* **distribué et dispersé :** semblable au RAID 60, il agrège des volumes dispersés

Par rapport au "distribué et répliqué", le "dispersé et distribué" (~RAID 60) a 
l'avantage de "gâcher" moins d'espace de stockage en contrepartie d'une moindre
tolérance aux pannes.

Typiquement on commence souvent avec un volume répliqué ou dispersé, et
lorsqu'on l'étend ça devient automatiquement distribué et répliqué/dispersé.

=> <https://docs.gluster.org/en/latest/Administrator-Guide/Setting-Up-Volumes/>

### Clients

Pour accéder à un volume GlusterFS, il existe différentes méthodes :

* **Gluster Native Client :** basé sur FUSE, c'est la méthode recommandée et la
  plus simple
* **NFS :** nécessite d'installer et configurer des composants supplémentaires, et
  notamment de s'assurer soi-même la haute-disponibilité du NFS
* **SMB/CIFS :** pareil que pour le NFS
* **Object Storage :** pareil que pour le NFS
* **libgfapi :** expose une API pour interagir avec le stockage via du code
  directement

=> <https://docs.gluster.org/en/latest/Administrator-Guide/Setting-Up-Clients/>

## Installation

GlusterFS est présent dans les dépôts Debian, toutefois pour avoir une version
plus récente il est possible d'utiliser les dépôts du projet :

```
# ajout des dépôts tiers
wget -O - https://download.gluster.org/pub/gluster/glusterfs/8/rsa.pub | apt-key add -
echo deb [arch=amd64] https://download.gluster.org/pub/gluster/glusterfs/9/LATEST/Debian/buster/amd64/apt buster main > /etc/apt/sources.list.d/gluster.list

# installation de GlusterFS
apt-get install glusterfs-server

# outils pour LVM
apt-get install lvm2 thin-provisionning-tools

# outils pour XFS
apt-get install xfsprogs
```

=> <https://download.gluster.org/pub/gluster/glusterfs/LATEST/>

## Configuration

### Préparation du stockage

#### LVM

L'utilisation de LVM est recommandée, car ça permet de bénéficier de la
fonction de snapshots de GlusterFS, sinon c'est optionnel. Plus spécifiquement,
il faut utiliser le "thin-provisionning" de LVM pour que ça fonctionne.

```
# création du groupe de volumes LVM
vgcreate data-vg /dev/sdx

# création du groupement destiné à recevoir les volumes
lvcreate --type thin-pool --extents 100%FREE --name data-vg/thin-pool

# création du volume dans le groupement
lvcreate --type thin --virtualsize 500G --thinpool data-vg/thin-pool --name thin-vol
```

#### Système de fichiers

N'importe quel système de fichiers gérant les attributs POSIX étendus est censé
être supporté, XFS est celui recommandé, ext4 ou Btrfs sont également valables.

```
# formatage du volume en XFS
mkfs.xfs -i size=512 /dev/mapper/data--vg-thin--vol

# montage du volume
mkdir -p /data/brick
echo '/dev/mapper/data--vg-thin--vol /data/brick xfs rw,inode64,noatime,nouuid 0 2' >> /etc/fstab
mount /data/brick
```

### Création de la grappe

En partant du principe qu'on a trois serveurs, respectivement nommés : gfs01,
gfs02 et gfs03. On créer le "trusted pool" avec ceux-ci :

```
# sur chaque membre, démarrer le service et l'activer au démarrage
systemctl enable --now glusterd

# depuis gfs01, sonder les autres membres pour les ajouter au groupement
gluster peer probe gfs02
gluster peer probe gfs03
```

On peut ensuite vérifier l'état du groupement et la liste de ses membres :

```
gluster peer status
gluster pool list
```

### Création du volume

C'est à cette étape qu'on choisit si on veut faire du distribué, répliqué ou
dispersé. On va commencer avec de la réplication.

On créer un volume `gv01` de type "replica 3", c'est à dire que la donnée sera
copiée à trois endroits, et si une machine devient indisponible, la donnée sera
encore sur les deux autres :

```
gluster volume create gv01 replica 3 gfs01:/data/brick/gv01 gfs02:/data/brick/gv01 gfs03:/data/brick/gv01
gluster volume start gv01
```

On peut ensuite consulter l'état du volume :

```
gluster volume info
```

La sortie devrait avoir une ligne indiquant `Status: Started`. Sinon pour
comprendre ce qui ne vas pas il faudra aller consulter le journal d'événements,
par défaut `/var/log/glusterfs/glusterd.log`.

### Montage du volume

Depuis les clients, il faut installer le paquet `glusterfs-client` dans la même
version que les serveurs, et simplement monter le volume :

```
mkdir -p /data/gv01
mount -t glusterfs -o defaults,noatime,_netdev gfs01:/gv01 /data/gv01
```

Le montage se fait via `gfs01`, mais une fois monté même si cette machine
disparaît ça continuera de fonctionner. Par contre si `gfs01` est indisponible
au moment du montage, ça échouera. Si on veut avoir une sécurité au montage on
peut ajouter l'option `backupvolfile-server=gfs02` par exemple.

Pour un montage persistent, ajouter cette ligne dans le fichier `/etc/fstab` :

```
gfs01:/gv01 /data/gv01 glusterfs defaults,noatime,_netdev 0 0
```

### Extension du stockage

Le nombre de bricks à ajouter doit un multiple du nombre de "replica" choisit,
par exemple pour une grappe en "replica 3" il faudra ajouter les membres par
groupe de 3 (exemples : 3, 6, 9, 12, ...).

```
# extension du volume
gluster volume add-brick gv01 gfs04:/data/brick/gv01 gfs05:/data/brick/gv01 gfs06:/data/brick/gv01

# vérifer l'état du volume
gluster volume info gv01

# reabalancement des donnés
gluster volume rebalance gv01 start

# vérifier l'état du rebalacement
gluster volume rebalance gv01 status
```

## Ressources

* <https://docs.gluster.org/en/latest/>
* <https://connect.ed-diamond.com/GNU-Linux-Magazine/GLMF-209/Un-systeme-de-fichiers-haute-disponibilite-avec-GlusterFS>
* <https://people.redhat.com/dblack/2013-10/gluster_for_sysadmins-advanced-with_demo.pdf>
* <https://www.redhat.com/en/about/videos/architecting-and-performance-tuning-efficient-gluster-storage-pools>
* <https://developers.redhat.com/blog/2017/11/20/monitoring-rhgs/>
* <https://developers.redhat.com/blog/2018/08/14/improving-rsync-performance-with-glusterfs/>

<!--
vim: spell spelllang=fr
-->
