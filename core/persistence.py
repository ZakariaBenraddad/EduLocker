# core/persistence.py
"""
Module de gestion de la persistance pour EduLocker (version contrôlée)
Cible principalement Windows pour les démonstrations classiques.
"""

import os
import sys
import platform
import subprocess
import logging

# Pour la gestion du registre Windows
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        # Cela peut arriver si on est sur Windows mais que pywin32 n'est pas installé
        # Bien que pour les opérations de registre, winreg soit standard.
        # Pour l'instant, on loggue et on continue, les fonctions Windows échoueront gracieusement.
        logging.getLogger(__name__).error(
            "Module 'winreg' non trouvé. Les opérations de registre Windows échoueront."
            "Assurez-vous d'être sur Windows et que l'installation Python est correcte."
        )
        winreg = None # Pour éviter des NameError plus tard

class PersistenceManager:
    """Gère l'ajout et la suppression de la persistance."""

    def __init__(self, config, logger):
        self.config = config.get('persistence_config', {})
        self.logger = logger.getChild('PersistenceManager') # Utiliser getChild pour hiérarchie
        
        self.persistence_name = self.config.get('name', 'EduLockerUpdate')
        self.description = self.config.get('description', 'Educational Locker Service')
        
        # Déterminer le chemin de l'exécutable/script à rendre persistant
        if getattr(sys, 'frozen', False): # Si le script est "gelé" (compilé en .exe)
            self.executable_path = sys.executable
        else: # Sinon, c'est le script Python lui-même
            # Construire la commande pour exécuter le script python avec l'argument --locked-startup
            # Les guillemets sont importants pour les chemins avec des espaces.
            python_exe_path = sys.executable
            script_path = os.path.abspath(sys.argv[0]) # Chemin absolu du script principal (main.py)
            self.executable_path = f'python "{script_path}" --locked-startup'

        self.logger.info(f"Gestionnaire de persistance initialisé pour '{self.persistence_name}'")
        self.logger.info(f"Chemin pour persistance : {self.executable_path}")

    def _is_windows(self):
        """Vérifie si le système est Windows."""
        return platform.system() == "Windows"

    # --- Persistance via Clé de Registre (Windows) ---
    def add_registry_run_key(self):
        """Ajoute une clé de registre pour démarrer au lancement de session Windows."""
        if not self._is_windows() or not winreg:
            self.logger.warning("Persistance par registre non applicable ou winreg non disponible.")
            return False

        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            # Ouvre la clé avec permission d'écriture. Crée la clé si elle n'existe pas (bien que 'Run' existe toujours).
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.persistence_name, 0, winreg.REG_SZ, self.executable_path)
            self.logger.info(f"Clé de registre '{self.persistence_name}' ajoutée avec succès dans HKCU\\Run.")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout de la clé de registre : {e}", exc_info=True)
            return False

    def remove_registry_run_key(self):
        """Supprime la clé de registre."""
        if not self._is_windows() or not winreg:
            self.logger.warning("Persistance par registre non applicable ou winreg non disponible.")
            return False
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, self.persistence_name)
            self.logger.info(f"Clé de registre '{self.persistence_name}' supprimée avec succès de HKCU\\Run.")
            return True
        except FileNotFoundError:
            self.logger.info(f"Clé de registre '{self.persistence_name}' non trouvée (déjà supprimée ?).")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression de la clé de registre : {e}", exc_info=True)
            return False

    def check_registry_run_key(self):
        """Vérifie si la clé de registre existe."""
        if not self._is_windows() or not winreg:
            return False
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
                # Essayer de lire la valeur. Si elle n'existe pas, FileNotFoundError est levée.
                winreg.QueryValueEx(key, self.persistence_name)
            self.logger.debug(f"Clé de registre '{self.persistence_name}' trouvée.")
            return True
        except FileNotFoundError:
            self.logger.debug(f"Clé de registre '{self.persistence_name}' non trouvée.")
            return False
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de la clé de registre : {e}", exc_info=True)
            return False

    # --- Persistance via Tâche Planifiée (Windows) ---
    def create_scheduled_task(self):
        """Crée une tâche planifiée pour démarrer au lancement de session Windows."""
        if not self._is_windows():
            self.logger.warning("Persistance par tâche planifiée non applicable sur ce SE.")
            return False
        try:
            # Utilisation de f-strings pour construire la commande TR (Task Run)
            # Assurez-vous que self.executable_path est correctement formaté avec des guillemets si nécessaire
            # La commande schtasks est sensible aux guillemets pour les chemins.
            # Notre self.executable_path est déjà formaté avec des guillemets autour des chemins.
            command = [
                "schtasks", "/Create", "/TN", f'"{self.persistence_name}"', # Nom de la tâche entre guillemets
                "/TR", self.executable_path, # Déjà formaté avec guillemets
                "/SC", "ONLOGON", "/RL", "HIGHEST", "/F"
            ]
            self.logger.debug(f"Commande de création de tâche : {' '.join(command)}")
            # Utiliser shell=True sous Windows pour que schtasks soit trouvé, mais attention à l'injection si les noms venaient de l'extérieur.
            # Ici, persistence_name vient de la config, donc c'est contrôlé.
            result = subprocess.run(' '.join(command), capture_output=True, text=True, check=False, shell=True)
            
            if result.returncode == 0:
                self.logger.info(f"Tâche planifiée '{self.persistence_name}' créée avec succès.")
                return True
            else:
                self.logger.error(f"Erreur lors de la création de la tâche planifiée (code {result.returncode}): {result.stderr or result.stdout}")
                return False
        except Exception as e:
            self.logger.error(f"Exception lors de la création de la tâche planifiée : {e}", exc_info=True)
            return False

    def remove_scheduled_task(self):
        """Supprime la tâche planifiée."""
        if not self._is_windows():
            self.logger.warning("Persistance par tâche planifiée non applicable sur ce SE.")
            return False
        try:
            command = ["schtasks", "/Delete", "/TN", f'"{self.persistence_name}"', "/F"]
            self.logger.debug(f"Commande de suppression de tâche : {' '.join(command)}")
            result = subprocess.run(' '.join(command), capture_output=True, text=True, check=False, shell=True)
            
            if result.returncode == 0:
                self.logger.info(f"Tâche planifiée '{self.persistence_name}' supprimée avec succès.")
                return True
            # Vérifier si l'erreur est que la tâche n'a pas été trouvée
            elif "ERROR: The specified task name was not found" in (result.stderr + result.stdout) or \
                 "ERREUR: Le nom de tâche spécifié est introuvable" in (result.stderr + result.stdout): # Pour Windows en français
                self.logger.info(f"Tâche planifiée '{self.persistence_name}' non trouvée (déjà supprimée ?).")
                return True
            else:
                self.logger.error(f"Erreur lors de la suppression de la tâche planifiée (code {result.returncode}): {result.stderr or result.stdout}")
                return False
        except Exception as e:
            self.logger.error(f"Exception lors de la suppression de la tâche planifiée : {e}", exc_info=True)
            return False

    def check_scheduled_task(self):
        """Vérifie si la tâche planifiée existe."""
        if not self._is_windows():
            return False
        try:
            command = ["schtasks", "/Query", "/TN", f'"{self.persistence_name}"']
            # Pour schtasks /Query, il est préférable de ne pas utiliser shell=True si possible,
            # mais pour la cohérence avec create/delete et la gestion des guillemets, on peut le garder.
            result = subprocess.run(' '.join(command), capture_output=True, text=True, check=False, shell=True)

            if result.returncode == 0 and self.persistence_name in result.stdout:
                self.logger.debug(f"Tâche planifiée '{self.persistence_name}' trouvée.")
                return True
            else:
                self.logger.debug(f"Tâche planifiée '{self.persistence_name}' non trouvée (code {result.returncode}).")
                return False
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de la tâche planifiée : {e}", exc_info=True)
            return False

    # --- Méthodes de gestion globale ---
    def apply_all_persistence_methods(self):
        """Applique toutes les méthodes de persistance configurées."""
        self.logger.info("Application des méthodes de persistance...")
        applied_successfully = True
        
        if self.config.get('use_registry_run_key', False): # Vérifier la config
            if not self.add_registry_run_key():
                applied_successfully = False
        else:
            self.logger.info("Persistance par clé de registre désactivée dans la configuration.")
            
        if self.config.get('use_scheduled_task', False): # Vérifier la config
            if not self.create_scheduled_task():
                applied_successfully = False
        else:
            self.logger.info("Persistance par tâche planifiée désactivée dans la configuration.")
        
        if applied_successfully:
            self.logger.info("Toutes les méthodes de persistance activées ont été appliquées (ou tentées).")
        else:
            self.logger.warning("Au moins une méthode de persistance a échoué ou n'a pas été appliquée.")
        return applied_successfully # Retourne True si tout s'est bien passé pour les méthodes activées

    def clear_all_persistence_methods(self):
        """Supprime toutes les méthodes de persistance configurées."""
        self.logger.info("Suppression des méthodes de persistance...")
        cleared_successfully = True

        if self.config.get('use_registry_run_key', False):
            if not self.remove_registry_run_key():
                cleared_successfully = False
        else:
            self.logger.info("Suppression de la persistance par clé de registre non nécessaire (désactivée).")

        if self.config.get('use_scheduled_task', False):
            if not self.remove_scheduled_task():
                cleared_successfully = False
        else:
            self.logger.info("Suppression de la persistance par tâche planifiée non nécessaire (désactivée).")

        if cleared_successfully:
            self.logger.info("Toutes les méthodes de persistance activées ont été supprimées (ou tentées).")
        else:
            self.logger.warning("Au moins une méthode de suppression de persistance a échoué.")
        return cleared_successfully

    def check_all_persistence_methods(self):
        """Vérifie toutes les méthodes de persistance configurées."""
        self.logger.info("Vérification de l'état de la persistance...")
        status = {}
        
        if self.config.get('use_registry_run_key', False):
            status['registry_run_key_active'] = self.check_registry_run_key()
        else:
            status['registry_run_key_active'] = 'NotConfigured'
            
        if self.config.get('use_scheduled_task', False):
            status['scheduled_task_active'] = self.check_scheduled_task()
        else:
            status['scheduled_task_active'] = 'NotConfigured'
            
        self.logger.info(f"État de la persistance : {status}")
        return status