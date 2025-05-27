# config/settings.py
"""
Configuration pour le POC EduLocker
"""

POC_CONFIG = {
    # Configuration générale
    "version": "1.0.0-POC",
    "name": "EduLocker POC",
    "educational_mode": True,
    
    # Configuration du verrouillage
    "lock_config": {
        "fullscreen": True,
        "topmost": True,
        "disable_alt_tab": True,
        "disable_task_manager": False,  # Désactivé en POC pour sécurité
        "hide_taskbar": False,          # Désactivé en POC pour sécurité
    },
    
    # Configuration de sécurité POC
    "safety_config": {
        "unlock_code": "UNLOCK2024",
        "emergency_exit": "EMERGENCY",
        "max_attempts": 5,
        "timeout_minutes": 10,  # Auto-unlock après 10 minutes
        "enable_logging": True,
    },
    
    # Configuration de l'interface
    "ui_config": {
        "background_color": "#8B0000",  # Rouge foncé
        "text_color": "#FFFFFF",        # Blanc
        "font_family": "Arial",
        "title_font_size": 36,
        "message_font_size": 14,
        "button_font_size": 12,
    },
    
    # Messages éducatifs
    "messages": {
        "title": "🔒 SYSTÈME VERROUILLÉ - DÉMONSTRATION ÉDUCATIVE 🔒",
        "subtitle": "Projet de Sécurité Informatique",
        "main_message": """
ATTENTION : Ceci est une démonstration éducative d'un locker-ransomware.

Votre système a été temporairement verrouillé à des fins pédagogiques.
Aucun fichier n'a été chiffré ou endommagé.

Cette démonstration illustre comment un malware peut :
• Verrouiller l'interface utilisateur
• Bloquer l'accès aux applications
• Demander un code de déverrouillage

OBJECTIF ÉDUCATIF :
Comprendre les mécanismes d'attaque pour mieux s'en protéger.
        """,
        "unlock_instruction": "Entrez le code de déverrouillage pour continuer :",
        "unlock_code_hint": "Code éducatif : UNLOCK2024",
        "emergency_hint": "Code d'urgence : EMERGENCY",
    }
}

# Configuration de développement
DEV_CONFIG = {
    "debug_mode": True,
    "show_unlock_code": True,
    "auto_unlock_timer": 600,  # 10 minutes
    "log_level": "DEBUG",
}