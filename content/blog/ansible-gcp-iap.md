---
title: "Utiliser Ansible sur des machines derrière l'IAP de Google Cloud"
date: 2023-12-29T12:56:52+01:00
---

L'IAP, pour [Identity-Aware Proxy](https://cloud.google.com/security/products/iap), est un outil de Google Cloud qui fonctionne comme un proxy en amont d'une application ou d'une VM en y ajoutant un couche d'authentification via le SSO de Google. Par exemple, ça peut servir à protéger le backend d'une application web. Ou dans le cas qui nous intéresse ici, d'éviter d'exposer publiquement une instance de VM et y ajouter une couche d'authentification forte. Vachement pratique pour faire un bastion dans un environement GCP.

> ℹ️ En plus de ça il y a la fonctionnalité [OS Login](https://cloud.google.com/compute/docs/oslogin) qui permet s'affranchir de la gestion des utilisateurs sur la machine en utilisant là encore les comptes Google, et en gérant leur permissions via l'IAM. Couplé à [snoopy](https://packages.debian.org/fr/sid/snoopy) (et/ou [auditd](https://packages.debian.org/fr/sid/auditd)) qui permet des logguer les actions des utilisateurs et [Ops Agent](https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent) qui permet de remonter les logs dans le dashboard GCP, on a une machine relativement bien sécurisée de manière assez aisée. Chapeau bas à Google sur ce coup, en espérant que ça ne rejoigne pas le [cimetière de leur produits](https://killedbygoogle.com) trop rapidement...

Dès lors, puisque la machine n'a pas d'IP publique, pour pouvoir la joindre derrière l'IAP il faut utiliser la commande :

```shell
gcloud compute ssh mon-instance --tunnel-through-iap
```

Mais ça devient problématique si on veut gérer cette machine via Ansible. La solution est alors de bidouiller les options de connexion d'Ansible pour lui passer un script qui sera un wrapper autour de cette commande. Il existe déjà des [articles qui expliquent comment faire](https://blg.robot-house.us/posts/ansible-and-iap/), mais leur inconvénient est qu'ils partent du principe toutes les machines sont gérées de cette manière, ce qui n'était pas mon cas (certaines étant derrière l'IAP et d'autres non), leur solution consitant à modifier la configuration globale d'Ansible ne fonctionnait donc pas pour moi.

**TLDR**: Plutôt que de modifier les options de connexion dans le fichier `ansible.cfg`, le faire dans les host_vars/group_vars des machines concernées.

### Inventaire dynamique

Pour faire les choses bien, il convient d'utiliser le [plugin d'inventaire dynamique pour GCP](https://docs.ansible.com/ansible/latest/collections/google/cloud/gcp_compute_inventory.html), ça nous permettra de récupérer la liste de nos machines sans avoir à les ajouter manuellement dans notre inventaire.

Première étape, activer le plugin en l'ajoutant aux plugins par défaut dans le fichier de configuration `./ansible.cfg`, via la clé `inventory.enable_plugins` :

```ini
[defaults]

# (pathlist) Comma separated list of Ansible inventory sources
inventory = ./inventory,/etc/ansible/hosts

[inventory]

# (list) List of enabled inventory plugins, it also determines the order in which they are used.
enable_plugins = google.cloud.gcp_compute, host_list, script, auto, yaml, ini, toml
```

Comme vous pouvez le voir dans le fichier de configuration ci-dessus, j'utilise comme source d'inventaire le dossier `./inventory`, ça permet d'y avoir plusieurs sources d'inventaire, dans mon cas un statique `./inventory/hosts.yml` et un dynamique pour GCP `./inventory/hosts.gcp.yml`. Pour l'inventaire dynamique de GCP il faut bien veiller à nommer le fichier de manière à ce qu'il termine par `gcp.(yml|yaml)`.

Voici donc le contenu de mon fichier `./inventory/hosts.gcp.yml` :

```yaml
---
plugin: google.cloud.gcp_compute
projects:
  - nikaro-dev
  - nikaro-prod
auth_kind: application
groups:
  bastion_servers: "'bastion' in labels.ansible_hostname"
  dev: "'-dev' in labels.ansible_hostname"
  prod: "'-prod' in labels.ansible_hostname"
keyed_groups:
  - key: labels['ansible_group']
filters:
  - labels.ansible = true
hostnames:
  - labels.ansible_hostname
compose:
  ansible_host: name
```

En bref, je l'ai configuré pour que uniquement les machines qui portent le label `ansible = true` soient listés. Car je ne veux pas récupérer les nœuds des clusters Kubernetes, par exemple. Et j'ai aussi fais en sorte que le hostname des machines soit défini par le label `ansible_hostname` que j'aurais configuré, et si `bastion` est présent dans le hostname j'ajoute cette machine au groupe `bastion_servers`. Je ne rentre pas davantage dans les détails, je vous laisse consulter la documentation du plugin pour en savoir plus.

### Wrapper scripts

Maintenant il faut créer nos scripts qui encapsuleront l'appel à la commande `gcloud compute ssh`. Je les ai placé arbitrairement dans un dossier `./scripts`. Copier/coller de ce j'ai trouvé dans les article qui m'ont aidés.

* `./scripts/gcp-scp-wrapper.sh` :

```shell
#!/bin/bash
# This is a wrapper script allowing to use GCP's IAP option to connect
# to our servers.

# Ansible passes a large number of SSH parameters along with the hostname as the
# second to last argument and the command as the last. We will pop the last two
# arguments off of the list and then pass all of the other SSH flags through
# without modification:
host="${*: -2: 1}"
cmd="${*: -1: 1}"

# Unfortunately ansible has hardcoded scp options, so we need to filter these out
# It's an ugly hack, but for now we'll only accept the options starting with '--'
declare -a opts
for scp_arg in "${@: 1: $# -2}" ; do
        if [[ "${scp_arg}" == --* ]] ; then
                opts+=("${scp_arg}")
        fi
done

# Remove [] around our host, as gcloud scp doesn't understand this syntax
cmd=$(echo "${cmd}" | tr -d "[]")

#echo "gcloud --project ${project} compute scp $opts ${src} ${host}:${dest}"
exec gcloud compute scp "${opts[@]}" "${host}" "${cmd}"
```
* `./scripts/gcp-ssh-wrapper.sh` :

```shell
#!/bin/bash
# This is a wrapper script allowing to use GCP's IAP SSH option to connect
# to our servers.

# Ansible passes a large number of SSH parameters along with the hostname as the
# second to last argument and the command as the last. We will pop the last two
# arguments off of the list and then pass all of the other SSH flags through
# without modification:
host="${*: -2: 1}"
cmd="${*: -1: 1}"

# Unfortunately ansible has hardcoded ssh options, so we need to filter these out
# It's an ugly hack, but for now we'll only accept the options starting with '--'
declare -a opts
for ssh_arg in "${@: 1: $# -2}" ; do
        if [[ "${ssh_arg}" == --* ]] ; then
                opts+=("${ssh_arg}")
        fi
done

exec gcloud compute ssh "${opts[@]}" "${host}" --command "${cmd}"
```

Il faut penser à leur ajouter le bit d'exécution :

```shell
chmod +x ./scripts/gcp-*-wrapper.sh
```

### Options de connexion

Ensuite c'est essentiellement là où ça diffère d'avec les méthodes trouvées sur internet. On va modifier les options de connexions des machines concernées via les variables d'inventaire, plutôt que via la la configuration globale dans `./ansible.cfg` qui s'appliquerait alors à toutes les machines. On créer alors le fichier `./inventory/group_vars/bastion_servers/ansible.yml` :

```yaml
---
# set python interpreter as the discovery does not seem to work
ansible_python_interpreter: /usr/bin/python3

# force scp usage for file transfer as the sftp method will not work
ansible_scp_if_ssh: true

ansible_ssh_executable: scripts/gcp-ssh-wrapper.sh
ansible_ssh_args: --tunnel-through-iap --zone={{ zone }} --project={{ project}} --no-user-output-enabled

ansible_scp_executable: scripts/gcp-scp-wrapper.sh
ansible_scp_extra_args: --tunnel-through-iap --zone={{ zone }} --project={{ project }} --quiet
```
