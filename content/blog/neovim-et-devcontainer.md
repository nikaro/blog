---
title: "(Neo)Vim et devcontainer"
date: "2019-12-14"
---

Suite à une [discussion sur le JdH](https://www.journalduhacker.net/s/k4oduv/pourquoi_jutilise_vim_et_pourquoi_vous_ne) et mon [dernier article](https://blog.karolak.fr/2019/11/25/les-raccourcis-clavier-de-bash/), je me suis dit quitte à passer du temps dans le terminal, autant y passer tout mon temps (sauf pour la navigation Web, je ne suis pas masochiste à ce point) en passant à Vim (ou [Neovim](https://neovim.io/) plus exactement) comme éditeur de code. Sauf qu'avec Visual Studio Code, mon éditeur du moment jusqu'alors, il y a une fonctionnalité qui m'est devenue indispensable : les [devcontainers](https://code.visualstudio.com/docs/remote/containers).

Du coup, je me suis attelé à la tâche pour appliquer le concept à une utilisation dans un terminal avec Neovim. Et j'ai pondu un petit utilitaire, nommé "devc", écrit en Go (ça a été l'occasion de m'y mettre, et en conclusion j'aime assez ce langage).

Concrètement, ça lance les commandes `docker-compose` qui font appel aux fichiers dans le dossier `.devcontainer/`, dont une qui permet dans lancer un shell dans le devcontainer, d'où je peux lancer ensuite `nvim`. J'ai aussi adapté ma config Neovim pour installer les plugins à l'intérieur du devcontainer.

Ça fait maintenant une petite semaine que je l'utilise en remplacement de VSCode, ça tourne très bien et ça m'a permit de franchir le pas d'un passage à Neovim comme IDE principal.

Je vous livre donc une version 0.3.1 (à l'heure où j'ecris ces lignes), vous trouverez également les instructions pour l'installation et la configuration de Vim et des conteneurs. Ça se passe par là : <https://sr.ht/~nka/devc/>
