# IMC_Projet

Application Python de calcul d'IMC avec interface graphique, recommandations, historique SQLite et pipeline de machine learning.

## Vue d'ensemble

Le projet suit un pipeline complet :

`Saisie utilisateur -> Validation -> Calcul IMC -> Analyse classique -> Prediction ML -> Recommandation -> Sauvegarde -> Historique`

Le projet permet de :

- calculer l'IMC a partir du poids et de la taille
- classer le niveau de risque avec une regle classique
- generer des recommandations de sante
- enregistrer l'historique utilisateur dans SQLite
- preparer un dataset pour le ML
- entrainer plusieurs modeles
- evaluer le meilleur modele
- sauvegarder le modele et sa configuration
- reutiliser le modele dans l'application

## Architecture

### Point d'entree

- `main.py`
  - charge la configuration
  - initialise les services
  - lance la GUI

### Couche application

- `app/gui.py`
  - interface graphique principale
  - boutons :
    - `Calculer IMC`
    - `Predire avec ML`
    - `Sauvegarder`
    - `Voir historique`
    - `Exporter CSV`
    - `Reinitialiser`

- `app/validator.py`
  - validation des saisies utilisateur

- `app/imc_service.py`
  - calcul de l'IMC
  - classification IMC
  - determination du risque classique

- `app/recommendation_service.py`
  - recommandations selon categorie IMC et risque classique

- `app/storage_service.py`
  - creation de la base
  - sauvegarde des enregistrements
  - lecture de l'historique
  - statistiques
  - export CSV

- `app/history_service.py`
  - facade metier pour l'historique et les statistiques

- `app/predictor_service.py`
  - chargement du modele ML
  - construction des features
  - prediction du risque
  - calcul de la confiance
  - formatage du resultat ML pour la GUI

### Couche machine learning

- `ml/prepare_dataset.py`
  - lecture des donnees brutes
  - renommage des colonnes
  - nettoyage
  - creation de `target_risk`
  - sauvegarde du dataset prepare

- `ml/preprocess.py`
  - separation `X / y`
  - split train / test
  - pipeline de preprocessing sklearn

- `ml/train_model.py`
  - entrainement de plusieurs modeles :
    - Logistic Regression
    - Decision Tree
    - Random Forest
  - comparaison des scores
  - choix du meilleur modele
  - sauvegarde du meilleur modele

- `ml/evaluate_model.py`
  - calcul des metriques :
    - accuracy
    - precision
    - recall
    - f1_score
  - generation du rapport d'evaluation
  - decision d'autorisation GUI

- `ml/save_model.py`
  - sauvegarde / chargement du modele
  - sauvegarde / chargement de la configuration des features

## Structure

```text
IMC_Projet/
├── main.py
├── app/
│   ├── gui.py
│   ├── validator.py
│   ├── imc_service.py
│   ├── recommendation_service.py
│   ├── storage_service.py
│   ├── history_service.py
│   └── predictor_service.py
├── ml/
│   ├── prepare_dataset.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── save_model.py
├── data/
│   ├── raw/
│   └── prepared/
├── models/
└── README.md
```

## Donnees

### Donnees brutes

- `data/raw/sample_records.csv`
- `data/raw/records_export.csv`
- `data/raw/recommandations.json`
- `data/raw/data_imc.db`

### Donnees preparees

- `data/prepared/imc_dataset_prepared.csv`

### Base active

Le projet reutilise automatiquement :

- `data/raw/data_imc.db` si elle existe
- sinon `data/data_imc.db`

## Schema de stockage

La table principale stocke :

- `id`
- `weight`
- `height`
- `age`
- `gender`
- `activity_level`
- `bmi_value`
- `bmi_category`
- `risk_level_rule`
- `risk_level_ml`
- `prediction_confidence`
- `created_at`

## Artefacts ML

Les fichiers produits par l'entrainement sont :

- `models/best_model.pkl`
- `models/feature_config.json`
- `models/evaluation_report.json`

`feature_config.json` contient notamment :

- `feature_order`
- `numeric_features`
- `categorical_features`
- `encoded_feature_names`
- `label_mapping`
- `target_column`
- `model_name`

## Prerequis

- Python 3.x
- `tkinter`
- `pandas`
- `scikit-learn`

## Installation

```bash
git clone https://github.com/peterhadda/IMC_Projet.git
cd IMC_Projet
pip install pandas scikit-learn
```

## Lancer l'application

```bash
python main.py
```

## Pipeline ML

### 1. Preparation du dataset

```bash
python ml/prepare_dataset.py
```

Sortie :

- `data/prepared/imc_dataset_prepared.csv`

### 2. Preprocessing

```bash
python ml/preprocess.py
```

Ce script :

- charge le dataset prepare
- separe les features et la cible
- construit le pipeline de preprocessing
- cree le split train / test

### 3. Entrainement et evaluation

```bash
python ml/train_model.py
```

Ce script :

- entraine plusieurs modeles
- les compare sur le jeu de test
- choisit le meilleur
- genere le rapport d'evaluation
- sauvegarde le modele et la configuration

## Utilisation de l'application

### Calculer IMC

1. saisir :
   - poids
   - taille
   - age
   - sexe
   - niveau d'activite
2. cliquer sur `Calculer IMC`
3. consulter :
   - IMC
   - categorie
   - risque classique
   - recommandation

### Predire avec ML

1. saisir les donnees utilisateur
2. cliquer sur `Predire avec ML`
3. consulter :
   - risque predit
   - confiance
   - comparaison avec la regle classique
   - statut du modele

Note :

- si le modele est non valide selon `evaluation_report.json`, la prediction reste visible mais elle est marquee comme indicative

### Sauvegarder

Le bouton `Sauvegarder` enregistre :

- les donnees utilisateur
- le resultat classique
- la prediction ML si elle existe

### Historique et export

- `Voir historique` affiche :
  - le nombre total d'enregistrements
  - l'IMC moyen
  - la distribution par categorie IMC
  - la distribution des predictions ML

- `Exporter CSV` exporte les enregistrements au format CSV

## Etat actuel

- validation des donnees : OK
- calcul IMC : OK
- regles classiques : OK
- recommandations : OK
- sauvegarde SQLite : OK
- historique et statistiques : OK
- export CSV : OK
- preparation dataset ML : OK
- preprocessing ML : OK
- entrainement multi-modeles : OK
- evaluation du modele : OK
- sauvegarde du modele et de la config : OK
- integration du modele dans la GUI : OK

## Limite actuelle

Le meilleur modele actuel est charge dans la GUI, mais son rapport d'evaluation indique :

- `Modele non valide`

La prediction reste donc disponible a titre indicatif uniquement.

## Auteur

Peter El Hadad
