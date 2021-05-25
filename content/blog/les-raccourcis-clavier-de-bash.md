---
title: "Les raccourcis clavier de Bash"
date: "2019-11-25"
---

En tant qu'adminsys, le terminal est probablement l'application dans laquelle je passe le plus de temps. Du coup, afin d'être le plus efficace possible, ça vaut peut-être le coup d'apprendre à s'en servir efficacement. Notamment via les raccourcis clavier qui peuvent permettre de gagner en confort et en temps.

Voici donc une petite liste des combinaisons que je trouve potentiellement intéressantes. Avec, en bonus, la signification derrière le choix de la touche, quand je la connais et/ou qu'il y en a une, ce qui peut aider à retenir la combinaison le cas échéant.

Petite précision, ces raccourcis ne sont pas spécifiquement liés à Bash, mais (pour la plupart) à la bibliothèque [Readline](https://fr.wikipedia.org/wiki/GNU_Readline) (utilisée par Bash, entre autres).

Déplacement
-----------

-   **Ctrl + A :** aller au début de la ligne
-   **Ctrl + E :** aller à la fin de la ligne (**E**nd)
-   **Ctrl + F** : aller un caractère en avant (**F**orward)
-   **Ctrl + B** : aller un caractère en arrière (**B**ackward)
-   **Alt + B :** aller un mot en arrière (**B**ackward)
-   **Alt + F :** aller un mot en avant (**F**orward)
-   **Ctrl + XX :** aller et revenir entre le début de la ligne et la position actuelle du curseur
-   **Ctrl + L** : vider le terminal

Historique
----------

-   **Ctrl + P** : afficher la commande précédente dans l'historique (**P**revious)
-   **Ctrl + N** : afficher la commande suivante dans l'historique (**N**ext)
-   **Alt + <** : aller au début de l'historique
-   **Alt + >** : aller à la fin de l'historique
-   **Ctrl + R** : rechercher une commande (**R**everse)
    -   ensuite il suffit de commencer à écrire les caractères de la commande en question
    -   **Ctrl + R** : remonter dans l'historique de recherche
    -   **Ctrl + S** : redescendre dans l'historique de recherche, si ce n'est pas déjà utilisé par le [contrôle de flux](https://coderwall.com/p/ltiqsq/disable-ctrl-s-and-ctrl-q-on-terminal), ce qui est généralement le cas (**S**earch)
    -   **Ctrl + G** : quitter la recherche sans rien exécuter

-   **Alt + R** : annuler les changements en cours dans une commande de l'historique (**R**evert)
-   **Ctrl + Alt + Y** : insérer le premier argument de la commande précédente (**Y**anking)
-   **Alt + .** ou **Alt + _** : insérer la dernière chaîne de caractères de la commande précédente
    -   répéter la commande pour remonter dans l'historique

Modification
------------

-   **Ctrl + U** : supprimer avant le curseur jusqu'au début de la ligne
-   **Ctrl + K** : supprimer depuis le curseur jusqu'à la fin de la ligne (**K**illing)
-   **Ctrl + W** : supprimer avant le curseur jusqu'au début de la chaîne
-   **Alt + D** : supprimer depuis le curseur jusqu'à la fin de la chaîne
-   **Ctrl + Y** : restaurer ce qui a été supprimé avec l'une des combinaisons (**Y**anking)
    -   **Alt + Y** : remonter de l'historique du "[kill ring](https://www.gnu.org/software/emacs/manual/html_node/emacs/Kill-Ring.html)" et ainsi restaurer d'anciennes suppressions

-   **Ctrl + D** : supprimer le caractère sous le curseur, comme **Suppr**
-   **Ctrl + H** : supprimer le caractère avant le curseur, comme **Retour**
-   **Ctrl + J** ou **Ctrl + M** : valide la commande, comme **Entrée**

-   **Alt + U** : mettre en majuscule depuis le curseur jusqu'à la fin de la chaîne (**U**ppercase)
-   **Alt + L** : mettre en minuscule depuis le curseur jusqu'à la fin de la chaîne (**L**owercase)
-   **Alt + C** : mettre en majuscule le caractère sous le curseur (**C**apitalize)

-   **Alt + T** : inverser les deux chaînes avant le curseur (**T**ranspose)
-   **Ctrl + T** : inverser les deux derniers caractères depuis le curseur (**T**ranspose)

-   **Alt + #** : insérer un **#** au début de la ligne et valider
    -   ça revient à insérer un commentaire dans l'historique de bash

-   **Ctrl + V** : fait que le prochain caractère tapé est inséré en "**V**erbatim"
    -   faites **Ctrl + V** et appuyer **Entrée** en suite pour voir ce que ça fait concrètement, ça peut servir pour insérer une tabulation par exemple

-   **Ctrl + Insert** ou **Ctrl + Shift + C** : copier
-   **Shift + Insert** ou **Ctrl + Shift + V** : coller
    -   l'avantage de la combinaison avec **Insert** c'est qu'elle fonctionne partout

Complétion
----------

-   **Tab** : compléter l'élément (commande, chemin, arguments) sous le curseur
-   **Alt + ?** : afficher les complétions possibles
-   **Alt + \*** : insérer toutes les complétions possibles

-   **Ctrl + X (** : commencer l'enregistrement d'une macro
-   **Ctrl + X )** : terminer l'enregistrement d'une macro
-   **Ctrl + X E** : exécuter la macro précédemment enregistrée

Divers
------

-   **Ctrl + C** : arrêter la commande en cours
-   **Ctrl + Z** : suspendre le programme en cours
    -   il faut saisir la commande `fg` (foreground) pour reprendre le programme

-   **Shift + PgUp** : faire défiler vers le haut une "page"
-   **Shift + PgDn** : faire défiler vers le bas une "page"
-   **Ctrl + Shift + Haut** : faire défiler vers le haut une ligne
-   **Ctrl + Shift + Bas** : faire défiler vers le bas une ligne

Pour en savoir plus
-------------------

-   `man -P 'less -p ^READLINE' bash`
-   `man -P 'less -p ^EDITING' readline`
