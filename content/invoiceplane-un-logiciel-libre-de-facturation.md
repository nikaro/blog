Title: InvoicePlane, un logiciel libre de facturation
Date: 2016-07-13 19:10
Author: Nicolas Karolak
Category: Articles
Tags: adminsys, auto-hébergement, floss, informatique
Slug: invoiceplane-un-logiciel-libre-de-facturation
Status: published

Aujourd'hui j’aimerais vous présenter [InvoicePlane](https://invoiceplane.com/), un logiciel libre de devis et facturation. Pour deux raisons, premièrement je l’utilise et je l’apprécie, et ensuite le développeur principal lâche l’affaire et cherche un repreneur.

> InvoicePlane is a self-hosted open source application for managing your quotes, invoices, clients and payments.

Ce qui pourrait se traduire par « InvoicePlane est une application open-source auto-hébergée pour gérer vos devis, clients et paiements ».

Avec celui-ci, niveau fonctionnalités on est très loin de mastodontes que sont [Dolibarr](http://www.dolibarr.fr/) ou [Odoo](https://www.odoo.com/) (ex-OpenERP), mais c’est justement ce qu’il me fallait dans mon utilisation assez simple en tant qu’autoentrepreneur. Du coup ça serait peut-être suffisant pour quelques-uns d’entre vous.

On retrouve donc les fonctionnalités suivantes :

-   Saisie et envoie des devis, factures et paiements
-   Gestion des clients (très sommaire)
-   Paiement en ligne via PayPal

Pour l’installation c’est extrêmement simple, l’application est en PHP/MySQL, donc il n’y a qu’à décompresser l’archive sur votre hébergement, créer la base de données et servir l’application.

Si vous voulez jeter un coup d’œil un peu plus poussé à l’interface et aux fonctionnalités proposées, il y a une instance de démo à disposition à cette adresse : <https://invoiceplane.com/demo>

Comme je le disais en introduction, [le développeur principal abandonne le développement](https://community.invoiceplane.com/t/topic/2978) de l’application, donc s’il y en a qui apprécient l’outil, qui ont le temps, les compétences et qui souhaitent y contribuer, voir le reprendre en main. Je vous en serais reconnaissant. Sinon dans le message d’annonce du développeur, je découvre [InvoiceNinja](https://www.invoiceninja.com/) qui semble faire plus ou moins la même chose mais avec un business model qui semble bien établi, donc un développement potentiellement plus pérenne, à tester.
