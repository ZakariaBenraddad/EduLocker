# persistence.py

## Description
Ce fichier contient le module de gestion de la persistance pour le projet EduLocker. Il implémente différentes méthodes permettant au ransomware éducatif de survivre aux redémarrages du système, illustrant ainsi les techniques utilisées par les logiciels malveillants réels pour maintenir leur présence sur un système compromis.

## Classe principale
### PersistenceManager
Cette classe gère l'ajout et la suppression des mécanismes de persistance.

#### Méthodes principales
- `__init__()`: Initialise le gestionnaire avec la configuration et le logger
- `add_registry_run_key()`: Ajoute une clé de registre pour démarrer au lancement de session Windows
- `remove_registry_run_key()`: Supprime la clé de registre
- `check_registry_run_key()`: Vérifie si la clé de registre existe
- `create_scheduled_task()`: Crée une tâche planifiée pour démarrer au lancement de session Windows
- `remove_scheduled_task()`: Supprime la tâche planifiée
- `check_scheduled_task()`: Vérifie si la tâche planifiée existe
- `apply_all_persistence_methods()`: Applique toutes les méthodes de persistance configurées
- `clear_all_persistence_methods()`: Supprime toutes les méthodes de persistance
- `check_all_persistence_methods()`: Vérifie l'état de toutes les méthodes de persistance

## Mécanismes de persistance implémentés
1. **Clé de registre Run**: Ajoute une entrée dans `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` pour exécuter le programme au démarrage de Windows
2. **Tâche planifiée**: Crée une tâche Windows qui s'exécute à chaque ouverture de session

## Fonctionnalités clés
1. **Multi-méthodes**: Implémente plusieurs techniques de persistance pour augmenter les chances de survie
2. **Compatibilité Windows**: Conçu principalement pour Windows, avec des vérifications de compatibilité
3. **Configuration flexible**: Les méthodes peuvent être activées/désactivées via la configuration
4. **Nettoyage complet**: Capacité à supprimer toutes les traces de persistance
5. **Vérification d'état**: Permet de vérifier quelles méthodes de persistance sont actives

## Intégration avec le projet
Ce module est utilisé par le point d'entrée principal (`main.py`) pour:
1. Installer des mécanismes de persistance lors du premier lancement
2. Nettoyer ces mécanismes lors de la désinstallation ou en cas d'erreur
3. Vérifier l'état de la persistance lors des analyses anti-malware

## Note technique
Le module utilise des fonctionnalités spécifiques à Windows comme:
- Le module `winreg` pour manipuler le registre Windows
- La commande `schtasks` pour gérer les tâches planifiées

Des vérifications sont effectuées pour s'assurer que ces fonctionnalités sont disponibles avant de les utiliser.