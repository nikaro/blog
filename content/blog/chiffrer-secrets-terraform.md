---
title: "Chiffrer des secrets dans Terraform"
date: "2022-02-05"
draft: true
---

Pour que Terraform puisse communiquer avec les fournisseurs de services
("providers") sur lesquels il doit pouvoir créer ses ressources, il a besoin
des identifiants des plateformes en questions. Il y a plusieurs manières de
faire, la plus basique étant de les passer via des variables d'environnement.

Personnellement je trouve embêtant d'avoir une étape supplémentaire qui
consiste à sourcer un éventuel fichier `.env`. Puis si on est parano ou
imprudent on peut craindre de faire fuiter ses secrets, par exemple avec un
programme qui planterait et souhaiterait envoyer un rapport de plantage avec le
contenu des variables d'environnement.

Jusque-là j'utilisais donc le plugin
[terraform-sops](https://github.com/carlpett/terraform-provider-sops) qui
permet d'utiliser [sops](https://github.com/mozilla/sops) pour chiffrer et
déchiffrer des secrets statiques, en se reposant sur des outils tels que GPG
(beurk) et [Age](https://age-encryption.org/) (miam) entre autres. Sauf que ça
nous fait une chaine de dépendances `terraform > plugin > sops > age` que je
serais content de pouvoir raccourcir.

Ça tombe bien, Terraform fournit une fonction
[`rsadecrypt`](https://www.terraform.io/language/functions/rsadecrypt) qui
devrait pouvoir nous y aider.

On commence par générer une clé :

```
$ openssl genrsa -out ./privkey.pem 4096
```

Ensuite on créer le fichier JSON qui va contenir nos identifiants :

```
$ cat /tmp/secrets.json
{
  "scaleway": {
    "access_key": "***",
    "secret_key": "***"
  }
}
```

On le chiffre à l'aide notre clé RSA :

```
$ openssl rsautl -encrypt -inkey privkey.pem -in /tmp/secrets.json -out ./secrets.json
```

Et ensuite on peut le charger dans nos fichiers Terraform :

```
$ cat main.tf
[...]

locals {
  secrets = jsondecode(rsadecrypt(filebase64("${path.module}/secrets.json"), file("${path.module}/privkey.pem")))
}

provider "scaleway" {
  region     = "fr-par"
  zone       = "fr-par-1"
  access_key = local.secrets.scaleway.access_key
  secret_key = local.secrets.scaleway.secret_key
}

[...]
```

On se retrouve donc maintenant avec une chaine de dépendances nettement plus
courte : `terraform > openssl`. Une victoire de plus pour le minimalisme !

Bon après il se pourrait qu'utiliser RSA via OpenSSL soit moins sécurisé que
AEAD via Age, toutefois je pense que c'est suffisant pour mon
[modèle de menace](https://fr.wikipedia.org/wiki/Modèle_de_menace).

<!--
vim: spell spelllang=fr
-->
