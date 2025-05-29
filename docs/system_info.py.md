# system_info.py

## Description
Ce fichier contient le module de collecte d'informations système pour le projet EduLocker. Il permet de recueillir des données sur l'environnement d'exécution, ce qui est une étape typique dans les logiciels malveillants pour adapter leur comportement au système cible.

## Classe principale
### SystemAnalyzer
Cette classe est responsable de l'analyse du système et de la collecte d'informations.

#### Méthodes principales
- `gather_basic_info()`: Collecte les informations de base sur le système (OS, version, architecture, etc.)
- `_get_local_ip()`: Récupère l'adresse IP locale de la machine
- `_get_mac_address()`: Obtient l'adresse MAC de l'interface réseau
- `_get_linux_info()`: Collecte des informations spécifiques aux systèmes Linux
- `_get_windows_info()`: Collecte des informations spécifiques aux systèmes Windows
- `generate_victim_id()`: Génère un identifiant unique pour la "victime" (à des fins éducatives)
- `is_virtual_environment()`: Détecte si le programme s'exécute dans un environnement virtuel
- `get_summary()`: Fournit un résumé des informations collectées

## Informations collectées
- Système d'exploitation et version
- Architecture matérielle
- Informations réseau (nom d'hôte, adresse IP)
- Identifiants uniques (adresse MAC, UUID)
- Informations temporelles (timestamp, fuseau horaire)
- Informations utilisateur (nom d'utilisateur, répertoire personnel)
- Version de Python et chemin de l'exécutable
- Informations spécifiques à l'OS (Linux ou Windows)

## Intégration avec le projet
Ce module est utilisé par le composant principal du ransomware (`core/locker.py`) pour:
1. Adapter son comportement en fonction du système d'exploitation
2. Générer un identifiant unique pour la "victime"
3. Détecter si le programme s'exécute dans un environnement virtuel (mesure de sécurité)
4. Afficher des informations système dans les logs et l'interface utilisateur

## Note de sécurité
La collecte d'informations est limitée aux données non sensibles et est utilisée uniquement à des fins éducatives. Dans un ransomware réel, ces informations pourraient être utilisées pour:
- Éviter la détection (en identifiant les environnements d'analyse)
- Personnaliser l'attaque selon le système cible
- Communiquer avec un serveur de commande et contrôle