# orchestration-ml-kubeflow-simplified
Ceci est le projet "Orchestration ML Kubeflow" qui à été simplifier pour être plus facilement "debuger" et "analyser" par le correcteur, vous pouvez retrouver le projet comme nous contions le faire sur ce lien "https://github.com/Athroniaeth/orchestration-ml-kubeflow". Vous pouvez retrouver la documentation / présentation du projet (qui est le même contenu du README.MD avec les images) sur ce lien : "https://docs.google.com/document/d/1LijRjtkPeytP10yCTLhzfp_WO5_ThMULkHGm2Dg9ITE/edit?usp=sharing"

## Projet Choisi:
Le projet utilise un dataset disponible sur Roboflow Universe, spécifiquement conçu pour entraîner des modèles de détection d'objets basés sur l'architecture YOLOv8. Le lien vers le dataset est le suivant : Roboflow Universe Dataset.

## Lien du GitHub : 
https://github.com/Athroniaeth/orchestration-ml-kubeflow-simplified

## Présentation du Dataset
Le dataset est soigneusement partitionné en trois sous-ensembles distincts :
- Train : Données d'entraînement, elle serviront à mettre à jour les poids du modèle, ce qui permettra à la fin de l'entraînement d’utiliser les images sur que le modèle n’à jamais vu et d’effectuer des prédictions similaire à ce pourquoi le datasets à été labellisé
- Test : Données de tests, elles serviront pendant l'entraînement à avoir une metrics “objectifs” ne ce basant pas sur les images que le modèle à déjà vu pour être sur que le modèle ne récite pas du par coeur (surapprentissage)
- Valid : Données de validation, elle seront utilisé à la fin pour tester la performance de notre modèle (car utiliser les données de test peuvent être biaisé vu qu’on à essayer d’obtenir le meilleur score sur ces données), avoir un taux de précision sur des données sur lesquelles le modèle n’à ni été entraîné, ni eu comme objectif d’avoir une bonne précision est un bon moyen de tester avec fiabilité les performances réelles du modèles

Le dataset contient des annotations de boîtes englobantes (bounding boxes) pour 18 classes d'objets, principalement des animaux tels que les **“buffalo”**, **“deer”**, **“elephant”**, **“gaur”**, **“cherentities”** et les humains **“persons”** (tous à +3000 instances pour 9809 images)

## Objectif du Projet
L'objectif principal de ce projet est de développer un modèle de détection d'objets robuste et efficace qui peut être appliqué dans des domaines tels que la surveillance de la faune, la recherche en écologie, et potentiellement la sécurité humaine dans des environnements où la faune et les humains coexistent.

## Rapport de Performance du Modèle Entraîné
### Informations Générales
Le modèle est basé sur l'architecture YOLOv8.0.170 et a été implémenté en utilisant Python 3.11.0 et PyTorch 2.0.1. L'entraînement et l'évaluation ont été effectués sur une machine équipée d'une NVIDIA GeForce RTX 3070 Laptop GPU avec 8192 MiB de mémoire vidéo.
Architecture du Modèle
Le modèle est composé de 168 couches et contient un total de 11 132 550 paramètres ajustables. Il est à noter que les gradients n'étaient pas présents dans le résumé du modèle, ce qui pourrait indiquer que cette exécution spécifique était destinée à l'évaluation et non à l'entraînement.
### Entraînement du Modèle
Le modèle a été entraîné en utilisant une version pré-entraînée de YOLO v8, spécifiquement la variante "small". Les images ont été redimensionnées à une résolution de 412 x 412 pixels. L'entraînement a été effectué sur 10 epochs.
Évaluation des Performances
Le modèle a été évalué sur un ensemble de données de test composé de 747 images, contenant un total de 1421 instances d'objets détectées. Les métriques clés sont les suivantes :
- mAP50: 0.69 (toutes classes)
- mAP50-95: 0.422 (toutes classes)
  
Ces métriques indiquent une performance raisonnable du modèle, bien que des améliorations soient possibles. Un mAP50 de 0.69 est un indicateur solide de la capacité du modèle à détecter des objets avec un seuil de confiance de 50%. Cependant, le mAP50-95 de 0.422 suggère que la performance du modèle diminue à des seuils de confiance plus élevés.

### Performances par Classe
Les performances du modèle varient considérablement entre les différentes classes. Par exemple :
- Classe "Raccoon": Précision de 0.575, Rappel de 0.333, mAP50 de 0.559, mAP50-95 de 0.291.
- Classe "Buffalo": Précision de 0.902, Rappel de 0.946, mAP50 de 0.972, mAP50-95 de 0.763.
- Classe "Person": Précision de 0.878, Rappel de 0.861, mAP50 de 0.88, mAP50-95 de 0.502.

### Lexique : 
**mAP50-95** est une métrique d'évaluation pour les modèles de détection d'objets qui mesure la précision moyenne en considérant une plage de seuils de confiance, généralement de 50% à 95%. Cela fournit une évaluation plus complète de la performance du modèle sur un éventail de confiances de détection.


**mAP50** est une métrique d'évaluation de la qualité des modèles de détection d'objets qui mesure la précision moyenne en considérant les 50 meilleures prédictions par classe.
Vitesse d'Exécution
Le modèle a été optimisé pour une exécution rapide, avec des temps d'exécution par image comme suit :
- Préparation: 0.1 ms
- Inférence: 2.1 ms
- Perte: 0.0 ms
- Post-traitement: 1.5 ms

### Discussion et Perspectives Futures
Bien que le modèle affiche des performances respectables, il existe des opportunités pour des améliorations futures. L'ajout de données supplémentaires, l'ajustement des hyperparamètres, ou l'exploration de techniques de régularisation pourraient contribuer à améliorer la performance globale. De plus, une comparaison avec d'autres architectures de détection d'objets pourrait fournir des insights précieux sur les avantages et les inconvénients de l'approche actuelle.
## Présentation API :
Notre API à été créée avec la librairie Fast API, pour lancer le serveur vous pouvez exécuter le fichier python “app/main.py” ou utiliser la commande uvicorn “uvicorn machin truc”. La route de prédiction se trouve sur “127.0.0.1:8000” et ne fonctionne qu' avec une requête POST.
- 127.0.0.1:8000/predict (POST) :
renvoie un json (object Pydantic) qui est une liste de “Prédiction” qui renvoie le “label” en texte, la “confidence” en nombre flottant et la “boxes” qui est une liste de nombre flottant, toujours de taille 4
	
## Tests :
Pour ce projet, nous avons créé un fichier contenant le code demandé pour tester l’application (modifié pour ce basé sur notre url et sur nos routes + routes de retour d’image) test.py

## Résultat dashboard : 
(sur le document word)

