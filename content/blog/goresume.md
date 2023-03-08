---
title: "GoResume, réinventer la roue, encore"
date: 2023-03-08T21:33:05+01:00
---

Bon, j'avais déjà écrit un outil permettant de générer des CV basé sur le
"standard" [JSON Resume](https://jsonresume.org), il s'agissait de
[resume-pycli]({{< ref "/blog/cv-en-integration-continue.md" >}}), pour les
raisons évoquées. Mais voilà que j'ai tout de même commis
[GoResume](https://github.com/nikaro/goresume), une réécriture en Go.

## Pourquoi ?

Il y a plusieurs raisons à cette réécriture. La principale étant que,
wkthmltopdf n'étant plus maintenu j'ai du le remplacer par autre chose et cet
autre chose pose des problèmes de packaging pour Hombrew. Ce soucis disparaît
lorsqu'il ne s'agit plus que de fournir un simple binaire, comme c'est le cas
avec du Go. Et surtout le travail de packaging est grandement facilité par
[GoReleaser](https://goreleaser.com).

Ensuite, l'autre raison est simplement que ces derniers temps je
[m'amuse davantage avec Go]({{< ref "/blog/tech-2022.md#go" >}}).

## Différences ?

Ce n'est pas simplement une réécriture pour le plaisir d'une réécriture, ça a
aussi été l'occasion d'ajouter quelques fonctionnalités :

* Le format d'entrée, bien que toujours basé sur JSON Resume, peut accepter sur
du YAML ou du TOML.
* Le système de templating gère l'internationalisation.
* La sortie HTML ou PDF peut se faire sur stdout, ce qui peut être utile si on
veut l'empaqueter dans un contenur.
* Le thème peut se configurer indépendamment pour le PDF et le HTML.

## Hugo ?

On pourrait se poser la question quant à savoir s'il y a un avantage à utiliser
GoResume plutôt que Hugo, comme [certains le font](https://github.com/eddiewebb/json-resume).
Surtout que ça se fait très facilement grace aux
[Data Templates](https://gohugo.io/templates/data-templates/). Donc pour être honnête,
si vous n'avez pas le besoin de générer un PDF, et qu'un site statique en HTML
vous suffit, il y a toutes les raisons d'utiliser Hugo plutôt que GoResume :
meilleur templating, probablement une foison de thèmes déjà existants, un outil
beaucoup plus éprouvé et populaire, etc.

Sinon, si vous voulez générer le PDF en même temps que le HTML, GoResume est là
pour vous servir.

Idéallement j'aurais aimé que GoResume se base sur Hugo, mais je n'ai pas
encore trouvé comment faire, peut-être à l'avenir.
