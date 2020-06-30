Title: Monter un serveur de sauvegardes avec BorgBackup
Date: 2017-05-05 19:45
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, auto-hébergement, floss, informatique, tutoriels
Slug: monter-un-serveur-de-sauvegardes-avec-borgbackup
Status: published

Un petit mémo/tutoriel sur le mise en place d'un serveur de sauvegarde avec [BorgBackup](https://borgbackup.readthedocs.io/). Il s'agit d'un logiciel de sauvegarde avec déduplication, qui supporte la compression et le chiffrement. Si vous voulez en savoir davantage je vous invite à aller jeter un coup d'œil à la documentation, ou à l'[article de Cascador sur le sujet](https://www.blog-libre.org/2016/08/21/borgbackup-borg-pour-les-intimes/). Merci à lui, au passage, de m'avoir fait découvrir cet outil :-)

Pour resituer le contexte, j'ai quatre serveurs persos hébergés chez [Scaleway](https://www.scaleway.com/) dans leur datacenter de Paris. Ceux-ci n'étant pas très réputés pour la sécurité des données (à ce prix-là il n'y a rien d'étonnant), il est plutôt judicieux d'avoir une bonne stratégie de sauvegarde. J'ai donc pris un cinquième serveur, situé dans le datacenter d'Amsterdam (au cas où Paris prend feu) pour servir de serveur de sauvegarde.

```
  +-------------------------+    +-------------------------+
  |          Paris          |    |        Amsterdam        |
  +-------------------------+    +-------------------------+
  |                         |    |                         |
  |        Serveur 1---\    |    |                         |
  |                     \   |    |                         |
  |        Serveur 2-\   \  |    |                         |
  |                   >===>=|====|=======>Serveur 5        |
  |        Serveur 3-/   /  |    |                         |
  |                     /   |    |                         |
  |        Serveur 4---/    |    |                         |
  |                         |    |                         |
  +-------------------------+    +-------------------------+
```

Le paquet `borgbackup`, disponible dans les dépôts de la distribution ou via `pip`, doit être installé sur tous les serveurs.

Sur `Serveur 5` on va créer un utilisateur dédié à recevoir les sauvegardes, avec les dossiers qui vont être nécessaires pour la suite :

```
useradd -d /home/backup -m -r -U backup
su - backup
mkdir /home/backup/.ssh
mkdir /home/backup/repos/srv{1,2,3,4}
```

Chaque client (les serveurs à sauvegarder) aura son dépôt dédié dans le dossier `/home/backup/repos`, par exemple `/home/backup/repos/srv1` pour `Serveur 1` et ainsi de suite.

Sur le client `Serveur 1`, en root, on va créer une clé SSH qui servira à l'authentification sur serveur `Serveur 5` :

```
ssh-keygen -t ed25519
```

Validez en appuyant sur la touche « Entrée » à toutes les questions, à moins de savoir exactement ce que vous faites.

Vous devriez maintenant avoir une clé privée contenue dans le fichier `/root/.ssh/id_ed25519`, et une clé publique contenue dans le fichier `/root/.ssh/id_ed25519.pub`. La clé privée est à garder en sécurité et à ne jamais partager.

Sur le serveur `Serveur 5`, il va falloir ajouter dans le fichier `/home/backup/.ssh/authorized_keys` la clé publique de chacun des clients avec l'option `command`, sur le modèle suivant :

```
command="cd /home/backup/repos/<SRV#>; borg serve --restrict-to-path /home/backup/repos/<SRV#>",no-port-forwarding,no-x11-forwarding,no-agent-forwarding,no-pty,no-user-rc <CLÉ_PUBLIQUE_DE_SRV#>
```

Exemple pour `Serveur 1` :

```
command="cd /home/backup/repos/srv1; borg serve --restrict-to-path /home/backup/repos/srv1",no-port-forwarding,no-x11-forwarding,no-agent-forwarding,no-pty,no-user-rc ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG+n17i8h2PF1/OTv62Ax/mOYhpWpDNDHXukGaK3Noaf root@srv1
```

L'option `command` permet de restreindre l'utilisation de la connexion SSH à une commande donnée, pour le client qui utilisera la clé publique associée. Si vous voulez en savoir plus sur cette étape vous pouvez consulter la [documentation de Borg](https://borgbackup.readthedocs.io/en/stable/deployment.html#restrictions) dédiée, ou le [manuel du service SSH](http://man.openbsd.org/sshd#command=%22command%22) concernant cette option.

Ceci étant fait pour tous les clients, il reste à configurer et planifier la sauvegarde sur ceux-ci.

Sur chaque client, faudra commencer par initialiser son dépôt avec la commande suivante :

```
borg init backup@<ADRESSE_DE_SRV5>:repo
```

La phrase de passe est à conserver soigneusement, c'est elle qui chiffre et déchiffre les données à sauvegarder. Si vous la perdez vos sauvegardes seront inexploitables.

Pour faciliter l'exécution de la sauvegarde on va faire un script, à placer par exemple dans `/usr/local/bin/borg-backup` :

```
#!/bin/bash

REPO='backup@<ADRESSE_DE_SRV5>:repo'

LIST=(
  /etc
  /root
  /usr/local
  /var/backups/mariadb
  /var/www
)

export BORG_PASSPHRASE='<VOTRE_PHRASE_DE_PASSE>'

function main() {
  # backup
  borg create --compression lz4   
   ${REPO}::'{now:%Y-%m-%d}'   
   "${LIST[@]}"

  # rotation
  borg prune ${REPO}   
   --keep-daily=7 --keep-weekly=4 --keep-monthly=6
}

if [[ "${BASH_SOURCE}" == "${0}" ]]; then
  main "${@}"
fi
```

Avec ce script, chacun des fichiers et dossiers présents dans la variable `LIST` seront sauvegardés. Pour le reste, je vous laisse consulter la documentation de Borg, ou posez vos questions par mail/commentaire :-)

On oublie pas de rendre le script exécutable :

```
chmod +x /usr/local/bin/borg-backup
```

Il ne reste plus qu'à planifier l'exécution du script toutes les nuits via une tâche cron. Pour ceci on ajoute la ligne suivante dans le fichier `/etc/crontab` :

```
30 3 * * *    root    /usr/local/bin/borg-backup
```

Et voilà, les serveurs sont sauvegardés ! Du moins à la prochaine exécution de la crontab…

Quelques commandes supplémentaires pour faire joujou :

- Lister les sauvegardes du dépôt :

```
borg list backup@<ADRESSE_DU_SERVEUR>:repo
```

- Lancer manuellement une sauvegarde :

```
borg create backup@<ADRESSE_DU_SERVEUR>:repo::<NOM_DE_LA_SAUVEGARDE> <ÉLÉMENTS_À_SAUVEGARDER>
```

- Supprimer une sauvegarde :

```
borg delete backup@<ADRESSE_DU_SERVEUR>:repo::<NOM_DE_LA_SAUVEGARDE>
```

- Extraire le contenu d'une sauvegarde :

```
borg extract backup@<ADRESSE_DU_SERVEUR>:repo::<NOM_DE_LA_SAUVEGARDE>
```

- Monter une sauvegarde :

```
borg mount backup@<ADRESSE_DU_SERVEUR>:repo::<NOM_DE_LA_SAUVEGARDE> <POINT_DE_MONTAGE>
```

Le reste et les détails sont dans la [documentation](https://borgbackup.readthedocs.io/en/stable/usage.html).
