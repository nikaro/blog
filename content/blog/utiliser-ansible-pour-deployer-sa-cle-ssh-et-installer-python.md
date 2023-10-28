---
title: "Utiliser Ansible pour déployer sa clé SSH et installer Python"
date: "2017-12-30"
---

Si vous commencez à utiliser Ansible, vous pouvez vous retrouver dans ce genre de situation :

> Standing up Ansible to help manage my 30+ VPS’ and couldn’t help thinking….
>
> “I really wish I had a tool like Ansible to deploy this SSH key to these 30+ systems…” /irony
>
> — Eric Capuano ([\@eric\_capuano](https://twitter.com/eric_capuano)) [December 30, 2017](https://twitter.com/eric_capuano/status/946936989496029184)

Vous avez un paquet de machines sur lesquels :

-   votre clé SSH n'est pas déployée
-   l'authentification se fait par mot de passe
-   vous n'utilisez pas le même utilisateur
-   Python n'est pas installé

À ce moment là, vous vous dîtes que ce serait pas mal d'avoir un outil comme Ansible pour normaliser tout ça. Eh bien bonne nouvelle ! Je connais un outil qui s'appelle Ansible et qui permet de faire tout ça 🙂

La première chose à faire est de définir votre [inventaire](https://docs.ansible.com/ansible/latest/intro_inventory.html#list-of-behavioral-inventory-parameters) prenant en compte vos cas particuliers. Voici un exemple commenté :

```
# hosts.ini
# un serveur avec :
#  - un utilisateur particulier défini par 'ansible_user'
#  - pas de clé SSH, donc on défini le mot de passe via 'ansible_ssh_pass'
srv-01 ansible_user=notroot ansible_ssh_pass=topsecret
# un serveur avec :
#  - le compte root
#  - une clé SSH spécifique définie via 'ansible_ssh_private_key_file'
srv-02 ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_srv02
```

Ensuite, la seconde première chose à faire c'est d'installer Python sur toutes les machines. Pour cela on va écrire un petit playbook qui utilisera le [module raw](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/raw_module.html) permettant de balancer des commandes brutes à travers SSH :

```
# bootstrap.yml
---
- hosts: all
  gather_facts: no
  become: yes
  tasks:
    - raw: test -e /usr/bin/python || ( [ $(command -v apt) ] && apt install -y python-minimal )
    - raw: test -e /usr/bin/python || ( [ $(command -v yum) ] && yum install -y python )
...
```

Ici j'ai utilisé `gather_facts: no` pour éviter qu'Ansible ne cherche à récupérer tout un tas d'informations sur le hôtes, ce qui échouerait Python n'étant pas encore installé. Le paramètre `become: yes` sert à escalader les privilèges pour lancer les commandes en root. Et les tâches lancent une commande qui :

-   vérifie la présence du binaire de Python,
-   si le binaire est absent :
-   elle vérifie si le gestionnaire de paquet spécifié est présent,
-   et l'utilise pour installer Python le cas échéant

On a ainsi quelque chose qui fonctionne pour Debian, Ubuntu, RedHat, CentOS, Fedora, etc. Et qu'on lance avec la commande suivante:

```
$ ansible-playbook -i hosts.ini bootstrap.yml
```

La troisième et dernière des premières choses à faire, c'est de déployer la configuration normalisée que vous souhaitez (votre clé SSH, votre user, etc.). On reprend donc notre playbook précédent et on y ajoute les éléments suivants :

```
# bootstrap.yml
---
[…]
- hosts: all
  become: yes
  tasks:
    - name: create my main user
      user:
        name: myusername
        password: $6$shKSkXZIG0ZLHKOg$Ai1nQ0ETm0MavWCAapU7F5GXIK.Y9SjSDZHzUnAQB7CxgihYy8HaNKZlT.ij1DHGjeoOsRXWSDNuRgnhE5Uwg.
        groups: sudo, wheel
        append: yes
    - name: deploy my main ssh public key to my main user
      authorized_key:
        user: myusername
        key: "{{ lookup('file', '/home/nicolas/.ssh/id_ed25519.pub') }}"
...
```

On a utilisé ici les modules [user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html) et [authorized\_keys](https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html), je vous laisse aller jeter un coup d'œil à la documentation de chacun pour voir la signification et l'utilisation des différents paramètres.

On relance l'exécution de notre playbook :

```
$ ansible-playbook -i hosts.ini bootstrap.yml
```

Et c'est terminé. On peut maintenant nettoyer notre inventaire de ses variables spécifiques à chaque hôte, et utiliser les options définies globalement dans le fichier `ansible.cfg` ou dans les variables de groupes.
