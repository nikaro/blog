---
title: Mon environnement de développement Python
date: 2024-08-30
draft: true
---
Je suis arrivé un setup que je trouve satisfaisant et je souhaite simplement le partager.

## Helix

Premièrement, le point d'entrée c'est mon éditeur : [Helix](https://helix-editor.com). Mais ça peut fonctionner avec n'importe quel éditeur qui sait parler le protocole \[LSP\]([https://en.wikipedia.org/wiki/Language\_Server\_Protocol](https://en.wikipedia.org/wiki/Language_Server_Protocol)).

Pourquoi pas VSCode comme tout le monde ? Au delà du fait qu'il ne soit pas vraiment libre et un peu verrouillé par Microsoft, et que je n'aime pas spécialement les applications Electron et l'écosystème JavaScript, c'est surtout une préférence personnelle pour l'utilisation du terminal. Je passe mon temps à lancer du `ls`, `cd`, `ssh`, `kubectl`, `grep`, `git`, etc. donc ça a du sens que mon éditeur y soit aussi. Je m'y sens plus à l'aise et donc plus efficace.

Dans ce cas pourquoi pas (neo)vim ? C'est justement celui que j'utilisais au préalable, il a l'avantage d'être installé par défaut quasiment partout et donc il y a un fort intérêt à savoir le maîtriser, par exemple pour éditer un fichier de configuration sur une session SSH distante. Cependant c'est de moins en moins nécessaire avec la prégnance de la gestion des infrastructures "as code", d'autant plus avec le modèle GitOps. Et Helix a de sérieux avantages sur vim à mes yeux. Premièrement et principalement, le support de LSP sans avoir à passer par des plugins et de la configuration VimScript ou Lua. Et il en va de même pour tout un tas de fonctionnalités qui sont fournies par défaut, là où vim requiert des plugins. Ensuite, bien que déroutant au premier abord, le paradigme inspiré de Kakoune qui consiste à faire du `motion -> action` en mode selection par défaut, là où vim fait du `action -> motion,` me semble au final plus cohérent et intuitif.

## Ruff

Il a remplacé tout ce que je pouvais utiliser pour le linting et la mise en forme.

## Jedi

Particulièrement \[jedi-language-server\]([https://github.com/pappasam/jedi-language-server](https://github.com/pappasam/jedi-language-server)) en remplacement de \[python-lsp-server\]([https://github.com/python-lsp/python-lsp-server](https://github.com/python-lsp/python-lsp-server)).

## BasedPyright

En remplacement de mypy (et pyright).