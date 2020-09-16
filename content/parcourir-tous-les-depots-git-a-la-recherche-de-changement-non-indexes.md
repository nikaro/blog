Title: Parcourir tous les dépôts Git à la recherche de changements non-indexés
Date: 2020-09-16 09:40
Author: Nicolas Karolak
Category: Articles
Tags: infromatique, git, bash, automatisation
Slug: parcourir-tous-les-depots-git-a-la-recherche-de-changement-non-indexes
Status: published

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

    echo --- Check dotfiles status ---
    dfg status -s
    dfg log --oneline "${u}..HEAD"

    echo --- Check today calendar ---
    khal list tomorrow
}
```

Il y a quelques pistes d'amélioration possibles. Par exemple vérifier que tous les changements ont été poussé sur le dépôt distant, ça peut se faire avec `git log ${u}..HEAD`, mais ça pose problème pour les submodules j'ai l'impression et je n'ai pas encore creuser comment faire ça proprement. Si vous avez des idées n'hésitez pas à m'envoyer ça par email.
