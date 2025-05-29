# config/messages.py
"""
Messages pour l'interface utilisateur
"""

RANSOM_MESSAGES = {
	"french": {
		"title": "SYSTÈME VERROUILLÉ",
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
		"unlock_instruction": "Entrez le code de déverrouillage pour continuer :",
		"unlock_code_hint": "Code éducatif : UNLOCK2024",
  "emergency_hint": "Code d'urgence : EMERGENCY_EXIT_123",
	},

	"english": {
		"title": "SYSTEM LOCKED",
		"subtitle": "Cybersecurity project",
  "main_message": """
WARNING: This is an educational demonstration of a locker-ransomware.

Your system has been temporarily locked for educational purposes.
No files have been encrypted or damaged.

This demonstration illustrates how malware can:
• Lock the user interface
• Block access to applications
• Request an unlock code

EDUCATIONAL OBJECTIVE:
Understanding attack mechanisms to better protect against them.
        """,
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
		"unlock_instruction": "Enter the unlock code to continue:",
		"unlock_code_hint": "Educational code: UNLOCK2024",
  "emergency_hint": "Emergency code: EMERGENCY_EXIT_123",
	}
}


def get_messages(language="french"):
	"""Récupère les messages dans la langue spécifiée"""
	return RANSOM_MESSAGES.get(language, RANSOM_MESSAGES["french"])
