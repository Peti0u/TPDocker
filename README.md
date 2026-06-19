# TP Docker

## Pourquoi Docker ?

Docker est un outil de conteneurisation qui permet de déployer plusieurs applications en simultané tout en réduisant considérablement la consommation de ressources matérielles. 

Contrairement à une machine virtuelle (VM), qui doit émuler l'ensemble des composants d'un ordinateur (y compris son propre système d'exploitation et son kernel), un conteneur partage le noyau de la machine hôte. 

Il embarque uniquement l'application et ses dépendances, ce qui le rend beaucoup plus léger, rapide et performant qu'une infrastructure basée uniquement sur des VM.

Au-delà de la performance, Docker résout le problème de la portabilité : l'application fonctionnera à l'identique quel que soit l'environnement (développement, test ou production).

Enfin, la configuration sous forme de code (Dockerfile, Docker Compose) facilite grandement l'automatisation, le versioning et l'intégration dans des pipelines CI/CD.

## Déploiement de toute l'IaC

Pour le déploiement de l'infrastructure as code, nous avons choisi de partir sur 2 applications Django possédant Gunicorn (plus performant), l'application d'e-commerce imposée et un site statique récupéré sur https://html5up.net/.

Nous avons donc commencé à déployer nos solutions à travers un Docker Compose global, qui fera appel à chaque Docker Compose présent dans chaque application pour faciliter le travail en groupe et l'implémentation du ReverseProxy par la suite via Nginx.

Puis, nous pouvons déployer nos conteneurs pour la première fois sans optimisation et sans ReverseProxy afin de vérifier leur bon fonctionnement

```
sudo docker compose up -d
```

![image](https://hackmd.io/_uploads/H1W9AOMzfx.png)

## Optimisation des conteneurs

Afin d'améliorer au maximum l'efficacité et la vitesse de déploiement de nos conteneurs, il fallait les optimiser et rendre les images les plus légères possibles.

Au départ, comme nous pouvons le voir sur la capture précédente, les images étaient assez lourdes avec en moyenne des tailles de 400 ou 500MB avant de voir leur taille réduite par 2 ou 3 après l'optimisation des images comme nous pouvons le voir ici :

![image](https://hackmd.io/_uploads/By7VWFMMGg.png)

Afin de trouver l'image la plus optimisée, nous nous sommes rendus sur le DockerHub et avons cherché l'image la plus légère possible tout en la testant rapidement pour s'assurer que l'application continuait à fonctionner malgré le rétrécissement conséquent de la taille de son image. Globalement, nous sommes souvent partis sur des versions alpine-slim qui sont plus légères car elles ne possèdent pas d'interface graphique

## Accessibilité des applications (Reverse Proxy)

Pour plus de sécurité, nous avons mis en place un Reverse Proxy sur notre application DjangoMain et RocketEcommerce afin d'isoler nos applications dans un réseau privé Docker.

Ainsi Nginx va intercepter le trafic public sur les ports 5000 et 5001 pour les rediriger localement vers les ports de Gunicorn (5005) dans notre réseau app_net ce qui empêche à notre application d'être visible de l'extérieur

## Paiement via Stripe

Pour procéder au paiement avec Stripe, nous devions d'abord connecter notre application RocketEcommerce à une base de données. Pour ce faire, nous avons créé un DockerCompose partant d'une image mysql:8.0. 

Nous avons ensuite renseigné nos variables d'environnement qui ont également été renseignées dans le .env de notre application pour permettre la connectivité entre nos deux solutions. De plus, pour que tout fonctionne, nous devions engager la migration de notre base de données sur Django afin de synchroniser le code Python avec nos tables

![image](https://hackmd.io/_uploads/BkItl3fffx.png)

Nous avons également rencontré une problématique de connectivité entre notre base de données et notre application en oubliant de les mettre sur un réseau commun, un problème rapidement résolu avec la création d'un nouveau network app_net.

Après avoir créé un compte gratuit, nous avons accédé à nos clés api gratuites et nous les avons renseignées comme variables d'environnement dans notre application et nous avons créé un superutilisateur pour pouvoir se connecter à l'interface administrateur de notre application graphiquement pour ajouter des produits à vendre et leurs caractéristiques

![image](https://hackmd.io/_uploads/H1MtPjGzMg.png)

![image](https://hackmd.io/_uploads/rJ7nv3zffg.png)

Et comme nous pouvons le voir, notre site affiche bien les produits ajoutés avec leur prix et la remise associée et le paiement via Stripe fonctionne également

![image](https://hackmd.io/_uploads/Hkzlu3fGfx.png)

Pour être sur de la mise à jour de la base de données, nous avons vérifié le bon ajout du produit créé graphiquement en nous connectant à la base de données et en faisant une requête SQL simple

```
sudo docker exec -it db-BV-19-06-2026 mysql -u wearo -p2026 Wearo
```

![image](https://hackmd.io/_uploads/SyBT-pGMzx.png)


## Solution de Monitoring && Test de Charge

Comme solution de Monitoring, nous avons choisi NetData, une solution déjà utilisée précedemment dans notre cours. Grâce à cette solution, nous avons accès à toutes les données concernant l'utilisation matérielle de notre serveur (CPU, RAM, bande passante, ...).

Par la suite, nous avons réalisé un test de charge, un envoi d'un grand nombre de requête sur notre serveur, pour tester la robustesse de notre application qui a finalement résisté et a absorbé la charge sans dégradation

![image](https://hackmd.io/_uploads/H1t4WhGzze.png)

## Vérification HealthCheck

Afin de vérifier le bon fonctionnement de nos applications et les lancer uniquement si l'infrastructure qui en dépend est fonctionnelle, nous avons mis en place plusieurs HealthCheck. 

Cela se traduit par l'utilisation de dépendances, c'est-à-dire que si notre service est "healthy" et donc en bonne santé, nous allons pouvoir déployer nos autres services

```
depends_on:
  db:
    condition: service_healthy
```


## DockerHub

Nous avons publié l'ensemble de nos images sur DockerHub puis nous les avons déployées à travers notre DockerCompose
https://hub.docker.com/r/peti0u/final-tp/tags

![image](https://hackmd.io/_uploads/ryAcihzMGe.png)

![image](https://hackmd.io/_uploads/H1ycI0zGMe.png)



## Infrastructure

![image](https://hackmd.io/_uploads/rJtKvpffze.png)


## Livrables

DjangoMain : application sur le port 5000 (ReverseProxy)

DjangoSoft : application sur le port 5005

RocketEcommerce : application ecommerce sur le port 5001 (ReverseProxy) liée à Stripe

Paradigm : site web statique visible sur le port 80

Netdata : solution de Monitoring visible sur le port 19999

Invitation sur notre dépôt GitHub par mail

## Répartition des tâches : 

#### Mathis BORKOWSKA : 
- Optimisation des conteneurs
- Monitoring
- Networking
- Test de charge
- HealthCheck
- Base de données

#### Quentin VIBRAC
- Déploiement des conteneurs
- Docker Compose
- ReverseProxy
- Intégration de Stripe
- DockerHub
- Schéma de l'infrastructure