---
title: "Faire tourner HTTPS et SSH sur le même port avec NGINX"
date: "2019-02-04"
categories: ["Articles"]
tags: ["adminsys", "floss", "informatique", "web"]
slug: "faire-tourner-https-et-ssh-sur-le-meme-port-avec-nginx"
---

Depuis la version 1.15.2, [NGINX](https://nginx.org/) a ajouté une fonctionnalité qui permet de faire une distinction entre un flux HTTPS et un autre flux TCP arrivant sur un même port. Ça permet par exemple de faire tourner en même temps sur le port 443 un service Web en HTTPS et un service VPN ou SSH. Et ainsi passer outre certains pare-feux restrictif qui ne laissent pas passer certains flux (Git, SSH, DNS personnalisé).

Pour ce faire, NGINX grâce au module [stream\_ssl\_preread](https://nginx.org/en/docs/stream/ngx_stream_ssl_preread_module.html) inspecte le `ClientHello` d'une connexion TLS et remplit certaines variables avec les éléments qu'il y trouve ou non, dont la variable `$ssl_preread_protocol` qui nous intéresse. Si il s'agit d'un flux HTTPS, la variable va prendre la valeur de la version TLS utilisée, sinon elle restera vide. En fonction de sa valeur on pourra donc rediriger le flux vers le service Web ou autre.

Comment faire ?
---------------

Pour commencer il faut avoir une version récente de NGINX (\>= 1.15.2), si les paquets de votre distribution ne respectent pas ce pré-requis vous pouvez utiliser les dépôts officiels mis à disposition : <https://nginx.org/en/linux_packages.html>

Dans un premier temps il va falloir éditer vos vhosts (probablement dans `/etc/nginx/conf.d/`ou `/etc/nginx/sites-available/`) pour y modifier le port de la directive `listen 443 ssl;` afin d'éviter d'être en conflit avec la configuration que nous allons mettre en place. Pour l'exemple on va utiliser le port `8443`.

Ensuite, vous devez éditer le fichier `/etc/nginx/nginx.conf` pour y ajouter à la fin, en dehors du bloc `http { [...] }` :

```
stream {}
```

On utilise ici un bloc [`stream`](https://nginx.org/en/docs/stream/ngx_stream_core_module.html#stream) au lieu de « l'habituel » bloc `http` car nous allons dans un premier temps travailler au niveau TCP.

On y ajoute nos [`upstream`](https://nginx.org/en/docs/stream/ngx_stream_upstream_module.html) pointant respectivement vers notre service TCP, ici SSH, et notre service HTTPS (pour lequel on a modifié le port d'écoute par `8443`) :

```
stream {
  upstream ssh {
    server 127.0.0.1:22;
  }

  upstream web {
    server 127.0.0.1:8443;
  }
}
```

On a maintenant deux « cibles » qu'on va pouvoir servir par la suite. Si à la place de SSH on voulait servir un service OpenVPN tournant sur le port 1194 en TCP, on utiliserait ceci :

```
upstream vpn {
  server 127.0.0.1:1194;
}
```

Grâce au module [`map`](https://nginx.org/en/docs/http/ngx_http_map_module.html#map) on va ensuite rediriger le traffic vers la bonne cible en fonction de la valeur de la variable `$ssl_preread_protocol` :

```
stream {
  upstream ssh {
    server 127.0.0.1:22;
  }

  upstream web {
    server 127.0.0.1:8443;
  }

  map $ssl_preread_protocol $upstream {
    default ssh;
    "TLSv1*" web;
  }
}
```

Plus précisément, on a créé une variable `$upstream` qui va avoir la valeur `web` si le contenu de la variable `$ssl_preread_protocol` correspond à `TLSv1*` (par exemple `TLSv1.2`), sinon par défaut `$upstream` prendra la valeur `ssh`.

Pour terminer il ne reste plus qu'à ajouter un bloc [`server`](https://nginx.org/en/docs/stream/ngx_stream_upstream_module.html#server) qui va, lui, écouter sur le port 443 et faire proxy vers la cible définie dans la variable `$upstream`, en prenant soin d'activer le mode `ssl_preread` :

```
stream {
  upstream ssh {
    server 127.0.0.1:22;
  }

  upstream web {
    server 127.0.0.1:8443;
  }

  map $ssl_preread_procotol $upstream {
    default ssh;
    "TLSv1*" web;
  }

  server {
    listen 443;

    proxy_pass $upstream;
    ssl_preread on;
  }
}
```

Et voilà, si on fait une requête HTTPS vers notre serveur, le `ClientHello` contiendra la version TLS de notre client et NGINX la fera « matcher » avec la cible `web`, sinon pour toute requête non-HTTPS sur le port 443 il servira la cible `ssh`.

Joyeux contournement de pare-feux et à la prochaine.

-   Source: [Running SSL and Non-SSL Protocols over the Same Port with NGINX 1.15.2](https://www.nginx.com/blog/running-non-ssl-protocols-over-ssl-port-nginx-1-15-2/)
