Title: Ansible TLDR
Date: 2020-09-22 14:36
Author: Nicolas Karolak
Category: Articles
Tags: ansible, devops, linux, automatisation, adminsys
Slug: ansible-tldr
Status: draft

Besoin d'un introduction à [Ansible](https://docs.ansible.com/ansible/latest/) et la flemme de lire la documentation ?

## Principes

Ansible est un outil de [gestion de configuration](https://fr.wikipedia.org/wiki/Gestion_de_configuration). À partir d'une machine, dite "contrôleur", on exécute des tâches sur des machines distantes via SSH. Les machines distantes n'ont donc besoin que d'avoir Python installé et d'être accessible en SSH.

## Installation

La meilleure manière, selon moi, est d'installer Ansible dans un [environnement virtuel](https://docs.python.org/fr/3/library/venv.html) avec [pip](https://pip.pypa.io/en/stable/) :

```
$ python3 -m venv ~/.local/share/pyvenv/ansible-test
$ source ~/.local/share/pyvenv/ansible-test
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
serveur-front-02
```

Les premières lignes correspondent à la liste des hôtes avec leurs informations de connexion. Détails :

- `serveur-bdd-01` : il s'agit d'un nom arbitraire
- `ansible_host=` : il s'agit de l'hôte SSH distant sous forme d'un [FQDN](https://fr.wikipedia.org/wiki/Fully_qualified_domain_name), une adresse IP ou une entrée `Host` de [ssh_config](https://linux.die.net/man/5/ssh_config)
- `ansible_port=` : il s'agit du port de connexion distante SSH
- `ansible_user=` : il s'agit de l'utilisateur distant utilisé pour la connexion SSH
- `ansible_become=true` : il s'agit d'un paramètre qui permet de dire à Ansible d'acquérir les permissions root (via sudo par défaut, donc il faut que l'utilisateur soit sudoer, avec l'option NOPASSWD idéalement)

Les lignes suivantes sont les groupes et leurs membres.

Plus de détails sur l'inventaire : <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html>

Plus spécifiquement sur les options de connexion : <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters>

## Playbook

## Variables

## Rôle

<!-- vim: spell spelllang=fr
