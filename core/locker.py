# core/locker.py
"""
Module de verrouillage système pour le POC EduLocker
Version sécurisée pour démonstration éducative
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import logging
from datetime import datetime, timedelta

class SystemLocker:
    """Système de verrouillage éducatif"""
    
    def __init__(self, config, system_info):
        self.config = config
        self.system_info = system_info
        self.logger = logging.getLogger('EduLocker.Locker')
        
        # État du verrouillage
        self.is_locked = False
        self.lock_window = None
        self.start_time = None
        self.unlock_attempts = 0
        self.max_attempts = config['safety_config']['max_attempts']
        
        # Configuration de sécurité
        self.unlock_code = config['safety_config']['unlock_code']
        self.emergency_code = config['safety_config']['emergency_exit']
        self.timeout_minutes = config['safety_config']['timeout_minutes']
        
        # Interface
        self.ui_config = config['ui_config']
        self.messages = config['messages']
        
        self.logger.info("SystemLocker initialisé")
    
    def start_lock_sequence(self):
        """Démarre la séquence de verrouillage"""
        try:
            self.logger.info("Début de la séquence de verrouillage")
            self.start_time = datetime.now()
            
            # Affichage des informations pré-verrouillage
            self._display_pre_lock_info()
            
            # Démarrage du verrouillage
            self._initiate_lock()
            
        except Exception as e:
            self.logger.error(f"Erreur dans la séquence de verrouillage : {e}")
            raise
    
    def _display_pre_lock_info(self):
        """Affiche les informations avant le verrouillage"""
        print("\n" + "="*60)
        print("🔒 INFORMATIONS DE VERROUILLAGE")
        print("="*60)
        
        summary = self.system_info
        print(f"Système cible : {summary.get('os', 'Unknown')}")
        print(f"Utilisateur : {summary.get('username', 'Unknown')}")
        print(f"Machine : {summary.get('hostname', 'Unknown')}")
        print(f"Heure de début : {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n🔓 Code de déverrouillage : {self.unlock_code}")
        print(f"🚨 Code d'urgence : {self.emergency_code}")
        print(f"⏰ Auto-déverrouillage : {self.timeout_minutes} minutes")
        
        print("\n⚠️  Appuyez sur Ctrl+C maintenant pour annuler")
        print("="*60)
        
        # Délai de sécurité
        for i in range(3, 0, -1):
            print(f"Verrouillage dans {i}...")
            time.sleep(1)
        print()
    
    def _initiate_lock(self):
        """Initie le verrouillage du système"""
        self.is_locked = True
        self.logger.info("Verrouillage système activé")
        
        # Création de l'interface de verrouillage
        self._create_lock_interface()
        
        # Démarrage du monitoring
        self._start_monitoring()
        
        # Démarrage de l'interface
        self._run_lock_interface()
    
    def _create_lock_interface(self):
        """Crée l'interface de verrouillage"""
        self.lock_window = tk.Tk()
        self.lock_window.title("EduLocker - Démonstration Éducative")
        
        # Configuration de la fenêtre
        if self.config['lock_config']['fullscreen']:
            self.lock_window.attributes('-fullscreen', True)
        else:
            self.lock_window.geometry("800x600")
            
        if self.config['lock_config']['topmost']:
            self.lock_window.attributes('-topmost', True)
        
        # Style de la fenêtre
        self.lock_window.configure(bg=self.ui_config['background_color'])
        
        # Désactivation des raccourcis (partiellement pour sécurité)
        self.lock_window.protocol("WM_DELETE_WINDOW", self._on_close_attempt)
        
        # Gestion des événements clavier
        self.lock_window.bind('<Key>', self._on_key_press)
        self.lock_window.focus_set()
        
        # Construction de l'interface
        self._build_interface()
        
        self.logger.info("Interface de verrouillage créée")
    
    def _build_interface(self):
        """Construit l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(
            self.lock_window,
            bg=self.ui_config['background_color']
        )
        main_frame.pack(expand=True, fill='both')
        
        # Titre principal
        title_label = tk.Label(
            main_frame,
            text=self.messages['title'],
            font=(self.ui_config['font_family'], self.ui_config['title_font_size'], 'bold'),
            fg=self.ui_config['text_color'],
            bg=self.ui_config['background_color']
        )
        title_label.pack(pady=30)
        
        # Sous-titre
        subtitle_label = tk.Label(
            main_frame,
            text=self.messages['subtitle'],
            font=(self.ui_config['font_family'], 18, 'italic'),
            fg='#FFD700',  # Or
            bg=self.ui_config['background_color']
        )
        subtitle_label.pack(pady=10)
        
        # Message principal
        message_label = tk.Label(
            main_frame,
            text=self.messages['main_message'],
            font=(self.ui_config['font_family'], self.ui_config['message_font_size']),
            fg=self.ui_config['text_color'],
            bg=self.ui_config['background_color'],
            justify='center',
            wraplength=700
        )
        message_label.pack(pady=20)
        
        # Frame pour le déverrouillage
        unlock_frame = tk.Frame(
            main_frame,
            bg=self.ui_config['background_color']
        )
        unlock_frame.pack(pady=30)
        
        # Instructions de déverrouillage
        unlock_instruction = tk.Label(
            unlock_frame,
            text=self.messages['unlock_instruction'],
            font=(self.ui_config['font_family'], 16, 'bold'),
            fg='#00FF00',  # Vert
            bg=self.ui_config['background_color']
        )
        unlock_instruction.pack(pady=10)
        
        # Zone de saisie
        self.unlock_entry = tk.Entry(
            unlock_frame,
            font=(self.ui_config['font_family'], 16),
            width=25,
            justify='center',
            show='*'  # Masquer la saisie
        )
        self.unlock_entry.pack(pady=10)
        self.unlock_entry.bind('<Return>', self._check_unlock_code)
        self.unlock_entry.focus()
        
        # Bouton de déverrouillage
        unlock_button = tk.Button(
            unlock_frame,
            text=self.messages['unlock_button'],
            font=(self.ui_config['font_family'], self.ui_config['button_font_size'], 'bold'),
            command=self._check_unlock_code,
            bg='#228B22',  # Vert forêt
            fg='white',
            width=15,
            height=2
        )
        unlock_button.pack(pady=15)
        
        # Informations de débogage (POC uniquement)
        debug_frame = tk.Frame(
            main_frame,
            bg=self.ui_config['background_color']
        )
        debug_frame.pack(side='bottom', pady=20)
        
        # Affichage du code (éducatif)
        code_hint = tk.Label(
            debug_frame,
            text=self.messages['unlock_code_hint'],
            font=(self.ui_config['font_family'], 12),
            fg='#FFD700',
            bg=self.ui_config['background_color']
        )
        code_hint.pack()
        
        emergency_hint = tk.Label(
            debug_frame,
            text=self.messages['emergency_hint'],
            font=(self.ui_config['font_family'], 10),
            fg='#FFA500',
            bg=self.ui_config['background_color']
        )
        emergency_hint.pack(pady=5)
        
        # Informations système
        system_id = f"ID Système: EDU-{hash(str(self.system_info)) % 10000:04d}"
        system_label = tk.Label(
            debug_frame,
            text=system_id,
            font=(self.ui_config['font_family'], 10),
            fg='#808080',
            bg=self.ui_config['background_color']
        )
        system_label.pack()
        
        # Timer d'auto-déverrouillage
        self.timer_label = tk.Label(
            debug_frame,
            text="",
            font=(self.ui_config['font_family'], 10),
            fg='#FF6347',
            bg=self.ui_config['background_color']
        )
        self.timer_label.pack(pady=5)
    
    def _check_unlock_code(self, event=None):
        """Vérifie le code de déverrouillage"""
        entered_code = self.unlock_entry.get().strip()
        self.unlock_attempts += 1
        
        self.logger.info(f"Tentative de déverrouillage #{self.unlock_attempts}: {entered_code[:3]}...")
        
        # Vérification du code principal
        if entered_code == self.unlock_code:
            self.logger.info("Code de déverrouillage correct")
            self._unlock_system("Code correct")
            return
        
        # Vérification du code d'urgence
        if entered_code == self.emergency_code:
            self.logger.warning("Code d'urgence utilisé")
            self._unlock_system("Code d'urgence")
            return
        
        # Code incorrect
        self.logger.warning(f"Code incorrect: {entered_code}")
        remaining_attempts = self.max_attempts - self.unlock_attempts
        
        if remaining_attempts > 0:
            messagebox.showerror(
                "Code Incorrect",
                f"Code de déverrouillage incorrect !\n"
                f"Tentatives restantes : {remaining_attempts}\n\n"
                f"Rappel - Code éducatif : {self.unlock_code}"
            )
        else:
            self.logger.warning("Nombre maximum de tentatives atteint")
            messagebox.showwarning(
                "Tentatives Épuisées",
                f"Nombre maximum de tentatives atteint.\n"
                f"Auto-déverrouillage dans {self.timeout_minutes} minutes.\n\n"
                f"Code d'urgence disponible : {self.emergency_code}"
            )
        
        # Effacer la zone de saisie
        self.unlock_entry.delete(0, tk.END)
        self.unlock_entry.focus()
    
    def _unlock_system(self, reason):
        """Déverrouille le système"""
        try:
            self.logger.info(f"Déverrouillage du système - Raison: {reason}")
            
            # Calcul du temps de verrouillage
            if self.start_time:
                lock_duration = datetime.now() - self.start_time
                duration_str = str(lock_duration).split('.')[0]  # Supprimer les microsecondes
            else:
                duration_str = "Inconnu"
            
            # Message de confirmation
            messagebox.showinfo(
                "Système Déverrouillé",
                f"✅ Système déverrouillé avec succès !\n\n"
                f"Raison : {reason}\n"
                f"Durée de verrouillage : {duration_str}\n"
                f"Tentatives : {self.unlock_attempts}\n\n"
                f"Démonstration EduLocker terminée."
            )
            
            # Arrêt du verrouillage
            self.is_locked = False
            
            # Fermeture de l'interface
            if self.lock_window:
                self.lock_window.destroy()
            
            self.logger.info("Système déverrouillé avec succès")
            
        except Exception as e:
            self.logger.error(f"Erreur lors du déverrouillage : {e}")
    
    def _start_monitoring(self):
        """Démarre le monitoring du système"""
        def monitor():
            while self.is_locked:
                try:
                    # Vérification du timeout
                    if self.start_time:
                        elapsed = datetime.now() - self.start_time
                        if elapsed.total_seconds() > (self.timeout_minutes * 60):
                            self.logger.info("Timeout atteint - Auto-déverrouillage")
                            self._unlock_system("Timeout automatique")
                            break
                    
                    # Mise à jour du timer
                    self._update_timer()
                    
                    # Maintien de la fenêtre au premier plan (POC)
                    if self.lock_window and self.lock_window.winfo_exists():
                        self.lock_window.lift()
                        if self.config['lock_config']['topmost']:
                            self.lock_window.attributes('-topmost', True)
                    
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Erreur dans le monitoring : {e}")
                    break
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        self.logger.info("Monitoring démarré")
    
    def _update_timer(self):
        """Met à jour l'affichage du timer"""
        if self.start_time and self.timer_label and self.timer_label.winfo_exists():
            elapsed = datetime.now() - self.start_time
            remaining = timedelta(minutes=self.timeout_minutes) - elapsed
            
            if remaining.total_seconds() > 0:
                minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                timer_text = f"Auto-déverrouillage dans : {minutes:02d}:{seconds:02d}"
            else:
                timer_text = "Auto-déverrouillage imminent..."
            
            try:
                self.timer_label.config(text=timer_text)
            except:
                pass  # Fenêtre fermée
    
    def _on_close_attempt(self):
        """Gestion des tentatives de fermeture"""
        self.logger.warning("Tentative de fermeture de la fenêtre")
        messagebox.showwarning(
            "Accès Refusé",
            "Impossible de fermer cette fenêtre.\n\n"
            "Entrez le code de déverrouillage pour continuer.\n"
            f"Code éducatif : {self.unlock_code}"
        )
        return False
    
    def _on_key_press(self, event):
        """Gestion des événements clavier"""
        key = event.keysym
        
        # Log des tentatives de raccourcis
        if key in ['Alt_L', 'Alt_R', 'Control_L', 'Control_R', 'Tab', 'Escape']:
            self.logger.info(f"Tentative de raccourci détectée : {key}")
        
        # Blocage de certains raccourcis (partiel pour sécurité POC)
        blocked_keys = ['Alt_L', 'Alt_R'] if event.state & 0x8 else []  # Alt+Tab
        
        if key in blocked_keys:
            return "break"
    
    def _run_lock_interface(self):
        """Lance l'interface de verrouillage"""
        try:
            self.logger.info("Démarrage de l'interface de verrouillage")
            self.lock_window.mainloop()
        except Exception as e:
            self.logger.error(f"Erreur dans l'interface : {e}")
        finally:
            self.is_locked = False
            self.logger.info("Interface de verrouillage fermée")