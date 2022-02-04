---
title: "Gestionnaire de dotfiles : yadm vs. chezmoi"
date: "2022-02-04"
---

Il en existe un paquet d'autres, mais ce sont ces deux là qui ont retenu mon
attention car ils répondent à mes besoins et semblent aussi être ceux qui font
consensus.

Mes besoins sont les suivants :

* synchroniser ma config entre plusieurs machines, avec des OS différents
* conséquence du besoin précédent : pouvoir gérer simplement les différences
  entre les machines au sein d'un même fichier
* avoir un historique des modifications, afin de pouvoir revenir en arrière si
  besoin
* permettre un déploiement simple et rapide sur une nouvelle machine
* permettre de chiffrer/déchiffrer certains fichiers de manière transparente
* je veux un outil qui fait le job pour moi, pas un nouveau jouet à bidouiller

Actuellement j'utilise simplement Git, avec un alias pour faire pointer le
`GIT_DIR` ailleurs, la méthode est décrite plus en détails ici pour ceux que ça
intéresse : <https://www.atlassian.com/git/tutorials/dotfiles>.

L'inconvénient principal est que le processus de bootstrap est un peu
compliqué, et je ne veux plus bidouiller, je veux quelque chose qui fonctionne
simplement. Donc si un outil peut me simplifier la vie, je suis preneur.

## yadm

Descriptif :

* écrit en Python, pas de dépendances en dehors de Python lui-même et awk pour
  les templates
* un wrapper à Git, en gros `$HOME` est le `GIT_WORK_TREE`, et son `GIT_DIR` est
  déporté dans `~/.local/share/yadm/repo.git`

Avantages :

* présent dans les dépôts de la plupart des distributions
* simple, les commandes peuvent se jouer depuis n'importe quel dossier
* si on maîtrise Git la prise en main est très rapide
* à une commande de bootstrap qui permet d'exécuter un script lors du bootsrap
  (déploiement sur une nouvelle machine)

Inconvénients :

* les "fichiers alternatifs" polluent le `$HOME`
* j'ai remarqué qu'il galère sur la complétion du nom des fichiers
* le déchiffrement n'est pas transparent (sauf avec
  [transcrypt](https://github.com/elasticdog/transcrypt)), il faut exécuter une
  commande, ce n'est pas la mer à boire... et pour l'instant je ne l'utilise
  pas

=> <https://yadm.io/>

## chezmoi

Descriptif :

* écrit en Go
* créer un dossier `~/.local/share/chezmoi`, versionné avec Git, qui contient
  une copie (ou plutôt ce qui va être la source) des dotfiles

Avantages :

* le $HOME n'est pas pollué avec des fichiers templates, etc.
* écrit en Go, donc le build est un binaire qui ne nécessite pas de dépendances
* propose plus d'options pour le chiffrement, dont le très prometteur
  [age](https://age-encryption.org/)
* permet également de s'intégrer avec différents gestionnaire de mots de passe

Inconvénients :

* un poil plus complexe, par exemple il nécessite de se déplacer dans le repo
  pour commit ses changements

=> <https://www.chezmoi.io/>

## Conclusion

Pour l'instant moi choix se porte davantage sur yadm, car :

* il écrit en Python, sans dépendances, et je maîtrise davantage ce langage que
  Go
* l'utilisation est quasiment identique à celle de ma méthode actuelle, donc je
  n'ai pas à apprendre une nouvelle manière de faire
* chezmoi avait un bug de parsing de template, donc même si je préfère son
  approche, pas envie de déboguer ça

<!--
vim: spell spelllang=fr
-->
