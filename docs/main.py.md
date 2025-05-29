# main.py

## Description
Ce fichier est le point d'entrée principal du projet EduLocker. Il coordonne l'ensemble des fonctionnalités du ransomware éducatif et de l'outil anti-malware, gérant les différents modes d'exécution et assurant une utilisation sécurisée du programme.

## Fonctions principales

### setup_logging()
Configure le système de journalisation pour le projet, créant un fichier de log avec horodatage.

### display_warning()
Affiche un avertissement clair sur la nature éducative du programme et donne un délai pour permettre à l'utilisateur d'annuler l'exécution.

### check_environment()
Vérifie l'environnement d'exécution, collecte des informations système et affiche des avertissements si nécessaire.

### cleanup()
Fonction de nettoyage qui supprime toutes les méthodes de persistance installées par le programme.

### main()
Point d'entrée principal qui gère les différents modes d'exécution:
- Mode normal: Affiche des avertissements, demande confirmation et exécute le verrouillage
- Mode nettoyage (--cleanup): Supprime toutes les méthodes de persistance
- Mode démarrage verrouillé (--locked-startup): Utilisé pour le démarrage automatique
- Mode anti-malware (--antimalware): Lance l'outil anti-malware avec interface graphique
- Mode scan (--scan): Effectue une analyse anti-malware en ligne de commande

## Modes d'exécution
Le programme peut être lancé avec différentes options:
```
python main.py                   # Mode normal (verrouillage)
python main.py --cleanup         # Nettoyage des méthodes de persistance
python main.py --antimalware     # Interface anti-malware
python main.py --scan            # Analyse anti-malware en ligne de commande
python main.py --locked-startup  # Démarrage automatique (usage interne)
```

## Flux d'exécution
1. Analyse des arguments de ligne de commande
2. Configuration du logging
3. Affichage des avertissements (sauf en mode démarrage automatique)
4. Vérification de l'environnement
5. Confirmation utilisateur (sauf en mode démarrage automatique)
6. Exécution du mode sélectionné
7. Nettoyage de sécurité en cas d'erreur

## Mesures de sécurité
- Avertissements multiples avant exécution
- Délai de 5 secondes avec possibilité d'annulation (Ctrl+C)
- Nettoyage automatique en cas d'erreur via le bloc `finally`
- Affichage du code de déverrouillage dans la console
- Confirmation explicite requise avant le verrouillage

## Intégration avec le projet
Ce fichier importe et utilise:
- `core/persistence.py` pour la gestion de la persistance
- `core/anti_malware.py` pour les fonctionnalités anti-malware
- `core/locker.py` pour le verrouillage du système
- `utils/system_info.py` pour l'analyse du système
- `config/settings.py` pour la configuration

## Note éducative
Le fichier inclut de nombreux commentaires et messages explicatifs pour faciliter la compréhension du fonctionnement d'un ransomware, tout en mettant l'accent sur la nature strictement éducative du projet.