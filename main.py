# main.py
#!/usr/bin/env python3
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
from datetime import datetime

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
    import time
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
    if os.geteuid() == 0:  # Root sur Linux
        logger.warning("Exécution en tant que root détectée")
        response = input("Continuer en tant que root ? (y/N): ")
        if response.lower() != 'y':
            logger.info("Arrêt demandé par l'utilisateur")
            sys.exit(0)
    
    # Collecte d'informations système
    analyzer = SystemAnalyzer()
    system_info = analyzer.gather_basic_info()
    
    logger.info(f"Système détecté : {system_info['os']} {system_info['version']}")
    logger.info(f"Architecture : {system_info['machine']}")
    
    return system_info

def main():
    """Point d'entrée principal du POC"""
    try:
        # Configuration du logging
        logger = setup_logging()
        logger.info("=== DÉMARRAGE EDULOCKER POC ===")
        
        # Affichage de l'avertissement
        display_warning()
        
        # Vérification de l'environnement
        system_info = check_environment()
        
        # Confirmation finale
        print("🔒 Prêt à démarrer le POC EduLocker")
        response = input("Confirmer le démarrage ? (y/N): ")
        
        if response.lower() != 'y':
            logger.info("Démarrage annulé par l'utilisateur")
            print("✅ Démarrage annulé. Aucune action effectuée.")
            return
        
        logger.info("Démarrage confirmé par l'utilisateur")
        
        # Initialisation du locker
        logger.info("Initialisation du système de verrouillage...")
        locker = SystemLocker(config=POC_CONFIG, system_info=system_info)
        
        # Démarrage du verrouillage
        logger.info("Démarrage du verrouillage système...")
        locker.start_lock_sequence()
        
        logger.info("=== FIN EDULOCKER POC ===")
        
    except KeyboardInterrupt:
        logger.info("Interruption par l'utilisateur (Ctrl+C)")
        print("\n✅ Arrêt demandé. Aucune action malveillante effectuée.")
        
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        print(f"❌ Erreur : {e}")
        print("Le programme va se terminer de manière sécurisée.")
        
    finally:
        # Nettoyage de sécurité
        print("🧹 Nettoyage en cours...")
        # Ici on s'assurerait que tout est restauré

if __name__ == "__main__":
    main()