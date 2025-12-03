# Module Gestion Contrat

Module Odoo pour la gestion des contrats d'alternance et de stage.

## Description

Ce module permet de gérer les contrats entre étudiants et entreprises, avec un suivi des tuteurs en entreprise. Il prend en charge deux types de contrats :
- **Alternance**
- **Stage**

## Dépendances

- `base` : Module de base Odoo
- `gestion_ecole` : Module de gestion de l'école (étudiants, formations)
- `groupe_entreprise` : Module de gestion des entreprises et salariés

## Fonctionnalités

### Modèle principal : Contrat

Le modèle `contrat.contrat` gère les informations suivantes :

- **Type de contrat** : Alternance ou Stage
- **Dates** : Date de début et de fin avec calcul automatique de la durée
- **Parties prenantes** :
  - Étudiant (lié au module gestion_ecole)
  - Entreprise d'accueil (liée au module groupe_entreprise)
  - Tuteur en entreprise (salarié de l'entreprise)
- **Formation** : Récupération automatique de la formation de l'étudiant

### Extension du modèle Personne

Le module étend `school.personne` pour ajouter :
- Liste des contrats pour les étudiants
- Liste des contrats supervisés pour les tuteurs

### Validations

- La date de fin doit être postérieure à la date de début
- Le tuteur doit être un salarié de l'entreprise d'accueil
- Les domaines limitent les choix :
  - Étudiant : uniquement les personnes de type "étudiant"
  - Tuteur : uniquement les personnes de type "salarié"

## Installation

1. Copier le module dans le répertoire `addons` d'Odoo
2. Mettre à jour la liste des applications
3. Installer le module "Gestion Contrat"

## Utilisation

### Créer un contrat

1. Aller dans le menu **Gestion Contrat > Tous les Contrats**
2. Cliquer sur **Créer**
3. Remplir les informations :
   - Type de contrat
   - Étudiant
   - Dates de début et de fin
   - Entreprise d'accueil
   - Tuteur en entreprise
4. Sauvegarder

### Consulter les contrats d'un étudiant

1. Aller dans la fiche d'une personne de type "Étudiant"
2. Consulter l'onglet **Contrats (Étudiant)**

### Consulter les contrats supervisés par un tuteur

1. Aller dans la fiche d'une personne de type "Salarié"
2. Consulter l'onglet **Contrats (Tuteur)**

## Structure du module

```
gestion_contrat/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── models.py
├── security/
│   └── ir.model.access.csv
└── views/
    └── views.xml
```

## Auteur

**MoonDev**

## Version

1.0

## Catégorie

Human Resources
