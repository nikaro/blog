Title: Supprimer un conteneur OpenStack Swift et tous ses objets
Date: 2019-11-04 14:28
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, devops, informatique, openstack
Slug: supprimer-un-conteneur-openstack-swift-et-tous-ses-objets
Status: published

Une petite note qui pourrait éventuellement servir à d'autres dans le même cas. J'ai un conteneur de stockage d'objets sur le Public Cloud OVH avec plusieurs téraoctets de données que j'ai besoin de supprimer. Sauf que via l'interface je ne peux pas le faire, car il faut d'abord supprimer toutes ses données, et ça prend énormément de ressources au point de rendre mon navigateur inutilisable, en plus de prendre énormément de temps.

Du coup, comme pour tous les problèmes liés à une interface, la solution est l'utilisation de la ligne de commande. On va donc utiliser le client python [openstackclient](https://docs.openstack.org/python-openstackclient/latest/), il est installable via [pip](https://pypi.org/project/openstackclient/) ou dans les dépôts Debian sous le nom de [python3-openstackclient](https://tracker.debian.org/pkg/python-openstackclient). Et dans le l'interface de gestion des utilisateurs du projet Public Cloud OVH, on peut télécharger le fichier RC avec les informations d'authentification.

```
$ export OS_AUTH_URL=https://auth.cloud.ovh.net/v2.0/
$ export OS_IDENTITY_API_VERSION=2
$ export OS_TENANT_ID=******
$ export OS_TENANT_NAME="******"
$ export OS_USERNAME="******"
$ export OS_PASSWORD="******"
$ export OS_REGION_NAME="GRA1"
$ openstack container delete monconteneur
Conflict (HTTP 409) (Request-ID: txc504d5d75e734666bfd6d-**********)
```

Naïvement je me suis dit qu'en ligne de commande on pourrait simplement supprimer le conteneur entier, sauf que non, on se mange une erreur 409 qui à priori signifie qu'on ne peut pas supprimer un conteneur qui n'est pas vide.

```
$ openstack object list monconteneur --format value --all | xargs openstack object delete monconteneur
$ openstack container delete monconteneur
```

Voilà qui devrait résoudre le problème. Avec cette commande on liste tous les objets au format brut, afin de pouvoir les passer en argument, via `xargs`, à la commande qui supprime les objets individuellement. Ça prend toujours énormément de temps, mais quasiment aucune ressource. Il n'y a plus qu'à laisser tourner dans un tmux en arrière plan.

**Mise à jour 05/11/2019 :** Il s'avère que même avec l'argument `--all` la commande ne peut en lister que 10 000 objets au maximum. J'ai donc terminé avec le script suivant :

```
#!/usr/bin/bash

export OS_AUTH_URL="https://auth.cloud.ovh.net/v2.0/"
export OS_IDENTITY_API_VERSION="2"
export OS_TENANT_ID="******"
export OS_TENANT_NAME="******"
export OS_USERNAME="******"
export OS_PASSWORD="******"
export OS_REGION_NAME="GRA1"

CT_NAME="backup"

openstack object list $CT_NAME --format value --all > /tmp/objects.txt
while [[ $(wc -l /tmp/objects.txt) > 0 ]]; do
    for object in $(cat /tmp/objects.txt); do
        echo deleting: $object
        openstack object delete $CT_NAME $object
    done
    openstack object list $CT_NAME --format value --all > /tmp/objects.txt
done

rm -rf /tmp/objects.txt

openstack container delete $CT_NAME
```

**Mise à jour 07/11/2019 :** Bon ça prend encore trop de temps via le script, à priori avec cette méthode pour supprimer 2 000 000 d'objets ça prendrait environ 1 mois. En cherchant un peu j'ai trouvé le paquet client [swift](https://pypi.org/project/swift/) ([python3-swiftclient](https://tracker.debian.org/pkg/python-swiftclient) pour le paquet Debian) qui permet vraisemblablement d'aller plus vite :

```
$ export OS_AUTH_URL=https://auth.cloud.ovh.net/v2.0/
$ export OS_IDENTITY_API_VERSION=2
$ export OS_TENANT_ID=******
$ export OS_TENANT_NAME="******"
$ export OS_USERNAME="******"
$ export OS_PASSWORD="******"
$ export OS_REGION_NAME="GRA1"
$ swift delete monconteneur
```
