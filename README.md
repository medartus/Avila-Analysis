# Avila-Analysis

## Probleme

### Le dataset
Le dataset représente des caractéristiques sur les pages, colonnes et lignes de la bible Avila provenant d’images.
Chaque ligne du dataset représente les caractéristiques d’une ligne écrite, de la colonne qui la contient, et de la page qui la contient.

### But du projet
Le but de la prédiction sur ces données, est de pouvoir prédire quel copiste a écrit une ligne donnée, en fonction des différents patterns de ce texte.
La Bible ayant été écrite par 12 copistes, assimilés à des lettres, le dataset dispose de 12 classes de cible.
Il s’agit bien ici d’appliquer un algorithme de classification, pour associer des patterns d'écritures à un des copistes ayant écrit la bible.

### Forme du projet
Un travail de prédiction a donc été effectué pour fournir la prédiction, au travers de différents tests, de différents modèles et leur configuration.

Le modèle de prediction retenu a été sauvegardé, et implémenter dans un rendu sous forme d'api Flask.

## Usage

### Installation

Pour démarrer l'api Flask et être en mesure de l'utiliser pour performer des predictions avec le modèle, il suffit de suivre les étapes suivantes:

> D'abord, il faut clone le repository:
```bash
git clone https://github.com/medartus/Avila-Analysis
```
> Ensuite, **dans le dossier du projet**, installer les dependances python en executant cette commande :
```bash
pip install -r requirements.txt
```
> Enfin, toujours dans le dossier du projet, lancer l'API avec la commande suivante:
```bash
python api/api.py
```

### Utilisation

Une fois l'API demarrée, pour l'utiliser il suffit de faire une requête `GET` à l'endpoint `/predict`, en y passant en paramètres les variables de votre prediction selon le schéma suivant:

|Paramètre dans la requête|Variable de prédiction associée|
| :-: | :- |
|F0|intercolumnar distance|
|F1|upper margin|
|F2|lower margin|
|F3|exploitation|
|F4|row number|
|F5|modular ratio|
|F6|interlinear spacing|
|F7|weight|
|F8|peak number|
|F9|modular ratio/ interlinear spacing|

---
> Par exemple : [http://localhost:5000/predict?F0=0.364825&F1=-0.189174&F2=0.502357&F3=0.223290&F4=-1.168333&F5=-3.837595&F6=0.069175&F7=0.534971&F8=-2.149801&F9=-3.417834](
http://localhost:5000/predict?F0=0.364825&F1=-0.189174&F2=0.502357&F3=0.223290&F4=-1.168333&F5=-3.837595&F6=0.069175&F7=0.534971&F8=-2.149801&F9=-3.417834)

## Conclusions

### Expérience
Ce projet est une application intéressante de machine learning. Car bien qu'il soit difficile à l'oeil humain de différencier les auteurs d'une certaine habitude d'écriture et calligraphie, le machine learning y arrive particulièrement bien, du moins avec le dataset Avila.

### Apprentissage
L'exploration des données, leur visualisation et leur compréhension à été une étape importante dans l'élaboration du modèle. Cela nous a permis de comprendre en profondeur chaque variable de façon concrète, et par la suite de créer de l'information utile pour le modèle.

### Résultat
En plus de ce feature engineering, il nous a suffit de tester plusieurs modèles, d'effectuer des recherches d'hyper-paramètres optimaux, et le résultat retenu est d'une précision très satisfaisante.

## Appendix (Résultats et performances)

![Resultats](https://user-images.githubusercontent.com/45569127/103666323-c8e23280-4f74-11eb-9a05-cd75af173d60.png)
![Performances (ROC)](https://user-images.githubusercontent.com/45569127/103666276-b667f900-4f74-11eb-91ab-fadd078d5c05.png)