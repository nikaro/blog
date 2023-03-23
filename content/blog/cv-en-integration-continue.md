---
title: "Votre CV en Intégration Continue"
date: 2021-06-06
---

Je ne sais pas pour vous, mais pour moi ça a toujours été un exercice fastidieux de faire et refaire mon CV. Retrouver un de mes anciens CV pour le mettre à jour, me remémorer les dates, essayer de trouver un modèle moderne et beau, bidouiller pour le faire tenir sur une seule page, etc...

Jusqu'à ce que je découvre des outils qui permettent de publier son CV en ligne. Il en existe un paquet, mais si vous voulez avoir quelque chose de joli sans vous prendre la tête, je vous conseille DoYouBuzz. Celui-ci a aussi l'avantage de servir de base de données pour des recruteurs, donc vous êtes susceptibles d'être contacté, généralement pour des propositions plus pertinentes que celles venant de LinkedIn.

=> https://www.doyoubuzz.com/fr/

Par contre l'inconvénient de ce genre de plateforme est que, comme pour les réseaux sociaux, vous n'êtes plus « propriétaire » de vos données. Elles sont sur une plateforme dans un format qui vous échappe, si vous voulez les récupérer pour les exploiter ailleurs, c'est souvent impossible ou difficile.

C'est là qu'intervient l'initiative « JSON Resume » qui propose de créer un format standard pouvant être exploité ensuite sur différentes plateforme ou par l'outil de votre choix. Notamment le générateur officiel en CLI « resume-cli », avec la myriade de thèmes qui va avec.

=> https://jsonresume.org/

Personnellement j'ai eu pas mal de difficultés à le faire fonctionner, avec différents thèmes. N'étant pas familier avec JavaScript et voyant que les GitHub Issues sur les problèmes que j'ai rencontrés ne semblent pas avancer, j'ai décidé d'écrire mon propre générateur en Python.

=> https://github.com/nikaro/resume-pycli/

Il a les mêmes fonctionnalités que la CLI officielle. Vous créez un fichier JSON de base avec la commande `resume init`, vous l'éditez avec votre éditeur préféré, ensuite vous l'exportez dans le thème de votre choix `resume export --theme stackoverflow`. Et vous pouvez le visualiser dans votre navigateur avec la commande `resume serve`. Ou ouvrir le fichier généré au format PDF : `public/index.pdf`.

Si vous voulez voir à quoi ça peut ressembler, vous pouvez jeter un coup d'œil à mon CV.

=> https://cv.karolak.fr/

Reste plus qu'à intégrer le processus de génération et de publication dans une pipeline de CI, avec GitHub Actions ou Gitlab CI par exemple. Côté hébergement vous pouvez jeter un coup d'œil chez Netlify aussi, qui permet d'héberger gratuitement des sites statiques. Dans mon cas j'utilise les outils SourceHut, et voici mon manifeste de build :

```
image: archlinux
packages:
  - gtk3
  - jq
  - make
  - python-pip
  - resume-pycli
  - wkhtmltopdf
oauth: pages.sr.ht/PAGES:RW
environment:
  PATH: /home/build/.local/bin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  site: cv.karolak.fr
tasks:
  - build: |
      cd cv
      make build
  - upload: |
      cd cv
      acurl -f https://pages.sr.ht/publish/$site -F content=@site.tar.gz
```

De cette manière, vous n'avez plus qu'à mettre à jour le fichier JSON Resume et lorsque vous pousserez vos changements, votre CV sera automatiquement mis à jour.

Vous pouvez également jeter un coup d'œil au reste de mes sources.

=> https://github.com/nikaro/resume
