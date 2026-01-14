IMC_PROJET – PROJET PIPELINE

IMC_Projet est une application développée en Python suivant une architecture de type pipeline.
Elle permet de calculer l’Indice de Masse Corporelle (IMC), d’analyser le résultat, de générer des recommandations de santé et de sauvegarder les données utilisateur.

DESCRIPTION DU PROJET

Ce projet est conçu comme un pipeline de traitement, où chaque étape est clairement séparée et gérée par un module indépendant.
Les données circulent d’une étape à l’autre de manière séquentielle, ce qui rend le projet structuré, lisible et facile à maintenir.

ARCHITECTURE PIPELINE

Le fonctionnement du pipeline est le suivant :

Entrée utilisateur (interface graphique)
→ Calcul de l’IMC
→ Analyse du niveau de risque
→ Recommandations de santé
→ Sauvegarde des données

Chaque étape reçoit les données, les traite, puis transmet le résultat à l’étape suivante.

FONCTIONNALITÉS

Interface graphique pour la saisie du poids et de la taille

Calcul automatique de l’Indice de Masse Corporelle

Classification selon les normes de santé

Recommandations adaptées au résultat

Sauvegarde des données dans un fichier texte

Architecture modulaire de type pipeline

PRÉREQUIS

Python version 3.x

Bibliothèques Python standards (exemple : tkinter)

INSTALLATION

Cloner le dépôt GitHub :
git clone https://github.com/peterhadda/IMC_Projet.git

Accéder au dossier du projet :
cd IMC_Projet

Lancer l’application :
python main.py

STRUCTURE DU PROJET

main.py
Orchestration du pipeline et lancement de l’application

IMCAppGUI.py
Gestion de l’interface utilisateur et des entrées

IMC.py
Calcul de l’indice de masse corporelle

RecommandationSante.py
Analyse du résultat et génération des recommandations

SauvegardeIMC.py
Sauvegarde des données utilisateur dans un fichier texte

data/
Dossier contenant les fichiers de sauvegarde

UTILISATION

Lancer l’application

Entrer le poids (en kilogrammes)

Entrer la taille (en mètres)

Cliquer sur le bouton de calcul

Consulter l’IMC et la catégorie associée

Les données sont automatiquement sauvegardées

OBJECTIFS DU PROJET

Comprendre et appliquer une architecture pipeline

Apprendre la modularité en Python

Séparer l’interface, la logique métier et la persistance

Développer un projet structuré comme en contexte professionnel

LICENCE

Projet libre d’utilisation à des fins éducatives et personnelles.

AUTEUR

Peter El Hadad
Projet Python – Architecture Pipeline
