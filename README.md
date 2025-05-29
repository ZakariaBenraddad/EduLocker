# EduLocker - Ransomware Éducatif

## ⚠️ AVERTISSEMENT ⚠️

**CE LOGICIEL EST STRICTEMENT ÉDUCATIF**

Ce projet est un POC (Proof of Concept) développé dans le cadre d'un cours de sécurité informatique pour démontrer le fonctionnement d'un ransomware. Il est conçu uniquement à des fins pédagogiques et de sensibilisation.

**NE PAS UTILISER À DES FINS MALVEILLANTES**

## Description

EduLocker est un projet éducatif à double fonction :

1. **Simulation de ransomware** : Verrouille temporairement l'interface utilisateur du système pour démontrer le fonctionnement d'un ransomware. Contrairement à un vrai ransomware, il ne chiffre aucun fichier et n'endommage pas le système.

2. **Outil anti-malware** : Détecte et supprime le ransomware EduLocker, illustrant comment les logiciels de sécurité identifient et neutralisent les menaces.

## Objectifs pédagogiques

### Côté Malware
- Comprendre les mécanismes d'attaque des ransomwares
- Étudier les techniques de verrouillage d'interface utilisateur
- Explorer les méthodes de persistance sur un système

### Côté Anti-Malware
- Apprendre les techniques de détection des logiciels malveillants
- Comprendre les méthodes de suppression et de nettoyage
- Étudier la restauration des systèmes compromis

### Général
- Sensibiliser aux bonnes pratiques de sécurité
- Développer une compréhension complète du cycle attaque/défense

## Prérequis

- Python 3.6 ou supérieur
- Environnement virtuel (VM) isolé pour les tests
- Privilèges administrateur pour certaines fonctionnalités

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/edulocker.git
cd edulocker

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

**IMPORTANT**: Exécutez ce logiciel UNIQUEMENT dans un environnement virtuel isolé.

### Mode Ransomware (éducatif)

```bash
python main.py
```

### Mode Anti-Malware

Le projet inclut également un outil anti-malware pour détecter et supprimer EduLocker:

```bash
# Interface graphique anti-malware
python main.py --antimalware

# Analyse en ligne de commande
python main.py --scan
```

### Codes de déverrouillage

- Code standard: `UNLOCK2024`
- Code d'urgence: `EMERGENCY_EXIT_123`

## Configuration

Le comportement d'EduLocker peut être personnalisé en modifiant le fichier `config/settings.py`.

### Mode agressif

Le mode agressif active des fonctionnalités plus intrusives comme:
- Désactivation du gestionnaire de tâches
- Masquage de la barre des tâches
- Terminaison du processus explorer.exe

**ATTENTION**: Ces fonctionnalités peuvent rendre votre système temporairement inutilisable. Utilisez-les uniquement dans un environnement virtuel.

## Sécurité et précautions

- Créez toujours un snapshot de votre VM avant d'exécuter ce logiciel
- N'exécutez jamais ce code sur un système de production
- Le programme s'auto-déverrouille après 10 minutes par défaut
- Utilisez Ctrl+C pendant le compte à rebours initial pour annuler l'exécution

## Structure du projet

```
edulocker/
├── config/           # Fichiers de configuration
├── core/             # Fonctionnalités principales
├── gui/              # Interface graphique
├── utils/            # Utilitaires
├── tests/            # Tests unitaires
├── main.py           # Point d'entrée
└── README.md         # Documentation
```

## Désinstallation

Pour nettoyer complètement votre système après utilisation:

```bash
python main.py --cleanup
```

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Avertissement légal

L'utilisation de ce logiciel pour des activités illégales est strictement interdite. Les auteurs déclinent toute responsabilité en cas d'utilisation abusive.

## Auteur

IGBYA - Cours de Sécurité Informatique
