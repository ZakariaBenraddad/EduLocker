# config/settings.py
# ... (début du fichier existant) ...

POC_CONFIG = {
    # ... (configurations générales et de sécurité POC existantes) ...
    
    "lock_config": {
        "fullscreen": True,
        "topmost": True,         # On va essayer de renforcer ça
        # Options agressives (À N'UTILISER QU'EN VM ISOLÉE ET AVEC PRÉCAUTION)
        "aggressive_mode": False, # Interrupteur général pour les fonctions ci-dessous
        "force_disable_task_manager": False, # Vraie désactivation via registre
        "force_hide_taskbar": False,
        "kill_explorer_on_lock": False, # TRÈS RISQUÉ - À NE PAS ACTIVER LÉGÈREMENT
        "restart_explorer_on_unlock": True, # Important si kill_explorer_on_lock est True
    },

    "persistence_config": {
        # ... (configuration de persistance existante) ...
    },

    "evasion_config": {
        # ... (configuration d'évasion existante) ...
    },
    
    "ui_config": {
        # ... (configuration UI existante) ...
    },
    
    "messages": {
        # ... (messages existants, y compris "unlock_button") ...
    }
}

# ... (fin du fichier) ...