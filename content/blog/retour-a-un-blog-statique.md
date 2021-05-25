---
title: "Retour à un blog statique"
date: "2020-07-01"
---

Ça faisait maintenant un petit moment que mon blog était sous [Wordpress](https://wordpress.org/), avant ça il y a eu [Hugo](https://gohugo.io/), encore avant [Pelican](https://docs.getpelican.com/en/stable/), une petite période sous [Grav](https://getgrav.org/) et mes tout débuts avec [Ghost](https://ghost.org/). Et ça se pourrait que j'en ai oublié... Mais me revoilà avec un blog statique, avec Pelican.

## Pourquoi encore changer ?

Bah déjà ça se pourrait bien que j'aie la bougeotte et que quand ça ne bouge pas je m'ennuie, et donc je change pour changer. Mais il y a quand même d'autres vraies bonnes raisons de revenir à un blog statique.

Premièrement, je n'ai plus à me soucier des mises à jour de mon moteur de blog. Exit les éventuelles failles de sécurité pouvant venir de là. Aucune crainte qu'une extension ou un thème soit cassé par une quelconque mise à jour. Et ça fait des dépendances et configurations en moins sur mon serveur.

Ensuite il y a un aspect écologique à la chose. Déjà sous Wordpress j'étais passé au thème [GeneratePress](https://generatepress.com/) (pour ceux que ça intéresse il y a [Susty](https://sustywp.com/) dans la même veine) dans le but d'avoir un truc le plus léger possible, histoire que côté serveur ça consomme le moins possible et soit le plus performant possible, et côté client que ça charge le moins possible la bande passante et le navigateur, sans avoir un truc moche non plus. Eh bien avec un site statique c'est un pas de plus dans ce sens. J'ai pareillement veillé à utiliser un thème minimaliste, très léger et sans JavaScript, parce que honnêtement ça ne sert à rien pour mon petit blog (et même pour une grande partie du Web en vérité...). J'en ai aussi profité pour virer les images de tous mes articles, et il est très probable que je n'en mettrais plus dans mes futurs articles non plus, parce qu'à vrai dire je peux très bien m'en passer aussi pour mon type de publications. L'idée c'est aussi que mon blog soit facilement navigable dans un terminal avec lynx ou elinks par exemple, et probablement pour les personnes malvoyantes en même temps, bien que l'accessibilité soit une problématique à part entière sur laquelle je me pencherais certainement bientôt.

Accessoirement il y a aussi un gain en performance, mais ça n'a vraisemblablement jamais été un problème jusque là et donc ce n'est pas le but recherché, même si ça reste toujours bienvenu.

Puis sinon je préfère nettement écrire mes articles en Markdown dans mon éditeur de texte qu'utiliser l'éditeur WYSIWYG de Wordpress. Déjà parce que ça met pas le bordel avec des balises inutiles dans tous les sens. Puis l'argument qui veut qu'avec l'interface d'administration d'un SGC on puisse gérer son site depuis n'importe où est un peu bidon à mon sens, car 100% du temps je gère mon blog depuis... mon ordinateur. Donc autant ne pas ajouter un point d'entrée supplémentaire et utiliser des outils que j'utilise déjà par ailleurs (Vim, Make, Git, Rsync, etc.).

Quant au choix de Pelican, plutôt que Hugo, Jekyll ou autre, c'est juste que celui-ci est écrit en Python et donc que je serais probablement le plus à l'aise avec si il faut bidouiller et corriger des trucs, etc.

## Avec ou sans commentaires ?

Les commentaires, c'est un peu la chose pour laquelle je suis mitigé. Intrinsèquement avec un blog statique on peut dire adieu au commentaires dynamiques, sauf à passer par un outil tiers. Disqus non merci. Il y a bien son alternative éthique et libre, [Commento](https://commento.io/), mais ça aurait signifié intégrer un bloc en dessous de l'article avec une esthétique qui ne collerait pas forcément avec mon thème, et qui injecterait son JS et CCS, en contradiction avec mes objectifs de minimalisme et sobriété numérique.

Il y a ceux, comme [Ploum](https://ploum.net/la-fin-des-commentaires/) avec des très bonnes raisons, qui ont fait le choix de se passer des commentaires. L'idée me plait, en ce qu'elle va dans le sens du minimalisme. Mais d'un autre côté je trouve ça dommage de perdre l'interactivité qu'il peut y avoir dans les commentaires, par exemple j'ai apprécié les retours que j'ai eu sur l'article « [Ma première grosse boulette professionnelle](https://blog.karolak.fr/2020/05/03/ma-premiere-grosse-boulette-professionnelle/) ». Sans commentaires ces retours auraient et pourront très bien se faire par des courriels échangés en privé, mais je pense qu'il y a une partie des gens qui commentent qui ne le font pas uniquement pour échanger avec le rédacteur, mais également avec la communauté, et les courriels privés ne répondent pas à ce besoin.

Il y en a d'autres comme [Cyrille Borne](https://cyrille-borne.com/) ou [Korben](https://korben.info/) qui ont déporté leurs commentaires dans un forum, ça a ses avantages. Mais je n'ai pas viré un SGC pour me retrouver à administrer un forum derrière.

La solution que j'ai finalement trouvée, ouvertement pompée chez [Drew DeVault](https://drewdevault.com/), c'est de déporter les commentaires sur une liste de diffusion publique. Je publie un article, et en pied de page de celui-ci il y un lien vers la liste de diffusion avec le titre de l'article. Ainsi chacun peut aller voir si il y a des commentaires pour un article donné, et le cas échéant participer à la discussion, ou en commencer une nouvelle. Ça permet de continuer la discussion via un moyen simple, qui ne nécessite pas de créer un compte sur une plateforme tierce (tout internaute possède déjà une adresse électronique), mais qui en même temps peut décourager certains commentateurs qui voudraient uniquement cracher leur haine, ou alors réfléchiront à deux fois quant à savoir si leur commentaire vaut vraiment la peine d'être écrit.

*[WYSIWYG]: What You See Is What You Get
*[SGC]: Système de Gestion de Contenu
