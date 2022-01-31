---
title: "Parcourir les dépôts Git à la recherche de changements non-indexés"
date: "2020-09-16"
---

Tous les soirs avant d'éteindre mon ordinateur j'essaie de m'assurer que tous les changements que j'ai faites dans mes projets soient "commité". Si j'ai bossé sur plusieurs choses ça peut être fastidieux de devoir repasser dans chaque projet pour vérifier l'état du dépôt, et je peux en oublier.

Pour me faciliter la vie et éviter les oublis j'ai donc fait un petit script :

```sh
repos="$(find ~/src -type d -name .git -exec dirname {} +)"
for repo in $repos; do
    if git -C "$repo" status -s | grep -q .; then
        echo "$repo"
        git -C "$repo" status -s
    fi
done
```

Je récupère ainsi la liste de tous les dossiers en dessous de `~/src/` qui contiennent un dossier `.git`, et pour tout ceux pour lesquels la commande `git status` retourne quelque chose, j'affiche ce quelque chose avec le chemin du dossier.

J'ai ensuite intégré ça dans une fonction de mon `.bashrc`, que j'exécute avant d'éteindre mon ordinateur et m'assurer que tout est en ordre. J'ai une fonction `hello` pour le matin, et une `bye` pour le soir :

```sh
# manage dotfiles with git
alias dfg='git --git-dir=$HOME/.local/share/dfg --work-tree=$HOME'

# morning routine shortcut
function hello() {
        echo --- Update dotfiles ---
        dfg pull

        echo --- Update passwords ---
        pass git pull

        echo --- Update system ---
        yay -Syu

        echo --- Check today calendar ---
        khal list today
}

# evening routine shortcut
function bye() {
    echo --- Check repositories status ---
    repos="$(find ~/src -type d -name .git -exec dirname {} +)"
    repo in $repos; do
        if git -C "$repo" status -s | grep -q .; then
            echo "$repo"
            git -C "$repo" status -s
        fi
    done

    echo --- Check password store status ---
    pass git status -s

    echo --- Check dotfiles status ---
    dfg status -s
    dfg log --oneline "${u}..HEAD"

    echo --- Check today calendar ---
    khal list tomorrow
}
```

Il y a quelques pistes d'amélioration possibles. Par exemple vérifier que tous les changements ont été poussé sur le dépôt distant, ça peut se faire avec `git log ${u}..HEAD`, mais ça pose problème pour les submodules j'ai l'impression et je n'ai pas encore creuser comment faire ça proprement. Si vous avez des idées n'hésitez pas à m'envoyer ça par email.

**Mise à jour 17/09/2020 :** un [commentaire sur le JdH](https://www.journalduhacker.net/s/bfmhji/parcourir_tous_les_d_p_ts_git_la_recherche#c_mvcszf) a porté à ma connaissance un merveilleux outil, [git-summary](https://gitlab.com/lordadamson/git-summary) qui fait ça beaucoup mieux que mon bout de script, et qui en fait beaucoup plus également. Testé et joyeusement adopté.
