Title: Pourquoi je reviens à Apache après être passé à Nginx ?
Date: 2016-03-14 05:54
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, floss, informatique, web
Slug: pourquoi-je-reviens-a-apache-apres-etre-passe-a-nginx
Status: published

Ça va faire peut-être un an ou deux que je me suis mis à [NGINX](http://nginx.org/), au détriment d'[Apache](http://httpd.apache.org/). Les raisons étaient que celui-ci était présenté comme plus performant, plus léger, plus souple, etc. C'était aussi pour le fun, pour découvrir un nouvel outil. Et également me faire la main sur une technologie qui devient incontournable, afin de ne pas être à la ramasse professionnellement.

Mais aujourd'hui je reviens au bon vieux Apache… Pourquoi donc ?

### Compatibilité

Malgré la hype autour de NGINX, la majorité des applications Web sont encore faites pour fonctionner de base avec Apache. Notamment en incluant des fichiers `.htaccess` pour faire le job concernant tout ce qui est réécriture d'URLs, protection des fichiers et dossiers, etc.

Ça se voit aussi au niveau des différentes documentations. Pour prendre un exemple, la [documentation de ownCloud](https://doc.owncloud.org/) présente Apache 2.4 comme le serveur recommandé pour son installation, et la procédure d'installation et de configuration se base donc sur ce serveur Web. Pour NGINX, il faut aller fouiller au fin fond de la doc pour trouver un exemple de fichier de config à rallonge.

### Simplicité

Avec NGINX, chaque application Web nécessite une configuration spécifique différente. Pour la gestion des scripts PHP, d'une application à l'autre les paramètres `fastcgi_param` ne sont pas les mêmes. Donc pas moyen de normaliser et d'externaliser la configuration PHP dans un fichier, qu'il suffirait d'inclure dans chaque *vhost*. Toutes les règles se trouvant dans les fichiers `.htaccess` doivent être réécrites et adaptées pour NGINX, et là je vous souhaite bien du courage si la documentation de l'application ne les fournit pas ! Enfin bon, dans le contexte d'un serveur qui héberge diverses applications c'est difficile de maintenir une configuration cohérente et efficace.

### Performances

Question performances, le résultat dépend grandement du matériel et du type de sites que vous servez. En résumé, sur des petites configurations (mono-core) NGINX s'en sort mieux du fait de son architecture *[event-driven](https://fr.wikipedia.org/wiki/Architecture_orient%C3%A9e_%C3%A9v%C3%A8nements)*. Pour servir des fichiers statiques (HTML, JS, CSS, images), NGINX est là aussi encore loin devant Apache. Ceci malgré le fait qu'avec le mode MPM Worker de Apache on s'approche du fonctionnement de NGINX, et qu'avec le mode Event on y est carrément.

Par contre, pour ce qui est des applications PHP, il semblerait que Apache s'en sorte mieux (en dehors des petites config matérielles), en mode Worker ou Event.

### Conclusion

La seule raison qui pourrait me faire rester sous NGINX, c'est le côté performance pour des sites statiques, sauf que j'en ai pas et que même le cas échéant je n'ai pas de site à fort trafic. Donc bon, j'ai assez fait joujou avec NGINX et je reviens à Apache pour mon utilisation personnelle, je reviens à la simplicité.

Pour ceux qui veulent explorer davantage les différences entre NGINX et Apache, voici un article qui m'a l'air de faire une bonne synthèse : <https://www.digitalocean.com/community/tutorials/apache-vs-nginx-practical-considerations>

À suivre, un article pour [installer Apache en mode Event, avec PHP-FPM](https://blog.karolak.fr/2016/03/14/apache-mode-event-et-php-fpm/).
