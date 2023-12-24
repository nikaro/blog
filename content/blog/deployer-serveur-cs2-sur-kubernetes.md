---
title: "Déployer un serveur Counter-Strike 2 sur Kubernetes"
date: 2023-12-23T22:10:29+01:00
draft: false
---

Quoi de mieux que de trouver un projet sympa pour se faire les dents sur une technologie ? Si vous êtes amateur de Counter-Strike et de Kubernetes j'ai peut-être ce qu'il vous faut : déployer un serveur de jeu privé, sur Kubernetes.

La première chose dont on va avoir besoin c'est une image de conteneur à déployer, pas besoin de réinventer la roue ici, il en existe déjà une : <https://github.com/joedwards32/CS2>

Ensuite, on va y aller par étapes :

* création d'un `Namespace`
* création d'un `Deployment` basique
* création d'un `PeristentVolumeClaim`
* montage du `PersistentVolumeClaim` dans le `Deployment`
* création d'une `ConfigMap`
* injection de la `ConfigMap` dans le `Deployment`
* exposition des ports du `Deployment`
* création d'un `Service` pour exposer publiquement les ports

Je pars du principe que vous avez déjà un cluster Kubernetes fonctionnel auquel vous pouvez vous connecter via `kubectl`. Pour ma part le mien est hébergé chez [Scaleway](https://www.scaleway.com/fr/kubernetes-kapsule/), sinon comme alternative européenne il y a [Exoscale](https://www.exoscale.com/sks/) et [OVH](https://www.ovhcloud.com/fr/public-cloud/kubernetes/).

TLDR : le [fichier de manifeste Kubernetes complet](/files/k8s-cs2ds.yaml).

### Namespace

L'intérêt de créer un `Namespace`[^1] est de pouvoir y "isoler" les resources. C'est surtout utile quand on fait tourner plusieurs applications dans un cluster, et/ou qu'il est partagé par plusieurs utilisateurs, ceci afin d'éviter les conflits de noms et faciliter le filtrage des ressources (`kubectl get -n <namespace> [...]`). Mais autant appliquer de bonnes pratiques dès le début.

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: cs2ds
```

On met ça dans un fichier de "manifeste Kubernetes", par exemple `k8s-cs2ds.yaml`, et il n'y a plus qu'à déployer :

```sh
kubectl apply -f ./k8s-cs2ds.yaml
```

Si tout se passe bien vous devriez le voir apparaître dans la liste :

```sh
kubectl get ns
```

### Deployment

Maintenant qu'on a notre `Namespace` on va pouvoir y déployer notre application à proprement parlé.

Pour un besoin aussi simple que le notre nous pourrions utiliser un `Pod`[^2], de cette manière :

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: cs2ds
  name: cs2ds
  namespace: cs2ds
spec:
  containers:
    - name: cs2ds
      image: joedwards32/cs2:latest
      imagePullPolicy: Always
```

Cependant c'est un cas qu'on ne retrouve pratiquement jamais dans la "vraie vie", généralement on utilise plutôt une ressource de type `Deployment`[^3].

Le notre sera dans un premier temps très basique, et ne sera pas immédiatement fonctionnel, ajoutons donc ceci dans notre manifeste :

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: cs2ds
  name: cs2ds
  namespace: cs2ds
spec:
  selector:
    matchLabels:
      app: cs2ds
  template:
    metadata:
      labels:
        app: cs2ds
      namespace: cs2ds
    spec:
      containers:
        - name: cs2ds
          image: joedwards32/cs2:latest
          imagePullPolicy: Always
```

Comme vous l'aurez peut-être constaté le `Deployment` encapsule le `Pod` en y ajoutant différentes propriétés et fonctionnalités.

Pour avoir l'explication de chaque éléments de la ressource vous pouvez utiliser la commande `kubectl explain [...]`, par exemple :

```sh
kubectl explain Deployment
kubectl explain Deployment.spec
kubectl explain Deployment.spec.selector
```

On re-déploie notre manifeste avec la même commande que précedemment, Kubernetes est suffisamment intelligent pour ne créer que les nouvelles ressources de celui-ci :

```sh
kubectl apply -f ./k8s-cs2ds.yaml
```

On peut ensuite vérifier l'état de notre `Deployment` :

```sh
kubectl get deploy --namespace cs2ds
```

Après un moment, vous devriez constater que la colonne `READY` indique `0/1`, ce qui signifie qu'aucun des `Pods` de notre `Deployment` n'est disponible.

> ℹ️ Idéallement pour que l'information de cette colonne soit pertinente il faudrait [configurer des sondes sur notre conteneur](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/). Par exemple en faisant une requête vers notre application ou en vérifiant que le port est bien en écoute.

Cela peut être normal si l'application prend du temps à démarrer, mais si l'état persiste il est probable que notre application ai un problème. Pour en avoir le cœur net on peut, entre autres, utiliser deux commandes, La première étant `kubectl describe [...]` :

```sh
kubectl describe deploy/cs2ds --namespace cs2ds
```

La sortie devrait nous indiquer l'état de notre `Deployment` un peu plus en détails, et notamment la section `Events:` tout en bas. Dans le cas présent il ne devrait y avoir aucun événement intéressant.

On peut donc utiliser la seconde commande pour notre diagnostic, `kubectl logs [...]`, qui va nous sortir les logs de notre application :

```sh
kubectl logs deploy/cs2ds --namespace cs2ds
```

On y apprendra notamment que certains fichiers/dossiers ne sont pas présents. Occupons-nous donc de fournir du stockage persistant pour notre application.

### PersistentVolumeClaim

Pour ça on va utiliser une ressource de type `PersistentVolumeClaim`[^4]. Elle va demander à notre Kubernetes créer quelque part, ce "quelque part" étant géré par l'administrateur du Kubernetes, un espace stockage avec les propriétés demandées. Ajoutons ceci à notre manifeste :

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    app: cs2ds
  name: cs2ds
  namespace: cs2ds
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 60Gi
```

Ensuite il faut rendre ce stockage disponible dans le `Deployment` et le monter dans le conteneur, comme ceci :

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: cs2ds
  name: cs2ds
  namespace: cs2ds
spec:
  selector:
    matchLabels:
      app: cs2ds
  template:
    metadata:
      labels:
        app: cs2ds
      namespace: cs2ds
    spec:
      # ici on définit les volumes qui vont être disponibles dans le Pod
      volumes:
        - name: cs2ds-data
          persistentVolumeClaim:
            claimName: cs2ds
      # cet élement est nécessaire pour que les volumes soient montés avec le GID 1000
      # qui correspond à celui de l'utilisateur défini dans notre image
      securityContext:
        fsGroup: 1000
      containers:
        - name: cs2ds
          image: joedwards32/cs2:latest
          imagePullPolicy: Always
          # on monte volume dans le conteneur
          volumeMounts:
            - mountPath: /home/steam/cs2-dedicated/
              name: cs2ds-data
```

Après avoir appliqué, pour voir si tout s'est bien passé :

```sh
kubectl get pvc --namespace cs2ds
```

### ConfigMap

La pratique habituelle pour la configuration des applications "conteneurisées" est de passer des variables d'environnement. Dans Kubernetes on utilise pour ça une ressource de type `ConfigMap`[^5].

Je vous invite à lire la [documentation de l'image du conteneur](https://github.com/joedwards32/CS2#server-configuration) pour savoir comment la configurer. Et ajoutez ceci au manifeste, en adaptant les valeurs :

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cs2ds
  namespace: cs2ds
data:
  CS2_ADDITIONAL_ARGS: ""
  CS2_GAMEMODE: "1"
  CS2_GAMETYPE: "0"
  CS2_IP: 0.0.0.0
  CS2_MAPGROUP: mg_active
  CS2_MAXPLAYERS: "12"
  CS2_PORT: "32715"
  CS2_PW: topsecret
  CS2_RCON_PORT: "32720"
  CS2_RCONPW: topmegasecret
  CS2_SERVERNAME: My Dedicated Server on Kubernetes
  CS2_STARTMAP: de_anubis
  SRCDS_TOKEN: xxxxxxx
```

Comme vous pouvez le voir on passe des éléments potentiellement sensibles dans la `ConfigMap` (`CS2_PW`, `SRCDS_TOKEN`, etc.), idéallement il faudrait plutôt utiliser des ressources de type `Secret`[^6] ou encore mieux utiliser le `Secrets Store CSI Driver`[^7] qui permet de s'interfacer avec des fournisseurs de secrets tiers, tels que Hashicorp Vault, AWS Secrets Manager, etc.

Ensuite, pour utiliser cette `ConfigMap` dans votre `Deployment`, éditez ce dernier dans votre manifeste comme ceci :

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: cs2ds
  name: cs2ds
  namespace: cs2ds
spec:
  selector:
    matchLabels:
      app: cs2ds
  template:
    metadata:
      labels:
        app: cs2ds
      namespace: cs2ds
    spec:
      volumes:
        - name: cs2ds-data
          persistentVolumeClaim:
            claimName: cs2ds
      securityContext:
        fsGroup: 1000
      containers:
        - name: cs2ds
          image: joedwards32/cs2:latest
          imagePullPolicy: Always
          volumeMounts:
            - mountPath: /home/steam/cs2-dedicated/
              name: cs2ds-data
          # injection du ConfigMap en variables d'environnement
          envFrom:
            - configMapRef:
                name: cs2ds
                optional: false
```

Pour voir la liste des `ConfigMap` :

```sh
kubectl get configmap --namespace cs2ds
```

On peut également lancer un shell dans le conteneur et vérifier si les variables d'environnement sont bien présentes :

```sh
kubectl exec -it deploy/cs2ds --namespace cs2ds -- env | grep CS2_
```

### Service

Si on jette un coup d'œil à l'état du `Deployment` et à ses logs on devrait constater que le serveur est maintenant fonctionnel. Il ne nous reste donc plus qu'à l'exposer publiquement.

On commence par éditer le `Deployment` pour exposer les ports du conteneur :

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: cs2ds
  name: cs2ds
  namespace: cs2ds
spec:
  selector:
    matchLabels:
      app: cs2ds
  template:
    metadata:
      labels:
        app: cs2ds
      namespace: cs2ds
    spec:
      volumes:
        - name: cs2ds-data
          persistentVolumeClaim:
            claimName: cs2ds
      securityContext:
        fsGroup: 1000
      containers:
        - name: cs2ds
          image: joedwards32/cs2:latest
          imagePullPolicy: Always
          volumeMounts:
            - mountPath: /home/steam/cs2-dedicated/
              name: cs2ds-data
          envFrom:
            - configMapRef:
                name: cs2ds
                optional: false
          # exposition des ports du conteneur
          ports:
            - containerPort: 32715
              name: cs2ds-tcp
              protocol: TCP
            - containerPort: 32715
              name: cs2ds-udp
              protocol: UDP
            - containerPort: 32720
              name: cs2ds-rcon-tcp
              protocol: TCP
```

Et ensuite on créer une ressource de type `Service`[^8], elle-même de type `NodePort`[^9], c'est à dire qui va ouvrir les ports directement sur le `Node`[^10]. Il existe d'autres types de `Services`, mais j'ai opté pour celui-ci dans notre cas car le load-balancer de Scaleway ne permet pas de faire transiter de l'UDP.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: cs2ds
  namespace: cs2ds
spec:
  type: NodePort
  selector:
    app: cs2ds
  ports:
    - name: cs2ds-tcp
      nodePort: 32715
      port: 32715
      protocol: TCP
      targetPort: cs2ds-tcp
    - name: cs2ds-udp
      nodePort: 32715
      port: 32715
      protocol: UDP
      targetPort: cs2ds-udp
    - name: cs2ds-rcon-tcp
      nodePort: 32720
      port: 32720
      protocol: TCP
      targetPort: cs2ds-rcon-tcp
```

### Go, go, go !

Et maintenant vous pouvez récupérer l'adresse IP publique du `Node` sur lequel tourne le `Pod` :

```sh
kubectl get nodes -o wide
```

Et dans le jeu exécuter la commande `connect <external-ip>:32715`, profitez.

### Cleanup

À la fin si on veut tout supprimer il suffit de supprimer notre `Namespace` (de l'avantage d'en avoir utilisé un) :

```sh
kubectl delete ns cs2ds
```

Comme alternative, notamment si on avait créé des ressources en dehors de notre `Namespace`, on pourrait également lui passer le manifeste :

```sh
kubectl delete -f ./k8s-cs2ds.yaml
```

### Aller plus loin

Pour un serveur de jeu Counter-Strike ce n'est pas nécessaire, puis ce n'est pas supporté par l'application, mais pour une application typique qui nécessite de pouvoir supporter une montée en charge on aurait eu besoin d'un `HorizontalPodAutoscaler`[^11]. C'est une ressource qui surveiller les métriques des conteneurs au sein du `Deployment` et en fonction des déclencheurs qu'on aura défini va augmenter ou réduire le nombre de `Replicas` de notre application.

Aussi, pour se balader dans le cluster, vérifier l'état des ressources, etc. je ne peux que vous conseiller l'excellent outil [k9s](https://k9scli.io). Il s'agit d'une TUI avec des raccourcis clavier à la ViM, et je trouve ça nettement plus efficace que de taper des commande `kubectl` à la chaîne.

[^1]: <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>
[^2]: <https://kubernetes.io/docs/concepts/workloads/pods/>
[^3]: <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
[^4]: <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>
[^5]: <https://kubernetes.io/docs/concepts/configuration/configmap/>
[^6]: <https://kubernetes.io/docs/concepts/configuration/secret/>
[^7]: <https://secrets-store-csi-driver.sigs.k8s.io>
[^8]: <https://kubernetes.io/docs/concepts/services-networking/service/>
[^9]: <https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport>
[^10]: <https://kubernetes.io/docs/concepts/architecture/nodes/>
[^11]: <https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/>
