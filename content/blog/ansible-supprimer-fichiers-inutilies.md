---
title: "Supprimer les fichiers inutilisés d'un dossier avec Ansible"
date: 2021-07-15T08:24:17Z
---

Un inconvénient qu'on rencontre parfois avec Ansible, c'est que quand on a
déployé des fichiers dans un dossier avec les modules `template` ou `file`, si
on change la liste ou le nom des fichiers déployés, les anciens ne sont pas
supprimés. C'est une action à ajouter dans une nouvelle tâche ou à faire
manuellement, mais dans ce dernier cas on perd tout l'intérêt d'Ansible.

Ce n'est pas forcément trivial à faire, voilà donc un petit mémo d'une solution
possible à ce problème :

```
- name: "récupération de la liste des fichiers existants"
  register: "ssh_configs_found"
  find:
    paths: "~/.ssh/config.d"
    patterns: "*.ssh"

- name: "création des variables intermédiaires"
  vars:
    ssh_wanted_fullpath: "{{ lookup('fileglob', '../templates/ssh_config/*.j2', wantlist=True) }}"
    ssh_found_fullpath: "{{ ssh_configs_found | json_query('files[*].path') }}"
  set_fact:
    ssh_wanted: "{{ ssh_wanted_fullpath |  map('basename') | map('regex_replace', '\\.j2$', '') }}"
    ssh_found: "{{ ssh_found_fullpath | map('basename') }}"

- name: "suppression des fichiers obsolètes"
  loop: "{{ ssh_found | difference(ssh_wanted) }}"
  file:
    path: "~/.ssh/config.d/{{ item }}"
    state: "absent"

- name: "copie des fichiers de configuration"
  loop: "{{ ssh_wanted }}"
  template:
    src: "ssh_config/{{ item }}.j2"
    dest: "~/.ssh/config.d/{{ item }}"
    mode: 0640
```

En gros, on liste les fichiers existants dans le dossier de destination, on en
extrait la différence d'avec la liste des fichiers qu'on souhaite être
présents, et on supprime cette différence.
