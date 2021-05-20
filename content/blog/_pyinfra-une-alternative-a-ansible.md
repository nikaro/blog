---
title: "Pyinfra, une alternative à Ansible"
date: "2020-06-21"
categories: ["Articles"]
tags: ["adminsys", "ansible", "devops", "informatique", "pyinfra", "python"]
slug: "pyinfra-une-alternative-a-ansible"
draft: true
---

Dans l'un de mes [derniers liens en vrac](https://blog.karolak.fr/2020/06/15/liens-en-vrac-n3/) je vous partageais le projet [pyinfra](https://pyinfra.com/), voici donc un petit comparatif avec Ansible. Pour l'exercice on va déployer un [rss2email](https://github.com/rss2email/rss2email).

## Installation

- Ansible

```
# pip install ansible
```

- Pyinfra

```
# pip install pyinfra
```

## Inventaire

```
# cat inventories/hosts.py
hosts = [
    'my.example.net',
]
```
