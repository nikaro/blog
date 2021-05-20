---
title: "Ma première grosse boulette professionnelle"
date: "2020-05-03"
categories: ["Articles"]
tags: ["adminsys", "informatique"]
slug: "ma-premiere-grosse-boulette-professionnelle"
---

Pour donner un peu de contexte, je suis administrateur systèmes Linux, et au moment de cette grosse boulette je bosse chez un éditeur logiciel qui vend principalement une plateforme vidéo à destination des établissements d'enseignement ou de formation, et pour qui je fais essentiellement du deploiement et de l'administration des serveurs des clients qui font tourner ce logiciel. Avant que la catastrophe arrive, je me disais que soit j'étais très chanceux ou très compétent, car plus d'une fois j'avais lu ou entendu que ça allait forcément m'arriver de faire une "grosse boulette", c'est à dire par exemple supprimer une base de données en production, faire un `rm -rf /` accidentel, ou quelque chose dans le genre. Et après 10 ans d'expérience ça ne m'était toujours pas arrivé... Jusqu'au jour fatidique.

Ironie de l'histoire, quelques jours ou semaines avant je passais un entretien pour un autre poste pour lequel on m'avait posé la question : "quelle a été ta plus grosse erreur ? et aujourd'hui si c'était à refaire tu ferais comment ?". Ce à quoi j'ai répondu un peu fièrement je l'avoue, quelque chose comme ça : "bah j'ai la chance de n'avoir jamais produit de catastrophe jusqu'à aujourd'hui donc je n'ai pas spécialement de retour d'expérience à vous donner là-dessus".

Que s'est-il donc passé ?
-------------------------

Un client, relativement important car lui-même revendeur de notre solution auprès de plusieurs clients "importants", commence à arriver à court d'espace de stockage sur son serveur. Il nous demande donc s'il est possible de rajouter de la capacité de stockage, en regardant on voit que sa machine a quatre enclosures de disques libres, donc on lui demande d'ajouter des disques dans le serveur et on s'occupera du reste.

Le client ajoute les disques et nous demande de procéder à l'extension. Je me connecte donc sur la machine, puis je vois que le partitionnement n'est pas le même qu'habituellement, les données ne sont pas sur une partition séparée, tout est monté sur `/`. Ça s'explique par le fait que c'est une vielle installation, donc pas forcément conforme au standard de ce qu'on livre aujourd'hui. Soit, j'ajoute les nouveaux disques à la grappe RAID6, puis j'essaie de voir s'il n'y a pas moyen d'étendre la partition racine à chaud... pour arriver à la conclusion que ce n'est pas faisable, en tout cas pas facilement.

Là, j'informe le client que de notre côté on ne peut pas faire le redimensionnement à cause du partitionnement non adapté, qu'il va probablement devoir le faire lui-même via un système LiveUSB, qu'on va tout de même continuer à regarder pour voir si on peut faire quelque chose, mais qu'avant qu'on tente quoi que ce soit ce serait bien qu'il ait une sauvegarde quelque part car quoi qu'il arrive l'opération présente des risques. Et là vous voyez peut-être venir le début des ennuis, le client n'a pas de sauvegarde...

Le client n'ayant pas de technicien compétent sur Linux on se dit qu'on va devoir se passer de lui pour les opérations, même lui demander de configurer le réseau sur un système live nous parait hors de sa portée. Donc je réfléchis à la suite des opérations. Le serveur avait quatre disques, il en a maintenant quatre en plus, je me dis qu'on peut partionner correctement les nouveaux disques, migrer dessus le système et les données, redémarrer le serveur sur le nouveau partionnement, et ensuite réintégrer les anciens disques. Je teste l'opération sur une machine virtuelle en essayant d'y répliquer la manière dont est configuré le serveur. Dans ma VM, je déroule donc les opérations, je retire les derniers disques du RAID, je partitionne, je rsync, etc. Ça passe, ça fonctionne correctement. On a une solution.

Entre temps quelques semaines ont passées, le client commence à s'impatienter et à s'inquiéter de la saturation de son serveur. De notre côté le commercial en charge du client aussi vient régulièrement aux nouvelles pour savoir comment ça avance. Mine de rien je commence donc à avoir la pression. On est vendredi, je me dis "bon allez, je commence les opérations, je vais faire le partitionnement, et ensuite je me concerterais avec le client pour planifier l'interruption de service et faire le rsync".

C'est parti, je lance la connexion SSH, et je déroule ma procédure. Je commence par retirer les quatre nouveaux disques que j'avais ajouté à la grappe RAID6. Et si vous vous y connaissez en RAID, voyez probablement déjà où est le problème. Je commence à avoir des erreurs qui passe dans la console, puis plus grand chose ne répond, un simple `ls` ne fonctionne plus, le binaire est introuvable. La seule commande qui passe encore est `mdadm`, via la session SSH que j'ai d'encore ouverte. Là je commence à avoir le corps qui tremble un peu, je réalise que j'ai flingué le serveur du client, je ne sais pas encore pourquoi. Je cherche des solutions sur internet pour voir si il y a moyen de réparer ça et qu'en dehors de quelques minutes d'indisponibilité ça passe inaperçu, je tente quelques trucs, sans succès. J'informe donc mes collègues que j'ai fait une grosse bourde. Réunion de crise, on prend la décision d'aller sur place pour faire une copie des disques avec `dd` et ensuite tenter quelques manipulations sur les disques originaux. Je ferme la connexion SSH. On informe le client du problème et de ma venue. Je prend donc la voiture, dans la nuit du vendredi au samedi, direction le centre de données du client à plusieurs heures de route.

Sauve qui peut
--------------

Arrivée sur place à 10h, j'explique au client avec mon anglais basique un peu plus en détail ce qu'il s'est passé et ce qu'on va faire. On passe les différentes portes et sas, on arrive devant le serveur, je connecte clavier et écran, console remplie d'erreurs. J'éteins physiquement la machine, je la redémarre en amorçant sur une clé USB avec une Debian Live. Dans une session tmux je lance la copie des quatre premiers disques.

Pendant ce temps j'essaie de comprendre ce qu'il s'est passé, pourquoi ça a fonctionné sur ma VM et pas sur le serveur, puis essayer de reproduire en VM afin de tester des manipulations de réparations sans risques. Je lance donc ma machine virtuelle, et là je me rends compte que sur celle-ci j'avais seulement six disques, au lieu de huit. Un RAID6 peut supporter de perdre jusqu'à deux disques, pas quatre... et même si je n'avais pas étendu la partition, les données avait quand-même commencé à se répartir sur tous les disques de la grappe.

La copie des disques prend du temps, je configure donc le réseau sur le système live afin de pouvoir y accéder depuis l'hôtel et ainsi superviser l'avancement. Je lance aussi une commande qui vérifie en boucle la présence d'un processus `dd` et quitte lorsqu'il n'y en a plus, chaînée avec un envoi de mail à la fin, comme ça j'aurais une notification. Dans la soirée la copie est terminée. J'y retourne pour lancer la copie des quatre disques suivants. Et pendant ce temps-là je reproduis le problème sur ma VM, avec huit disques cette fois-ci, et je fais des tentatives de réparation, avec succès. Je réussis à ré-assembler le RAID en réintégrant les disques retirés, il y a donc un espoir de ne pas perdre toutes les données du client. Mon niveau de stress commence à redescendre.

La seconde copie termine le lendemain, je retourne au DC récupérer les disques de sauvegarde, et tenter les manipulations sur les disques originaux. Ça ne fonctionne pas. Zut. On prend la décision de réinstaller le serveur, et on restaurera les données à distance... si on arrive à les récupérer. Je prend la route du retour, avec peu d'espoir.

Lundi matin de retour au bureau, je re-tente des trucs sur les disques de sauvegarde, en m'assurant que ce ne soit pas des manipulations potentiellement destructrices. On se rend compte qu'un des disques est vide, le sort (ou l'incompétence) s'acharne. Je perds encore un peu plus espoir. On se décide à faire appel à un professionnel de la récupération de données, sans grande conviction. On lui fournit donc les disques copiés en lui expliquant la situation et les détails techniques. Il fait une copie de sauvegarde à son tour, sur laquelle il travaillera. On le laisse faire son travail en venant aux nouvelles de temps en temps. À la fin de la semaine il nous annonce qu'il arrive à voir l'arborescence des fichiers, et qu'il va lancer la récupération. L'espoir revient. Ça lui prendra une partie de la semaine suivante, et finalement on a les données !

On lance la restauration à distance, qui prend extrèmement longtemps, en effet copie plusieurs centaines de miliers de petits fichiers (des fragement TS) c'est très long. Au bout de plus de deux semaines d'indisponibilité le client commence vraiment à s'énerver et à évoquer des "représailles", à juste titre. Même si je me dis que si il avait eu des sauvegardes tout aurait été beaucoup plus simple et moins dramatique. On prend la décision de retourner sur place pour faire une copie locale, qui sera beaucoup plus rapide. Cette fois-ci j'y vais en train, trop fatigué pour prendre la voiture. Je fais la copie et avec un collègue à distance restaure les données. Tout est de nouveau en ligne, il ne manque rien, tout le monde est soulagé. Le client sera bien sûr tout de même dédommagé en gestes commerciaux et très rapidement il nous mettra à dispostion un espace de stockage pour y programmer des sauvegardes. Tout est bien qui fini plutôt bien.

Conclusion
----------

Voilà donc comment j'ai fait ma première grosse boulette professionnelle. J'aurais maintenant des choses à raconter si on me repose la question à un prochain entretien. En attendant quelles sont les conclusions à en tirer ?

Déjà, je pense avoir bien fait d'informer très rapidement du problème au lieu de laisser pourrir la situation, ou pire d'avoir fait comme si de rien était. En effet, j'aurais pu faire semblant de ne pas savoir ce qu'il s'est passé et feindre de supposer que des éléments du serveur aient lâchés sans que j'y sois pour rien. Personne n'aurait pu prouver le contraire, et ce sont des choses qui arrivent. Mais si j'avais fait ça, après ça personne n'aurait pu réparer ma conscience et mon estime de moi non plus. Car il faut dire que c'est moi qui me suis foiré sur toute la ligne, à plusieurs reprises :

- j'ai pris une décision stupide sous la pression
- je ne me suis pas tenu à la recommendation que j'avais moi même faite, de ne rien faire sans sauvegarde au préalable
- l'environnement virtuel sur lequel j'ai fait mes tests n'était pas strictement semblable à son pendant en production
- j'aurais du percuter qu'on ne peut pas retirer quatre disques d'une grappe en RAID6 qui ne peut supporter qu'une perte de deux disques
- une fois sur place et les copies faites, j'aurais du vérifier la validité de celles-ci

La seule chose qu'on pourrait reprocher au client, c'était de ne pas avoir de sauvegarde en place.

Du coup comment je ferais aujourd'hui ?

Dans une situation sous pression et avec des risques, j'éssaierais d'éviter de prendre une décision sans avoir un avis tiers qui pourrait me ramener à la raison et éventuellement voir si je vais commettre une erreur.

Des sauvegardes, toujours avoir des sauvegardes, dans tous les cas. Je ne blaguerais plus avec ça. Il me faudra une validation explicite de l'usager/client/demandeur pour faire une manipulation qui n'est pas sécurisée par une sauvegarde. Et le RAID n'est pas de la sauvegarde, la preuve on peut bousiller un RAID.

Et dorénavant je suis bien conscient que je ne suis pas infaillible, ce qui me pousse à être plus prudent dans ce que je fais.

Si vous voyez autre chose qui pourrait éviter ce genre de scénario je suis preneur, n'hésitez pas.
