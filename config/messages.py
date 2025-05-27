# config/messages.py
"""
Messages pour l'interface utilisateur
"""

RANSOM_MESSAGES = {
    "french": {
        "title": "SYSTÈME VERROUILLÉ",
        "warning": "⚠️ DÉMONSTRATION ÉDUCATIVE ⚠️",
        "description": """
Votre système a été verrouillé dans le cadre d'une démonstration
de sécurité informatique.

Ceci est un EXERCICE ÉDUCATIF. Aucun dommage réel n'a été causé.

Pour déverrouiller le système, entrez le code ci-dessous.
        """,
        "unlock_prompt": "Code de déverrouillage :",
        "unlock_button": "DÉVERROUILLER",
        "attempts_remaining": "Tentatives restantes : {}",
        "invalid_code": "Code incorrect ! Veuillez réessayer.",
        "system_unlocked": "Système déverrouillé avec succès !",
        "emergency_unlock": "Déverrouillage d'urgence activé.",
    },
    
    "english": {
        "title": "SYSTEM LOCKED",
        "warning": "⚠️ EDUCATIONAL DEMONSTRATION ⚠️",
        "description": """
Your system has been locked as part of a cybersecurity demonstration.

This is an EDUCATIONAL EXERCISE. No real damage has been done.

To unlock the system, enter the code below.
        """,
        "unlock_prompt": "Unlock code:",
        "unlock_button": "UNLOCK",
        "attempts_remaining": "Attempts remaining: {}",
        "invalid_code": "Invalid code! Please try again.",
        "system_unlocked": "System unlocked successfully!",
        "emergency_unlock": "Emergency unlock activated.",
    }
}

def get_messages(language="french"):
    """Récupère les messages dans la langue spécifiée"""
    return RANSOM_MESSAGES.get(language, RANSOM_MESSAGES["french"])