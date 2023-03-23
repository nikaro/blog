---
title: "Pour votre sécurité, utilisez un bloqueur de pub"
date: 2023-03-23T10:29:43+01:00
---

Un bloqueur de publicité est une mesure d'hygiène numérique de base,
indispensable. Il convient même de cumuler un bloqueur au niveau DNS avec un
autre au niveau du navigateur. Cas pratique.

La sortie à venir de Counter-Strike 2 vient d'être annoncée, en attendant
quelques invitations sont distribuées au compte goute par Valve pour tester la
version Beta.

Sur YouTube ça pullule de contenu au sujet de cette annonce. Et je vois une
vidéo de la chaîne "Valve" qui propose de s'inscrire pour pouvoir accéder la
Beta, ni une ni deux je clique en me disant que c'est legit vu que c'est la
chaîne officielle de Valve. Il y a un lien vers `source2csgo.pro`, je clique,
page blanche. Je partage le lien à quelques amis en leur disant que le site
se fait probablement DDoS sous les inscriptions. Mais l'un d'eux y arrive et
s'inscrit, mais il remarque qu'il y a un paramètre dans l'URL, `auth=error`,
qui n'a pas de sens au vu message affiché sur la page. Ça me met la puce à
l'oreille et je décide d'y retourner et d'essayer de comprendre pourquoi de mon
côté j'ai une page blanche.

J'ouvre donc la console du navigateur et je vois un message d'erreur indiquant
qu'une resource en provenance de `webdev0.com` a été bloquée. Ça fait tilt,
c'est un blocage au niveau DNS. Je vais donc voir dans la console de mon compte
[NextDNS](https://nextdns.io), je trouve la correspondance du blocage dans les
logs, et je regarde à quelle liste de blocage appartient ce domaine : Threat
Intelligence Feeds.

Oups, je me suis fait avoir comme un n00b, et j'ai fait plonger un ami
dedans avec moi. Sauf que son bloqueur à lui n'a pas n'a pas fait le job.
Je le préviens, il change son mot de passe Steam dans la foulée et surveille
l'activité de son compte.

Rétrospéctivement j'ai honte de moi, rien que le nom de domaine aurait du
m'alerter, il n'y aucune raison que Valve utilise un site autre que les
officiels de Steam ou Counter-Strike pour ce genre d'opération. Du coup je
retourne sur la vidéo YouTube qui partage le lien pour essayer de comprendre
comment ça peut se retrouver sur la chaîne de Valve, je passe ma souris sur le
nom de la chaîne: @Valve7, ce n'est pas l'officielle... double n00b. Du
coup je signale la vidéo à YouTube, quelques minutes plus tard je reçois une
notification comme quoi elle a été prise en compte et bloquée, dans la foulée
il semble que Google Safe Browsing ai aussi ajouté le site à sa liste.

Morale de l'histoire, soyez très vigilants, et utilisez un bloqueur de
publicité, en l'occurence ici c'est NextDNS qui a fait le travail. Ni
[Wipr](https://giorgiocalderolla.com/wipr.html) sur Safari, ni les listes de
blocage de [uBlock Origin](https://github.com/gorhill/uBlock) ne le bloquaient.

### Recommandations

C'est valable pour chacun des bloqueurs ci-dessous : il faut bien choisir ses
listes de blocage pour être bien couvert.

#### DNS

* [NextDNS](https://nextdns.io), bien évidemment ❤️, il y une offre gratuite
pour 300 000 requêtes/mois, après c'est 2€/mois pour de l'illimité, ça vaut
vraiement le coup.
* [Pi-Hole](https://pi-hole.net), pour ceux qui préfèrent l'auto-hébergement et
l'open-source.
* [AdGuard Home](https://github.com/AdguardTeam/AdguardHome), une alternative à
Pi-Hole, par un acteur reconnu.

#### Navigateur

* [uBlock Origin](https://github.com/gorhill/uBlock), la Rolls des AdBlock,
pour presque tous les navigateurs sauf Safari.
* [Wipr](https://giorgiocalderolla.com/wipr.html), extrèmement simple, aucune
configuration, pour Safari uniquement.
* [AdGuard](https://adguard.com/), pour presque toutes les plateformes et
navigateurs.