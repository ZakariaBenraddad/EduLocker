# settings.py

## Description
Ce fichier contient la configuration centrale du projet EduLocker. Il définit tous les paramètres qui contrôlent le comportement du ransomware éducatif et de l'outil anti-malware, permettant une personnalisation facile sans modifier le code source.

## Structure principale
### POC_CONFIG
Un dictionnaire Python qui contient toutes les configurations du projet, organisées en sections thématiques:

#### Sections de configuration
1. **Configurations générales**
   - `debug_mode`: Active/désactive le mode débogage
   - `educational_mode`: Garantit que le programme reste en mode éducatif
   - `vm_detection_bypass`: Contrôle si la détection de VM est contournée

2. **lock_config**
   - Paramètres de l'interface de verrouillage (plein écran, premier plan)
   - Options du mode agressif (désactivation du gestionnaire des tâches, etc.)
   - Gestion du processus explorer.exe
   - Paramètres de monitoring

3. **persistence_config**
   - Configuration des méthodes de persistance
   - Noms et descriptions pour les entrées de registre et tâches planifiées
   - Activation/désactivation des différentes méthodes

4. **evasion_config**
   - Paramètres pour les techniques d'évasion
   - Détection de VM et d'analyse
   - Niveau d'obfuscation

5. **ui_config**
   - Configuration de l'interface utilisateur
   - Couleurs, polices et tailles de texte

6. **safety_config**
   - Paramètres de sécurité pour le POC
   - Codes de déverrouillage et d'urgence
   - Délai d'auto-déverrouillage
   - Limitations de sécurité

7. **system_config**
   - Configuration spécifique au système
   - Vérifications de compatibilité
   - Exigences de privilèges

8. **logging_config**
   - Configuration du système de journalisation
   - Niveaux de log et chemins de fichiers

9. **recovery_config**
   - Configuration des méthodes de récupération d'urgence
   - Intervalles de vérification

## Fonctions
- `validate_config()`: Valide la configuration et affiche des avertissements pour les options dangereuses

## Variables globales
- `RECOMMENDED_ENVIRONMENT`: Définit l'environnement recommandé pour exécuter le projet en toute sécurité

## Intégration avec le projet
Ce fichier est importé par presque tous les autres modules du projet pour accéder aux paramètres de configuration. Il est particulièrement utilisé par:
- `main.py` pour initialiser les composants avec la bonne configuration
- `locker.py` pour configurer le comportement du verrouillage
- `persistence.py` pour déterminer quelles méthodes de persistance utiliser

## Note de sécurité
La configuration par défaut inclut des avertissements pour les options potentiellement dangereuses comme le mode agressif. La fonction `validate_config()` affiche ces avertissements au démarrage pour s'assurer que l'utilisateur est conscient des risques.