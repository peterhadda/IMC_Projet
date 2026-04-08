# IMC_Projet

Application Python de calcul d'IMC avec interface graphique, recommandations, historique SQLite et preparation de donnees pour le machine learning.

## Objectifs

- calculer l'IMC a partir du poids et de la taille
- classifier le resultat selon des regles metier simples
- generer des recommandations de sante
- sauvegarder l'historique utilisateur
- preparer un dataset propre pour les etapes ML

## Architecture

Le projet est organise en couches.

### Application

- `main.py`
  - point d'entree
  - charge la configuration
  - initialise les services
  - lance la GUI

- `app/gui.py`
  - interface graphique
  - recuperation des saisies utilisateur
  - affichage des resultats
  - appel aux services metier

- `app/validator.py`
  - validation des donnees saisies

- `app/imc_service.py`
  - calcul IMC
  - classification IMC
  - determination du niveau de risque

- `app/recommendation_service.py`
  - recommandations par categorie IMC et niveau de risque

- `app/storage_service.py`
  - creation de la base SQLite
  - sauvegarde et lecture des enregistrements
  - export CSV

### Machine Learning

- `ml/prepare_dataset.py`
  - lecture des donnees brutes
  - standardisation des colonnes
  - nettoyage
  - creation de `target_risk`
  - sauvegarde du dataset prepare

- `ml/preprocess.py`
  - separation features / cible
  - encodage des variables categorielles
  - normalisation des variables numeriques
  - split train / test

## Structure

```text
IMC_Projet/
├── main.py
├── app/
├── data/
│   ├── raw/
│   └── prepared/
├── ml/
└── README.md
```

## Donnees

### Donnees brutes

- `data/raw/sample_records.csv`
- `data/raw/records_export.csv`
- `data/raw/recommandations.json`

### Donnees preparees

- `data/prepared/imc_dataset_prepared.csv`

### Base SQLite

- `data/data_imc.db`

## Schema de stockage

La table principale stocke notamment :

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

## Prerequis

- Python 3.x
- `tkinter`
- `pandas`
- `scikit-learn`

## Installation

```bash
git clone https://github.com/peterhadda/IMC_Projet.git
cd IMC_Projet
```

Si besoin :

```bash
pip install pandas scikit-learn
```

## Lancer l'application

```bash
python main.py
```

## Generer le dataset ML

```bash
python ml/prepare_dataset.py
```

Fichier genere :

- `data/prepared/imc_dataset_prepared.csv`

## Lancer le pretraitement ML

```bash
python ml/preprocess.py
```

Ce script :

- charge le dataset prepare
- separe `X` et `y`
- encode `gender` et `activity_level`
- scale `age`, `height`, `weight`, `bmi`
- cree un split train/test

## Utilisation de l'application

1. lancer `main.py`
2. saisir le poids, la taille, l'age, le genre et l'activite
3. cliquer sur `Calculer`
4. consulter l'IMC, la categorie et les recommandations
5. cliquer sur `Sauvegarder` pour enregistrer le resultat

## Etat actuel

- calcul IMC : OK
- recommandations reglees par regles metier : OK
- sauvegarde SQLite : OK
- export CSV : OK
- preparation dataset ML : OK
- preprocessing ML : OK
- prediction ML dans la GUI : placeholder

## Auteur

Peter El Hadad
