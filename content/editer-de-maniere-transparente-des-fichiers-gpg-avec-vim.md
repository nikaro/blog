Title: Éditer de manière transparente des fichiers GPG avec Vim
Date: 2020-12-13 15:40
Author: Nicolas Karolak
Category: Articles
Tags: vim,gpg,cli
Slug: editer-gpg-avec-vim
Status: published

Une petite astuce pour éditer des fichiers chiffrés avec GPG, de manière transparente, avec Vim. À mettre dans votre `~/.vimrc` :

```
augroup encrypted
  au!
  autocmd BufReadPre,FileReadPre *.gpg set viminfo=
  autocmd BufReadPre,FileReadPre *.gpg set noswapfile noundofile nobackup
  autocmd BufReadPre,FileReadPre *.gpg set bin
  autocmd BufReadPre,FileReadPre *.gpg let ch_save = &ch|set ch=2
  autocmd BufReadPost,FileReadPost *.gpg '[,']!gpg --decrypt 2> /dev/null
  autocmd BufReadPost,FileReadPost *.gpg set nobin
  autocmd BufReadPost,FileReadPost *.gpg let &ch = ch_save|unlet ch_save
  autocmd BufReadPost,FileReadPost *.gpg execute ":doautocmd BufReadPost " . expand("%:r")
  autocmd BufWritePre,FileWritePre *.gpg '[,']!gpg --default-recipient-self -ae 2>/dev/null
  autocmd BufWritePost,FileWritePost *.gpg u
augroup END
```

Ça marche aussi pour créer des fichiers chiffrés du coup, il suffit d'ouvrir un nouveau fichier en lui donnant `.gpg` pour extension, et à l'enregistrement il sera automatiquement chiffré :

```sh
$ vim nouveau-fichier.gpg
```

[Trouvé ici.](https://git.sr.ht/~sircmpwn/dotfiles/tree/master/.vimrc)

<!--
vim: spell spelllang=fr
-->
