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
from config.messages import get_messages

import platform
import subprocess  # Pour redémarrer explorer.exe
import os  # Pour tuer explorer.exe

if platform.system() == "Windows":
    import ctypes
    import winreg

class SystemLocker:
    def __init__(self, config, system_info):
        self.config = config
        self.system_info = system_info
        self.logger = logging.getLogger('EduLocker.Locker')

        self.is_locked = False
        self.lock_window = None
        self.start_time = None
        self.unlock_attempts = 0

        # Configurations spécifiques
        self.poc_safety_config = config['safety_config']
        self.lock_behavior_config = config['lock_config']  # Nouvelle config
        self.ui_config = config['ui_config']
        self.messages = config['messages']

        self.max_attempts = self.poc_safety_config['max_attempts']
        self.unlock_code = self.poc_safety_config['unlock_code']
        self.emergency_code = self.poc_safety_config['emergency_exit']
        self.timeout_minutes = self.poc_safety_config['timeout_minutes']

        self.logger.info("SystemLocker initialisé avec configuration de comportement de verrouillage.")

    def _is_windows(self):
        return platform.system() == "Windows"

    # --- Fonctions de verrouillage système agressives (Windows) ---
    def _set_task_manager_disabled_state(self, disable: bool):
        if not self._is_windows():
            return
        if not self.lock_behavior_config.get('aggressive_mode', False) or \
           not self.lock_behavior_config.get('force_disable_task_manager', False):
            self.logger.info("Désactivation/Réactivation agressive du Gestionnaire des Tâches non activée.")
            return

        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value = 1 if disable else 0
                winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, value)
            self.logger.info(f"Gestionnaire des Tâches {'désactivé' if disable else 'réactivé'} via registre (HKCU).")
        except Exception as e:
            self.logger.error(f"Erreur lors de la modification de l'état du Gestionnaire des Tâches : {e}")

    def _set_taskbar_visibility(self, show: bool):
        if not self._is_windows():
            return
        if not self.lock_behavior_config.get('aggressive_mode', False) or \
           not self.lock_behavior_config.get('force_hide_taskbar', False):
            self.logger.info("Masquage/Affichage agressif de la barre des tâches non activé.")
            return

        try:
            hwnd_taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            if hwnd_taskbar:
                command = 1 if show else 0  # SW_SHOW ou SW_HIDE
                ctypes.windll.user32.ShowWindow(hwnd_taskbar, command)
                self.logger.info(f"Barre des tâches {'affichée' if show else 'masquée'}.")
            else:
                self.logger.warning("Impossible de trouver le handle de la barre des tâches.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la modification de la visibilité de la barre des tâches : {e}")

    def _manage_explorer_process(self, kill: bool):
        if not self._is_windows():
            return
        if not self.lock_behavior_config.get('aggressive_mode', False) or \
           not self.lock_behavior_config.get('kill_explorer_on_lock', False):
            self.logger.info("Gestion du processus explorer.exe non activée.")
            return

        if kill:
            self.logger.warning("Tentative de terminaison du processus explorer.exe (RISQUÉ !)")
            try:
                result = subprocess.run(
                    ["taskkill", "/F", "/IM", "explorer.exe"],
                    capture_output=True, text=True, check=False, shell=True
                )
                if result.returncode == 0:
                    self.logger.info("explorer.exe terminé avec succès.")
                else:
                    self.logger.error(f"Échec de la terminaison d'explorer.exe: {result.stderr or result.stdout}")
            except Exception as e:
                self.logger.error(f"Exception lors de la terminaison d'explorer.exe : {e}")
        else:
            if self.lock_behavior_config.get('restart_explorer_on_unlock', True):
                self.logger.info("Tentative de redémarrage du processus explorer.exe.")
                try:
                    subprocess.Popen("explorer.exe")
                    self.logger.info("Commande de redémarrage d'explorer.exe envoyée.")
                except Exception as e:
                    self.logger.error(f"Exception lors du redémarrage d'explorer.exe : {e}")

    def start_lock_sequence(self):
        try:
            self.logger.info("Début de la séquence de verrouillage")
            self.start_time = datetime.now()
            self._display_pre_lock_info()

            # --- Actions de verrouillage agressif (avant création UI) ---
            if self.lock_behavior_config.get('aggressive_mode', False):
                self.logger.warning("Mode agressif activé. Application des verrouillages système.")
                self._set_task_manager_disabled_state(disable=True)
                self._set_taskbar_visibility(show=False)
                self._manage_explorer_process(kill=True)
            # --- Fin Actions de verrouillage agressif ---

            self._initiate_lock()
        except Exception as e:
            self.logger.error(f"Erreur dans la séquence de verrouillage : {e}", exc_info=True)
            self._perform_safe_unlock("Erreur au démarrage")

    def _initiate_lock(self):
        self.is_locked = True
        self.logger.info("Verrouillage système activé (interface)")
        self._create_lock_interface()
        self._start_monitoring()
        self._run_lock_interface()

    def _unlock_system(self, reason):
        try:
            self.logger.info(f"Déverrouillage du système - Raison: {reason}")
            if self.lock_behavior_config.get('aggressive_mode', False):
                self.logger.warning("Mode agressif : Annulation des verrouillages système.")
                self._manage_explorer_process(kill=False)
                self._set_taskbar_visibility(show=True)
                self._set_task_manager_disabled_state(disable=False)
            self.is_locked = False
            if self.lock_window:
                self.lock_window.destroy()
            self.logger.info("Système déverrouillé avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors du déverrouillage : {e}", exc_info=True)

    def _perform_safe_unlock(self, reason):
        """Appelé en cas d'erreur pour tenter de tout restaurer."""
        self.logger.critical(f"TENTATIVE DE DÉVERROUILLAGE SÉCURISÉ - Raison: {reason}")
        if self.lock_behavior_config.get('aggressive_mode', False):
            self._manage_explorer_process(kill=False)
            self._set_taskbar_visibility(show=True)
            self._set_task_manager_disabled_state(disable=False)
        self.is_locked = False
        if self.lock_window and self.lock_window.winfo_exists():
            try:
                self.lock_window.destroy()
            except:
                pass
        messagebox.showerror("Erreur Critique EduLocker", f"Une erreur critique est survenue: {reason}\nTentative de restauration du système.")

    def _start_monitoring(self):
        def monitor():
            last_focus_time = time.time()
            while self.is_locked:
                try:
                    if self.start_time and (datetime.now() - self.start_time).total_seconds() > (self.timeout_minutes * 60):
                        self.logger.info("Timeout atteint - Auto-déverrouillage")
                        self._unlock_system("Timeout automatique")
                        break
                    self._update_timer()

                    if self.lock_window and self.lock_window.winfo_exists():
                        if self.lock_behavior_config.get('aggressive_mode', False):
                            if time.time() - last_focus_time > 0.5:
                                self.lock_window.lift()
                                self.lock_window.attributes('-topmost', True)
                                last_focus_time = time.time()
                        else:
                            self.lock_window.lift()
                            if self.config['lock_config']['topmost']:
                                self.lock_window.attributes('-topmost', True)

                    time.sleep(0.1)
                except tk.TclError:
                    self.logger.warning("Erreur TclError dans la boucle de monitoring (fenêtre détruite ?).")
                    break
                except Exception as e:
                    self.logger.error(f"Erreur dans le monitoring : {e}")
                    break

        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        self.logger.info("Monitoring (potentiellement agressif) démarré")

    def _display_pre_lock_info(self):
        """Affiche les informations avant le verrouillage"""
        print("\n" + "=" * 60)
        print("🔒 INFORMATIONS DE VERROUILLAGE")
        print("=" * 60)

        summary = self.system_info
        print(f"Système cible : {summary.get('os', 'Unknown')}")
        print(f"Utilisateur : {summary.get('username', 'Unknown')}")
        print(f"Machine : {summary.get('hostname', 'Unknown')}")
        print(f"Heure de début : {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\n🔓 Code de déverrouillage : {self.unlock_code}")
        print(f"🚨 Code d'urgence : {self.emergency_code}")
        print(f"⏰ Auto-déverrouillage : {self.timeout_minutes} minutes")

        print("\n⚠️  Appuyez sur Ctrl+C maintenant pour annuler")
        print("=" * 60)

        for i in range(3, 0, -1):
            print(f"Verrouillage dans {i}...")
            time.sleep(1)
        print()

    def _create_lock_interface(self):
        """Crée l'interface de verrouillage"""
        self.lock_window = tk.Tk()
        self.lock_window.title("EduLocker - Démonstration Éducative")

        if self.config['lock_config']['fullscreen']:
            self.lock_window.attributes('-fullscreen', True)
        else:
            self.lock_window.geometry("800x600")

        if self.config['lock_config']['topmost']:
            self.lock_window.attributes('-topmost', True)

        self.lock_window.configure(bg=self.ui_config['background_color'])
        self.lock_window.protocol("WM_DELETE_WINDOW", self._on_close_attempt)
        self.lock_window.bind('<Key>', self._on_key_press)
        self.lock_window.focus_set()
        self._build_interface()
        self.logger.info("Interface de verrouillage créée")

    def _build_interface(self):
        """Construit l'interface utilisateur"""
        main_frame = tk.Frame(
            self.lock_window,
            bg=self.ui_config['background_color']
        )
        main_frame.pack(expand=True, fill='both')

        title_label = tk.Label(
            main_frame,
            text=self.messages['title'],
            font=(self.ui_config['font_family'], self.ui_config['title_font_size'], 'bold'),
            fg=self.ui_config['text_color'],
            bg=self.ui_config['background_color']
        )
        title_label.pack(pady=30)

        subtitle_label = tk.Label(
            main_frame,
            text=self.messages['subtitle'],
            font=(self.ui_config['font_family'], 18, 'italic'),
            fg='#FFD700',
            bg=self.ui_config['background_color']
        )
        subtitle_label.pack(pady=10)

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

        unlock_frame = tk.Frame(
            main_frame,
            bg=self.ui_config['background_color']
        )
        unlock_frame.pack(pady=30)

        unlock_instruction = tk.Label(
            unlock_frame,
            text=self.messages['unlock_instruction'],
            font=(self.ui_config['font_family'], 16, 'bold'),
            fg='#00FF00',
            bg=self.ui_config['background_color']
        )
        unlock_instruction.pack(pady=10)

        self.unlock_entry = tk.Entry(
            unlock_frame,
            font=(self.ui_config['font_family'], 16),
            width=25,
            justify='center',
            show='*'
        )
        self.unlock_entry.pack(pady=10)
        self.unlock_entry.bind('<Return>', self._check_unlock_code)
        self.unlock_entry.focus()

        unlock_button = tk.Button(
            unlock_frame,
            text=self.messages['unlock_button'],
            font=(self.ui_config['font_family'], self.ui_config['button_font_size'], 'bold'),
            command=self._check_unlock_code,
            bg='#228B22',
            fg='white',
            width=15,
            height=2
        )
        unlock_button.pack(pady=15)

        debug_frame = tk.Frame(
            main_frame,
            bg=self.ui_config['background_color']
        )
        debug_frame.pack(side='bottom', pady=20)

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

        system_id = f"ID Système: EDU-{hash(str(self.system_info)) % 10000:04d}"
        system_label = tk.Label(
            debug_frame,
            text=system_id,
            font=(self.ui_config['font_family'], 10),
            fg='#808080',
            bg=self.ui_config['background_color']
        )
        system_label.pack()

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

        if entered_code == self.unlock_code:
            self.logger.info("Code de déverrouillage correct")
            self._unlock_system("Code correct")
            return

        if entered_code == self.emergency_code:
            self.logger.warning("Code d'urgence utilisé")
            self._unlock_system("Code d'urgence")
            return

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

        self.unlock_entry.delete(0, tk.END)
        self.unlock_entry.focus()

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
                pass

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
        key = event.keysym
        if key in ['Alt_L', 'Alt_R', 'Control_L', 'Control_R', 'Tab', 'Escape']:
            self.logger.info(f"Tentative de raccourci détectée : {key}")

        blocked_keys = ['Alt_L', 'Alt_R'] if event.state & 0x8 else []
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
