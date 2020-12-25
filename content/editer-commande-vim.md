Title: Éditer une commande avec Vim
Date: 2020-12-17 10:57
Category: Articles
Tags: vim, cli, sécurité
Slug: editer-commande-vim
Status: published

Encore une petite astuce Vim, ou plutôt bash ou zsh. Il est possible d'éditer avec Vim une commande dans le terminal. Pour cela il suffit de faire `Ctrl+x Ctrl+e`, ce qui aura pour effet d'ouvrir Vim et ainsi de pouvoir bénéficier de toute la puissance de celui-ci pour manipuler le texte de la commande.

Ça peut s'avérer très utile lors d'un copier/coller d'une commande sur internet, pour éviter quelques mésaventures. Par exemple la copie qui prend en compte le retour à la ligne en fin de commande et donc l'exécute immédiatement lors de la copie...

Pire encore, JavaScript permet de modifier ce qui est envoyé dans le clipboard, donc quand vous copiez un texte ce que vous voyez n'est peut-être pas ce que vous copiez. Certains sites d'actualités utilisent ce mécanisme pour insérer un lien vers la source lorsque vous copiez leur contenu. D'autres mal intentionnés pourraient vous faire copier des commandes dangereuses.

<http://thejh.net/misc/website-terminal-copy-paste>

<!--
vim: spell spelllang=fr
-->
