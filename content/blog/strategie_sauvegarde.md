---
title: "Ma stratégie de sauvegarde"
date: "2022-09-03"
---

Un petit peu de généralités avant de vous en dire davantage. Quand on met en place une stratégie de sauvegarde, il y a quelques éléments à determiner :

* Qu'est-ce que je veux protéger ? Quelle données ?
* Contre quoi ? contre qui ?

À partir des réponses à ces questions je peux commencer à envisager différents scénarios et leurs conséquences. Par exemple :

* Je sauvegarde les données de mon ordinateur sur un NAS à la maison, mais je me fais cambrioler, j'ai potentiellement tout perdu.
* Mes données sont synchronisées chez un fournisseur (iCloud, Google Drive, OneDrive, Nextcloud), si le fournisseur bloque mon compte j'ai potentiellement toujours accès aux données locales. Par contre si j'efface localement mes données et que l'effacement est synchronisé, s'il y a pas de corbeille j'ai tout perdu.
* Je suis journaliste, mes données sont très confidentielles car elles peuvent compromettre mes sources, je fais donc une sauvegarde chiffrée chez un fournisseur, je fais une copie de ma clé de chiffrement et je la met dans un coffre chez moi au cas où je perd mon ordinateur. Mais une nuit ma maison brûle, et le coffre n'était pas ignifugé. J'ai une sauvegarde, mais elle est indéchiffrable.

Vous voyez ? Ce n'est pas forcément simple et il peut y avoir tout un tas de scénarios auxquels on a pas forcément pensé et qui pourraient faire qu'on se retrouve sans données ou sans moyen d'y accéder.

Et dans un cadre professionnel il y aurait davantage de questions à se poser. Par exemple, en cas de perte, combien de temps d'indisponibilité est acceptable pour que les données soient restaurées, etc.

## Personnelle

Pour ma part j'ai quatre types de données numériques que je cherche à protéger :

* Mes documents administratifs
* Mes photos
* Mes codes sources
* Mes identifiants

Pour faire simple, j'applique plus ou moins la même politique pour chacun, je cherche donc tous à les protéger contre :

1. La perte, le vol ou la destruction d'un ou de tous mes équipements
2. Le blocage de mon compte iCloud (j'ai un ordinateur et un smartphone Apple)
3. Les attaques de type ransomware
4. Le vol de données personnelles venant de pirates lambda, contre un attaquant de niveau étatique j'ai peu d'espoir, mais ce n'est pas spécialement dans mon modèle de menace de toute manière

Voilà donc comment je fait.

Le premier niveau de protection est que toutes mes données sont synchronisées sur iCloud, sauf mes sources qui sont sur GitHub. Je suis donc protégé contre le cas numéro 1. J'achète un nouvel équipement, je me connecte, et tout est de nouveau synchronisé. Si je ne peux pas valider le deuxième facteur d'authentification pour me connecter, Apple offre plusieurs possibilités dont la réinitialisation à l'aide d'un ou plusieurs contacts que j'ai défini, ou en dernier recours via une procédure à suivre sur [iforgot.apple.com](https://iforgot.apple.com/). Il y a aussi la possibilité de générer une clé de secours, mais je ne l'ai pas fait car il faudrait pouvoir la stocker quelques part.

Ensuite, le second niveau de protection est que tout le contenu de mon ordinateur est sauvegardé de manière chiffrée avec TimeMachine sur un NAS chez moi. Donc s'il arrivait que Apple décide de couper les ponts avec moi, et même de me bloquer l'accès à tous mes appareils marqués d'une pomme, dont la probabilité quand-même extrêmement faible. J'ai toujours un accès physique à mes données, même sans un Mac sous la main à l'aide de [apfs-fuse](https://github.com/sgan81/apfs-fuse) ou [APFS for Linux](https://www.paragon-software.com/us/business/apfs-linux/) par exemple. Je suis donc protégé contre le cas numéro 2 et partiellement le cas numéro 3.

La troisième niveau de protection est qu'en plus de TimeMachine, mes données sont sauvegardés chiffrées avec le logiciel [Arq](https://www.arqbackup.com) sur le stockage inclus avec leur offre Premium. Avec ce niveau je suis donc protégé contre les cas 1 et 2. Et également le cas numéro 3 de manière satisfaisante. Car en effet pour le cas numéro 3, un ransomware sur mon ordinateur pourrait infecter mon réseau local et donc mon NAS, mais il n'aurait pas accès aux sauvegardes du stockage Arq.

Pour ce qui est du cas numéro 4, toutes les communication entre ma machine et iCloud, mon NAS et le stockage Arq sont chiffrées. Donc pas spécialement d'inquiétude de ce côté là. Le bémol est que ce n'est pas du logiciel dont le code source est accessible, donc je peux pas être assuré qu'il n'y a pas de portes dérobées ou de failles béantes dans la mise en œuvre du chiffrement. Mais pour mon cas ça me semble un risque acceptable, je fait relativement et suffisamment confiance à Apple et Arq pour mettre en œuvre le nécessaire pour me protéger contre des attaquants tiers de niveau non-étatiques.

Toujours pour le cas numéro 4, j'ai une certaine hygiène numérique : je tiens mes systèmes à jour, j'utilise des listes de blocages au niveau DNS sur mon réseau local et sur tous mes appareils, j'ai une extension pour bloquer les pubs et autres sur mes navigateurs, je ne télécharge mes logiciels que depuis des sources fiables, je ne clique pas sur n'importe quels liens sur internet ou mes emails, j'utilise des phrases de passe aléatoires et différentes pour chaque site web, j'active l'authentification à double facteur là où c'est possible, je chiffre les fichiers pour lesquels ça me semble nécessaires (par exemple l'exports de mes identifiants), je configure le pare-feu sur mes équipements et sur mon réseau, etc. Donc en terme de pratiques je ne suis pas la cible la plus facile non plus.

Et on a fait à peu près le tour. Comme vous pouvez le constater j'ai appliqué la [stratégie de sauvegarde 3-2-1](https://www.nextinpact.com/article/30278/109000-quest-ce-que-strategie-sauvegarde-3-2-1) : minimum 3 copies des fichiers, sur au moins 2 supports différents, et au moins 1 sur un site distant.

Maintenant reste à identifier quels sont les points faibles de cette stratégie. Bah déjà le fait que je publie un article qui la détaille ça donne pas mal de billes à d'éventuels attaquants, ils savent où aller toquer pour essayer de rentrer. Et la plus grosse porte d'entrée et la plus sensible étant iCloud. Mais comme je le disais, je fait suffisamment confiance à Apple pour avoir des mécanismes de protection suffisants (authentification forte, limitation des attaques de type force brute, notification en cas de nouvelle connexion), donc je n'ai pas trop d'inquiétude de ce côté. Le point faible d'une attaque contre un compte iCloud, c'est l'humain, soit le propriétaire du compte soit le technicien Apple à qui on va demander la récupération du compte. Pour ce qui est du propriétaire, moi, je pense être plutôt solide et rodé contre ce genre d'attaque. Par contre pour une tentative de récupération de compte, je n'ai aucun contrôle sur la personne qui pourrait être amenée à traiter ça, mais de ce que j'ai pu lire c'est bien rodé aussi, et j'aurais le temps de voir passer une notification au cas où ça se produirait, et donc réagir en conséquence. Sinon en terme de résilience des données je pense être bien à l'abri.

## Professionnelle

Pour parler rapidement de ce que j'ai mis en place au travail pour protéger les données des clients, on a une architecture avec plusieurs paires de serveurs de fichiers en ZFS, un primaire et son replica.

Le serveur primaire fait des snapshots ZFS à différents intervals et avec une politique de rétention de ces snapshots, avec l'outil [Sanoid](https://github.com/jimsalterjrs/sanoid). Il y a l'outil Syncoid qui vient avec et qui permet de faire une synchronisation ZFS vers une machine distante via SSH. On l'utilise donc pour synchroniser les données vers le replica qui se trouve sur un autre site géographique. Le replica utilise lui aussi Sanoid pour faire des snapshots locaux, l'idée étant d'avoir des snapshots indépendants des deux côtés.

Seul le serveur primaire expose les données aux applications clientes, le replica quant à lui est en quelque sorte "hors-ligne", il est inaccessible aux applications et les systèmes de fichiers ZFS ne sont même pas montés localement dessus en temps normal.

Ensuite, sur le replica on utilise périodiquement [restic](https://restic.net) pour faire une sauvegarde chiffrée sur du stockage objet chez un autre fournisseur. Juste avant de lancer la sauvegarde avec restic, on fait un snapshot ZFS qu'on monte en lecture seule, comme ça on est sûr que sur toute la durée d'exécution les données ne vont pas bouger. À la fin le snapshot est démonté et supprimé, et une tâche de vérification du dépôt restic est exécutée pour s'assurer qu'il est dans un état consistent.

Donc pareil, on fait du 3-2-1 ici, les données sont à plusieurs endroits, chez plusieurs fournisseurs.

Et ZFS est une merveille, rien que sa fonctionnalité de snapshots en vaut la peine. Couplée avec sa réplication, qui se fait au niveau bloc et qui ne va donc pas tuer les performances de votre machine pendant qu'elle se fait (contrairement à un rsync), on atteint des sommets. Sans parler des vdevs mirror ou du RAIDz, de la compression et la déduplication... ZFS mangez en, c'est bon pour vos données.

D'ailleurs pour mon ordinateur perso, si je devais quitter Apple, j'irais probablement sur FreeBSD pour profiter de la forte intégration avec ZFS. En tout cas au moins en attendant que ça s'améliore de ce côté sous Linux, que ce soit ZFS ou btrfs.