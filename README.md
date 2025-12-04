# Module Gestion Contrat

Module Odoo 17 pour la gestion des contrats d'alternance et de stage avec validation métier.

## 🎯 Fonctionnalités

- **Contrats d'Alternance** : Gestion des contrats pro et apprentissage
- **Contrats de Stage** : Suivi des conventions de stage
- **Liaison Étudiant-Entreprise-Tuteur** : Relations validées
- **Calcul automatique** : Durée, formation associée
- **Validations métier** : Contraintes sur dates et cohérence des acteurs

## 📋 Architecture

### Extension de `res.partner`
- `contrat_etudiant_ids` : One2many - Contrats en tant qu'étudiant
- `contrat_tuteur_ids` : One2many - Contrats en tant que tuteur
- `contrat_entreprise_ids` : One2many - Contrats de l'entreprise
- `contrat_count` : Integer calculé (pour les entreprises)

### Modèle `contrat.contrat`

**Champs principaux :**
- `type_contrat` : Selection (alternance, stage)
- `date_started` : Date de début (obligatoire)
- `date_ended` : Date de fin (obligatoire)
- `personne_etudiant_id` : Many2one vers res.partner (type_profil='etudiant')
- `entreprise_id` : Many2one vers res.partner (is_company=True)
- `personne_tuteur_id` : Many2one vers res.partner (type_profil='salarie')

**Champs calculés :**
- `display_name` : "TYPE - Étudiant @ Entreprise"
- `duree_jours` : Nombre de jours entre début et fin
- `formation_id` : Formation de l'étudiant (auto-rempli)

## ✅ Validations métier

### Contrainte `_check_dates`
```python
date_ended > date_started
```
La date de fin doit être strictement postérieure à la date de début.

### Contrainte `_check_tuteur_entreprise`
```python
personne_tuteur_id.employer_partner_id == entreprise_id
```
Le tuteur doit être un salarié de l'entreprise d'accueil du contrat.

## 🎨 Extensions de vues

### Vue Étudiant
- Onglet "Contrats" avec la liste des contrats de l'étudiant

### Vue Salarié
- Onglet "Contrats de Tutorat" avec les contrats encadrés

### Vue Entreprise
- Champ `contrat_count` dans les vues tree et form
- Onglet "Contrats" avec tous les contrats de l'entreprise

## 📦 Installation

1. **Prérequis obligatoires** :
   - Module `gestion_ecole` installé
   - Module `gestion_entreprise` installé
2. Placer le module dans le dossier addons
3. Redémarrer Odoo : `sudo systemctl restart odoo`
4. Installer "Gestion Contrat"

## 🔗 Dépendances

- `base` (module natif Odoo)
- `gestion_ecole` (module personnalisé)
- `gestion_entreprise` (module personnalisé)

## 📊 Utilisation

1. Créer un étudiant dans "Gestion École → Étudiants"
2. Créer une entreprise dans "Gestion Entreprise → Contacts Entreprise"
3. Créer un salarié (tuteur) rattaché à cette entreprise
4. Créer un contrat dans "Gestion Contrat → Tous les Contrats"
5. Le système vérifiera automatiquement la cohérence des données

## 👨‍💻 Auteur

MoonDev - 2025
