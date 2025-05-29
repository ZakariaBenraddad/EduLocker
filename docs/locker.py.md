# locker.py

## Description
Ce fichier contient le module principal de verrouillage du système pour le projet EduLocker. Il implémente la fonctionnalité de "ransomware" éducatif en créant une interface graphique qui simule un écran de rançon, sans toutefois chiffrer de fichiers ou causer de dommages réels au système.

## Classe principale
### SystemLocker
Cette classe gère l'ensemble du processus de verrouillage de l'écran.

#### Méthodes principales
- `__init__()`: Initialise le locker avec la configuration et les informations système
- `start_lock_sequence()`: Démarre la séquence de verrouillage complète
- `_initiate_lock()`: Initialise le verrouillage de l'interface
- `_create_lock_interface()`: Crée l'interface graphique de verrouillage
- `_build_interface()`: Construit les éléments visuels de l'interface
- `_check_unlock_code()`: Vérifie le code de déverrouillage entré par l'utilisateur
- `_unlock_system()`: Déverrouille le système et restaure les paramètres
- `_perform_safe_unlock()`: Effectue un déverrouillage d'urgence en cas d'erreur

#### Fonctionnalités de verrouillage agressif (Windows uniquement)
- `_set_task_manager_disabled_state()`: Active/désactive le Gestionnaire des tâches
- `_set_taskbar_visibility()`: Affiche/masque la barre des tâches
- `_manage_explorer_process()`: Termine/redémarre le processus explorer.exe

## Fonctionnalités clés
1. **Interface de verrouillage**: Crée une fenêtre plein écran avec des messages menaçants et une demande de rançon
2. **Mode agressif**: Option pour rendre l'interface plus difficile à contourner (désactivation du gestionnaire de tâches, etc.)
3. **Système de déverrouillage**: Accepte un code de déverrouillage et un code d'urgence
4. **Auto-déverrouillage**: Se déverrouille automatiquement après un délai configurable
5. **Monitoring**: Surveille l'état du verrouillage et maintient l'interface au premier plan
6. **Sécurité**: Inclut des mécanismes pour éviter tout dommage réel au système

## Intégration avec le projet
Ce module est appelé par le point d'entrée principal (`main.py`) et utilise:
- Les configurations de `config/settings.py`
- Les messages de `config/messages.py`
- Les informations système de `utils/system_info.py`

## Note de sécurité
Le module inclut plusieurs mesures de sécurité pour éviter tout dommage réel:
- Aucun chiffrement de fichiers n'est effectué
- Auto-déverrouillage après un délai configurable
- Code d'urgence pour déverrouillage immédiat
- Déverrouillage sécurisé en cas d'erreur
- Affichage du code de déverrouillage dans la console avant le verrouillage