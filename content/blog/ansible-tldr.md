---
title: "Ansible TLDR"
date: "2020-09-23"
---

Besoin d'une introduction à [Ansible](https://docs.ansible.com/ansible/latest/) et la flemme de lire la documentation ? Bienvenue.

## Principes

Ansible est un outil de [gestion de configuration](https://fr.wikipedia.org/wiki/Gestion_de_configuration). À partir d'une machine, dite "contrôleur", on exécute des tâches sur des machines distantes via SSH. Les machines distantes n'ont donc besoin que d'avoir Python installé et d'être accessible en SSH.

## Intérêts

Utiliser Ansible pour déployer et configurer un service permet d'avoir une installation/configuration de facto documentée, automatisée et reproductible. Ce qui peut s'avérer utile dans une multitude de cas, par exemple : passage de l'environnement de test, à la preprod et à la prod, déployer plusieurs instances d'un même service, avoir un plan de reprise d'activité, etc.

## Installation

La meilleure manière, selon moi, est d'installer Ansible dans un [environnement virtuel](https://docs.python.org/fr/3/library/venv.html) avec [pip](https://pip.pypa.io/en/stable/) :

```
$ python3 -m venv ~/.local/share/pyvenv/ansible-test
$ source ~/.local/share/pyvenv/ansible-test/bin/activate
$ pip install ansible
```

Pour les autres méthodes d'installation c'est par-là : <https://docs.ansible.com/ansible/latest/installation_guide/index.html>

## Inventaire

Pour que Ansible sache à qui parler il a besoin d'un inventaire, le plus simple étant d'utiliser le format [INI](https://fr.wikipedia.org/wiki/Fichier_INI) :

```
$ cat inventory/hosts
serveur-bdd-01 ansible_host=192.0.2.1 ansible_port=2222 ansible_user=root
serveur-app-01 ansible_host=192.0.2.2 ansible_user=admin ansible_become=true
serveur-app-02 ansible_host=192.0.2.3 ansible_user=admin ansible_become=true
serveur-front-01 ansible_host=192.0.2.3 ansible_user=admin ansible_become=true

[groupe_bdd]
serveur-bdd-01

[groupe_app]
serveur-app-01
serveur-app-02

[groupe_front]
serveur-front-01
```

Les premières lignes correspondent à la liste des hôtes avec leurs informations de connexion. Détails :

- `serveur-bdd-01` : un nom arbitraire
- `ansible_host=` : l'hôte SSH distant sous forme d'un [FQDN](https://fr.wikipedia.org/wiki/Fully_qualified_domain_name), une adresse IP ou une entrée `Host` de [ssh_config](https://linux.die.net/man/5/ssh_config)
- `ansible_port=` : le port de connexion distante SSH
- `ansible_user=` : l'utilisateur distant utilisé pour la connexion SSH
- `ansible_become=true` : un paramètre qui permet de dire à Ansible d'acquérir les permissions root (via sudo par défaut, donc il faut que l'utilisateur soit sudoer, avec l'option NOPASSWD idéalement)

Les lignes suivantes sont les groupes et leurs membres.

On peut tester que tous les membres de l'inventaire sont joignable en utilisant le module `ping` sur le groupe `all`, avec la commande suivante :

```
$ ansible --inventory inventory/hosts --module-name ping all
serveur-app-02 | SUCCESS => {
    "changed": false,
        "ping": "pong"
        
}
serveur-app-01 | SUCCESS => {
    "changed": false,
        "ping": "pong"
        
}
serveur-bdd-01 | SUCCESS => {
    "changed": false,
        "ping": "pong"
        
}
serveur-front-01 | SUCCESS => {
    "changed": false,
        "ping": "pong"
        
}
```

Plus de détails sur l'inventaire : <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html>

Plus spécifiquement sur les options de connexion : <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters>

## Playbook

Pour faire des choses sympa avec Ansible, on utilise la commande `ansible-playbook` qui permet de lancer des playbooks. Un playbook c'est un fichier [YAML](https://fr.wikipedia.org/wiki/YAML) avec une suite de tâches à exécuter.

```
$ cat playbooks/ansible-tldr-debug.yml
---

- name: ANSIBLE TLDR
  hosts: all
  tasks:
    - name: print hello world
      debug:
        msg: hello world
```

```
$ ansible-playbook --inventory inventory/hosts playbooks/ansible-tldr-debug.yml

PLAY [ANSIBLE TLDR] **************************************************************************************

TASK [Gathering Facts] ***********************************************************************************
ok: [serveur-app-01]
ok: [serveur-front-01]
ok: [serveur-bdd-01]
ok: [serveur-app-02]

TASK [print hello world] *********************************************************************************
ok: [serveur-bdd-01] => {}

MSG:

hello world
ok: [serveur-app-01] => {}

MSG:

hello world
ok: [serveur-app-02] => {}

MSG:

hello world
ok: [serveur-front-01] => {}

MSG:

hello world

PLAY RECAP ***********************************************************************************************
serveur-app-01             : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
serveur-app-02             : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
serveur-bdd-01             : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
serveur-front-01           : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Pour faire simple, on a exécuté le [module `debug`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html), qui ne fait qu'afficher un message ou une variable, depuis tous les `hosts` membres du groupe `all`. Le groupe `all`, comme son nom l'indique contient tous les hôtes de l'inventaire.

Un autre exemple, un peu plus utile :

```
$ cat playbooks/ansible-tldr-apt.yml
---

- name: ANSIBLE TLDR
  hosts: groupe_app
  tasks:
    - name: dist upgrade
      apt:
        cache_valid_time: 3600
        upgrade: dist
    - name: remove noob text editor
      apt:
        name: nano
        state: absent
    - name: ensure best text editor in the world is installed
      apt:
        name: vim
```

```
$ ansible-playbook --inventory inventory/hosts playbooks/ansible-tldr-apt.yml
[...]
```

Cette fois ci, pour les membres du groupe `groupe_app`, on a mis à jour le système, désinstallé nano et installé vim. Tout ceci avec le [module `apt`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html).

Si vous exécutez le playbook plusieurs fois de suite, vous verrez que les fois suivantes l'état des tâches n'est plus `changed`, c'est ce qu'on appelle [l'idempotence](https://fr.wikipedia.org/wiki/Idempotence).

Pour plus de détails sur les playbooks : <https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html>

## Variables

Quand on exécute des playbooks sur plusieurs noeuds on potentiellement besoin d'avoir des paramètres différents pour chacun, ou simplement on ne veut pas mettre en dur des valeurs dans les tâches, on utilise donc des variables.

```
$ cat playbooks/ansible-tldr-debug.yml
---

- name: ANSIBLE TLDR
  hosts: all
  variables:
    my_name: Nicolas
  tasks:
    - name: print hello world
      debug:
        msg: hello {{ my_name }}
```

Là on a défini une variable `my_name` directement dans le playbook et on l'a utilisée dans la tâche `debug` grâce aux doubles accolades `{{ ... }}`. Ansible utilise [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) pour les variables et plein d'autres choses, vous retrouverez donc sa syntaxe à plein d'endroits.

De manière générale, pour l'assignation des variables on utilise plutôt les dossiers de l'inventaire. Voici comment ça se présente :

```
$ tree inventory/
inventory/
├── group_vars
│   ├── all.yml         <-- les variables assignées dans ce fichier s'appliqueront à tous les noeuds
│   ├── groupe_app.yml  <-- s'applique pour le groupe "groupe_app"
│   ├── groupe_bdd.yml
│   └── groupe_front.yml
├── host_vars
│   ├── serveur-app-01.yml  <-- les variables de ce fichier ne s'appliqueront que pour cet hôte
│   ├── serveur-app-02.yml
│   ├── serveur-bdd-01.yml
│   └── serveur-front-01.yml
└── hosts
```

Plus de détails sur les variables : <https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html>

## Rôle

Quand on fait des choses plutôt complexes, plutôt que d'avoir un playbook à rallonge, on va découper les tâches en rôles. Pour ma part j'ai tendance à faire un rôle par service.

Exemple avec le service sshd :

```
 $ tree roles/sshd/
 roles/sshd/
 ├── defaults
 │   └── main.yml  <-- ici on défini les valeurs par défaut des variables du rôle
 ├── handlers
 │   └── main.yml  <-- ici des actions qui peuvent être déclenchées lorsqu'une tâche applique un changement
 └── tasks
     └── main.yml  <-- ici les tâches à executer
```

D'autres dossiers peuvent exister dans un rôle, mais on a là les principaux. Voyons le détail des fichiers :

```
$ cat roles/sshd/defaults/main.yml
---

sshd_config:
  # ensure public key authentication is enabled
  - regexp: '^#?PubkeyAuthentication\s+.*$'
    replace: 'PubkeyAuthentication yes'
  # ensure password authentication is disabled
  - regexp: '^#?PasswordAuthentication\s+.*$'
    replace: 'PasswordAuthentication no'
  # disable challenge-response authentication
  - regexp: '^#?ChallengeResponseAuthentication\s+.*$'
    replace: 'ChallengeResponseAuthentication no'

sshd_authorized_keys: []
```

```
$ cat roles/sshd/handlers/main.yml
---

- name: restart sshd
  systemd:
    name: sshd.service
    state: restarted
```

```
$ cat roles/sshd/tasks/main.yml
---

- name: configure sshd
  notify: restart sshd
  loop: "{{ sshd_config }}"
  replace:
    path: /etc/ssh/sshd_config
    regexp: "{{ item.regexp }}"
    replace: "{{ item.replace }}"

- name: configure authorized_keys
  loop: "{{ sshd_authorized_keys }}"
  authorized_key:
    user: "{{ item.user }}"
    key: "{{ item.key }}"
    state: "{{ item.state | d('present') }}"
```

Si vous regardez le contenu du dernier fichier, vous pouvez constater qu'on utilise le [module `replace`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/replace_module.html), mais entre le nom de la tâche et l'appel du module il y a deux options :

- `notify` : qui permet de déclencher le handler nommé `restart sshd` lorsque cette tâche aura l'état "changed", ce qui aura pour effet de redémarrer le service SSH à la fin de l'exécution du playbook (uniquement si il y aura eu des changements)
- `loop` : qui permet d'exécuter le module pour chacun des éléments de la variable (de type "liste") qui lui est passée, pour chaque itération de la boucle l'élément sera disponible via la variable `item`

Plus de détails sur les rôles : <https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html>
Plus de détails sur les boucles ("loop") : <https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html>
Plus de détails sur les handlers : <https://docs.ansible.com/ansible/latest/user_guide/playbooks_handlers.html>

Ansible permet de faire encore plein d'autres choses comme des exécutions conditionnelles, utiliser des templates, des tags, chiffrer des variables, utiliser des inventaires dynamiques, utiliser ses propres modules, etc. Mais là, pas le choix il faudra passer par la documentation pour explorer tout ça. J'espère que ça vous aura donné un bon aperçu des possibilités et également l'envie d'aller plus loin.

## Idées reçues

Et pour terminer quelques réponses à des idées reçues au sujet d'Ansible ou semblable.

> *Ça prend plus de temps à écrire un rôle, le tester et le déployer, que de déployer le service à la main*

Oui mais c'est du temps gagné, partiellement en documentation, et ensuite surtout si il faut le réutiliser pour déployer de nouvelles instances supplémentaires ou dans différents environnements. C'est aussi du temps gagné quand il faut s'assurer de la conformité de la configuration d'une machine ou d'un service, au lieu de se connecter sur la machine et scruter chacun des fichiers, re-exécution du playbook et on en parle plus on sait que la machine est dans l'état attendu.

> *Ça ajoute juste une couche de complexité*

Ça ajoute potentiellement une complexité par rapport à une installation manuelle, mais ça n'est qu'une syntaxe de scripting un peu particulière à apprendre et comprendre. Ça reste plus simple et plus efficace que de faire du scripting manuel, et encore plus simple que d'apprendre un nouveau langage de programmation, donc la marche à franchir n'est franchement pas haute non plus.

> *Comme c'est automatisé on perd la maîtrise, plus personne ne sait comment faire les choses manuellement*

Alors là, grosse erreur, au contraire. Il n'y a rien de magique, ce n'est ni plus ni moins que du scripting simplifié et optimisé. Toutes les tâches sont à écrire au lieu d'être exécutée manuellement. Et faire les choses ainsi oblige à les poser, à réfléchir à ce qu'elles doivent faire, comment le faire, et ça implique souvent de devoir bien comprendre ce qu'on va faire. Ce qui n'est pas nécessairement le cas lorsqu'on bidouille un serveur jusqu'à ce qu'il tombe en marche.

Ça a même l'avantage d'avoir toutes les informations sur une installation et configuration à un seul endroit, le dépôt Git des rôles et playbooks.

<!--
vim: spell spelllang=fr
-->
