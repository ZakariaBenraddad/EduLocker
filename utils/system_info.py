# utils/system_info.py
"""
Module de collecte d'informations système pour le POC
"""

import platform
import os
import socket
import uuid
import time
from datetime import datetime

class SystemAnalyzer:
    """Analyseur d'informations système pour le POC"""
    
    def __init__(self):
        self.info = {}
        self.start_time = time.time()
    
    def gather_basic_info(self):
        """Collecte d'informations système de base"""
        try:
            self.info = {
                # Informations système
                'os': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture()[0],
                
                # Informations réseau
                'hostname': socket.gethostname(),
                'ip_address': self._get_local_ip(),
                
                # Identifiants
                'mac_address': self._get_mac_address(),
                'system_uuid': str(uuid.uuid4()),
                
                # Informations temporelles
                'timestamp': datetime.now().isoformat(),
                'timezone': time.tzname[0],
                
                # Informations utilisateur
                'username': os.getenv('USER') or os.getenv('USERNAME'),
                'home_directory': os.path.expanduser('~'),
                
                # Informations Python
                'python_version': platform.python_version(),
                'python_executable': platform.sys.executable,
            }
            
            # Informations spécifiques selon l'OS
            if platform.system() == 'Linux':
                self.info.update(self._get_linux_info())
            elif platform.system() == 'Windows':
                self.info.update(self._get_windows_info())
                
        except Exception as e:
            print(f"Erreur lors de la collecte d'informations : {e}")
            
        return self.info
    
    def _get_local_ip(self):
        """Récupère l'adresse IP locale"""
        try:
            # Connexion temporaire pour obtenir l'IP locale
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _get_mac_address(self):
        """Récupère l'adresse MAC"""
        try:
            mac = uuid.getnode()
            return ':'.join(['{:02x}'.format((mac >> i) & 0xff) 
                           for i in range(0, 8*6, 8)][::-1])
        except:
            return "00:00:00:00:00:00"
    
    def _get_linux_info(self):
        """Informations spécifiques à Linux"""
        linux_info = {}
        
        try:
            # Distribution Linux
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            linux_info['distribution'] = line.split('=')[1].strip().strip('"')
                            break
            
            # Informations sur la session
            linux_info['display'] = os.getenv('DISPLAY', 'N/A')
            linux_info['desktop_session'] = os.getenv('DESKTOP_SESSION', 'N/A')
            linux_info['xdg_session_type'] = os.getenv('XDG_SESSION_TYPE', 'N/A')
            
        except Exception as e:
            linux_info['error'] = str(e)
            
        return linux_info
    
    def _get_windows_info(self):
        """Informations spécifiques à Windows"""
        windows_info = {}
        
        try:
            # Version Windows détaillée
            windows_info['windows_edition'] = platform.win32_edition()
            windows_info['windows_version'] = platform.win32_ver()
            
            # Variables d'environnement Windows
            windows_info['computer_name'] = os.getenv('COMPUTERNAME', 'N/A')
            windows_info['user_domain'] = os.getenv('USERDOMAIN', 'N/A')
            windows_info['program_files'] = os.getenv('PROGRAMFILES', 'N/A')
            
        except Exception as e:
            windows_info['error'] = str(e)
            
        return windows_info
    
    def generate_victim_id(self):
        """Génère un ID unique pour la 'victime' (éducatif)"""
        import hashlib
        
        # Combinaison d'informations pour créer un ID unique
        unique_string = f"{self.info.get('mac_address', '')}-{self.info.get('hostname', '')}-{self.start_time}"
        
        # Hash SHA-256 tronqué
        victim_id = hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()
        
        return f"EDU-{victim_id}"
    
    def is_virtual_environment(self):
        """Détection basique d'environnement virtuel (pour le POC)"""
        vm_indicators = [
            # Processus VM courants
            'vmtoolsd', 'vboxservice', 'vboxtray',
            # Fichiers VM
            '/proc/scsi/scsi',  # Linux
            'C:\\Program Files\\VMware',  # Windows
        ]
        
        # Vérification simple pour le POC
        hostname = self.info.get('hostname', '').lower()
        if any(indicator in hostname for indicator in ['vm', 'virtual', 'vbox']):
            return True
            
        return False
    
    def get_summary(self):
        """Résumé des informations collectées"""
        if not self.info:
            self.gather_basic_info()
            
        summary = {
            'victim_id': self.generate_victim_id(),
            'os_summary': f"{self.info.get('os', 'Unknown')} {self.info.get('os_release', '')}",
            'machine_summary': f"{self.info.get('machine', '')} - {self.info.get('processor', '')}",
            'network_summary': f"{self.info.get('hostname', '')} ({self.info.get('ip_address', '')})",
            'is_vm': self.is_virtual_environment(),
            'timestamp': self.info.get('timestamp', ''),
        }
        
        return summary