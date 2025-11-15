import os
import sys
import shutil
import tempfile
import subprocess
import psutil # Importiamo la nuova libreria
import webbrowser # Importiamo la libreria per aprire il browser
import locale

# Importa i componenti necessari da PyQt6
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtGui import QPainter, QPixmap, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QProgressBar

def resource_path(relative_path):
    """
    Ottiene il percorso assoluto di una risorsa. Funziona sia in sviluppo
    che quando l'app è impacchettata con PyInstaller.
    """
    try:
        # PyInstaller crea una cartella temporanea e salva il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- GESTIONE MULTILINGUA ---

LANGUAGES = {
    "it": {
        "window_title": "PC Facile - Il Tuo Assistente",
        "welcome_label": "Cosa vuoi fare?",
        "clean_button_text": "🧹 Fai Pulizia",
        "clean_button_tooltip": "Svuota il cestino e cancella i file temporanei per liberare spazio.",
        "pictures_button_text": "🖼️ Trova le mie Foto",
        "pictures_button_tooltip": "Apre la cartella dove sono salvate le tue immagini.",
        "documents_button_text": "📄 Trova i miei Documenti",
        "documents_button_tooltip": "Apre la cartella dove sono salvati i tuoi documenti.",
        "security_button_text": "🛡️ Controlla Sicurezza",
        "security_button_tooltip": "Verifica se l'antivirus di Windows è attivo.",
        "info_button_text": "ℹ️ Informazioni del PC",
        "info_button_tooltip": "Mostra informazioni base sul tuo computer (spazio su disco, memoria).",
        "analyzer_button_text": "🔍 Analizza Spazio Disco",
        "analyzer_button_tooltip": "Trova i file più grandi nelle tue cartelle personali.",
        "uninstall_button_text": "🚫 Disinstalla Programmi",
        "uninstall_button_tooltip": "Apre il pannello per rimuovere i programmi installati.",
        "support_button_text": "❤️ Supporta il Progetto",
        "support_button_tooltip": "Se ti piace l'app, considera una piccola donazione!",
        "results_dialog_title": "File più Grandi Trovati",
        "results_dialog_label": "Ecco i file più grandi trovati. Clicca su un file e poi sul pulsante per aprire la sua cartella.",
        "results_dialog_button": "Apri Cartella del File Selezionato",
        "results_dialog_no_selection": "Nessuna selezione",
        "results_dialog_no_selection_text": "Per favore, seleziona un file dalla lista.",
        "confirm_clean_title": "Conferma Pulizia",
        "confirm_clean_text": "Stai per cancellare i file temporanei e la cache dei browser.\n\nNessuna password o dato importante verrà toccato.\n\nSei sicuro di voler continuare?",
        "clean_success_title": "Pulizia Completata",
        "clean_success_text": "Operazione terminata!\n\nHai liberato circa {mb} MB di spazio.",
        "clean_error_title": "Errore",
        "clean_error_text": "Si è verificato un errore durante la pulizia: {e}",
        "unsupported_os_title": "Funzione non supportata",
        "unsupported_os_text": "Questa funzione è disponibile solo su Windows.",
        "defender_active_title": "Sicurezza Attiva",
        "defender_active_text": "✅ Ottime notizie!\n\nL'antivirus di Windows (Defender) è attivo e sta proteggendo il tuo PC.",
        "defender_inactive_title": "Attenzione Sicurezza",
        "defender_inactive_text": "⚠️ Attenzione!\n\nL'antivirus di Windows (Defender) non risulta attivo. Ti consigliamo di attivarlo.",
        "sysinfo_title": "Informazioni del PC",
        "sysinfo_text": "INFORMAZIONI DEL TUO PC:\n\n💾 Spazio su Disco (C:): {free} GB liberi su {total} GB totali\n\n🧠 Memoria (RAM): {ram} GB installati",
        "sysinfo_error_text": "Impossibile recuperare le informazioni di sistema: {e}",
        "analysis_progress_title": "Analisi in corso...",
        "analysis_progress_text": "Sto cercando i file più grandi...",
        "analysis_no_files_title": "Nessun file trovato",
        "analysis_no_files_text": "Non ho trovato file di grandi dimensioni nelle cartelle analizzate.",
        "analysis_error_text": "Si è verificato un errore durante l'analisi: {e}",
        "open_folder_error_text": "Impossibile aprire la cartella: {e}",
    },
    "en": {
        "window_title": "PC Easy - Your Assistant",
        "welcome_label": "What do you want to do?",
        "clean_button_text": "🧹 Clean Up",
        "clean_button_tooltip": "Empty the recycle bin and delete temporary files to free up space.",
        "pictures_button_text": "🖼️ Find my Photos",
        "pictures_button_tooltip": "Opens the folder where your images are saved.",
        "documents_button_text": "📄 Find my Documents",
        "documents_button_tooltip": "Opens the folder where your documents are saved.",
        "security_button_text": "🛡️ Check Security",
        "security_button_tooltip": "Checks if the Windows antivirus is active.",
        "info_button_text": "ℹ️ PC Information",
        "info_button_tooltip": "Shows basic information about your computer (disk space, memory).",
        "analyzer_button_text": "🔍 Analyze Disk Space",
        "analyzer_button_tooltip": "Finds the largest files in your personal folders.",
        "uninstall_button_text": "🚫 Uninstall Programs",
        "uninstall_button_tooltip": "Opens the panel to remove installed software.",
        "support_button_text": "❤️ Support the Project",
        "support_button_tooltip": "If you like this app, consider a small donation!",
        "results_dialog_title": "Largest Files Found",
        "results_dialog_label": "Here are the largest files found. Click on a file and then on the button to open its folder.",
        "results_dialog_button": "Open Selected File's Folder",
        "results_dialog_no_selection": "No selection",
        "results_dialog_no_selection_text": "Please select a file from the list.",
        "confirm_clean_title": "Confirm Cleanup",
        "confirm_clean_text": "You are about to delete temporary files and browser cache.\n\nNo passwords or important data will be touched.\n\nAre you sure you want to continue?",
        "clean_success_title": "Cleanup Complete",
        "clean_success_text": "Operation finished!\n\nYou have freed up approximately {mb} MB of space.",
        "clean_error_title": "Error",
        "clean_error_text": "An error occurred during cleanup: {e}",
        "unsupported_os_title": "Function not supported",
        "unsupported_os_text": "This function is only available on Windows.",
        "defender_active_title": "Security Active",
        "defender_active_text": "✅ Great news!\n\nWindows Defender antivirus is active and protecting your PC.",
        "defender_inactive_title": "Security Warning",
        "defender_inactive_text": "⚠️ Warning!\n\nWindows Defender antivirus is not active. We recommend you enable it.",
        "sysinfo_title": "PC Information",
        "sysinfo_text": "YOUR PC'S INFORMATION:\n\n💾 Disk Space (C:): {free} GB free of {total} GB total\n\n🧠 Memory (RAM): {ram} GB installed",
        "sysinfo_error_text": "Could not retrieve system information: {e}",
        "analysis_progress_title": "Analysis in progress...",
        "analysis_progress_text": "Searching for the largest files...",
        "analysis_no_files_title": "No files found",
        "analysis_no_files_text": "I did not find any large files in the scanned folders.",
        "analysis_error_text": "An error occurred during the analysis: {e}",
        "open_folder_error_text": "Could not open folder: {e}",
    }
}

class ResultsDialog(QDialog):
    """
    Una finestra di dialogo per mostrare una lista di file.
    """
    def __init__(self, file_list, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setMinimumSize(700, 400)
        self.retranslate_ui()

        layout = QVBoxLayout(self)

        # Etichetta di spiegazione
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        # Tabella per i risultati
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setRowCount(len(file_list))
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Non modificabile
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Popola la tabella
        for row, (path, size) in enumerate(file_list):
            filename = os.path.basename(path)
            size_mb = round(size / (1024 * 1024), 1)
            
            self.table.setItem(row, 0, QTableWidgetItem(filename))
            self.table.setItem(row, 1, QTableWidgetItem(f"{size_mb} MB"))
            # Salva il percorso completo come dato associato alla riga
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, path)

        # Adatta la larghezza delle colonne
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        # Pulsante per aprire la cartella
        self.open_folder_button = QPushButton()
        self.open_folder_button.clicked.connect(self.open_selected_file_location)
        layout.addWidget(self.open_folder_button)
        
        self.retranslate_ui()

    def retranslate_ui(self):
        get_string = self.parent_window.get_string
        self.setWindowTitle(get_string("results_dialog_title"))
        self.info_label.setText(get_string("results_dialog_label"))
        self.table.setHorizontalHeaderLabels(["Nome File", "Dimensione"]) # Potremmo tradurre anche questo
        self.open_folder_button.setText(get_string("results_dialog_button"))

    def open_selected_file_location(self):
        selected_items = self.table.selectedItems()
        get_string = self.parent_window.get_string
        if not selected_items:
            QMessageBox.warning(self, get_string("results_dialog_no_selection"), get_string("results_dialog_no_selection_text"))
            return
        
        full_path = selected_items[0].data(Qt.ItemDataRole.UserRole)
        subprocess.run(['explorer', '/select,', full_path])

class Worker(QObject):
    """
    Un "lavoratore" che esegue un compito in un thread separato
    per non bloccare l'interfaccia grafica.
    """
    finished = pyqtSignal(list) # Segnale emesso quando ha finito, con la lista dei file
    progress = pyqtSignal(int)  # Segnale emesso per aggiornare il progresso

    def find_large_files(self, num_files=15):
        """
        Trova i file più grandi nelle cartelle utente, emettendo segnali di progresso.
        """
        files_with_sizes = []
        home_dir = os.path.expanduser('~')
        scan_paths = [
            os.path.join(home_dir, 'Documents'),
            os.path.join(home_dir, 'Downloads'),
            os.path.join(home_dir, 'Desktop'),
            os.path.join(home_dir, 'Pictures'),
            os.path.join(home_dir, 'Videos'),
        ]

        total_dirs = 0
        for path in scan_paths:
            if os.path.isdir(path):
                try:
                    total_dirs += sum([1 for _ in os.walk(path)])
                except PermissionError:
                    continue
        
        current_dir_count = 0
        for path in scan_paths:
            if not os.path.isdir(path): continue
            try:
                for dirpath, _, filenames in os.walk(path):
                    current_dir_count += 1
                    for f in filenames:
                        file_path = os.path.join(dirpath, f)
                        try:
                            if not os.path.islink(file_path):
                                size = os.path.getsize(file_path)
                                files_with_sizes.append((file_path, size))
                        except (FileNotFoundError, PermissionError):
                            continue
                    if total_dirs > 0:
                        progress_percentage = int((current_dir_count / total_dirs) * 100)
                        self.progress.emit(progress_percentage)
            except PermissionError:
                continue
        
        files_with_sizes.sort(key=lambda x: x[1], reverse=True)
        self.finished.emit(files_with_sizes[:num_files])


class PCFacileWindow(QWidget):
    """
    La finestra principale della nostra applicazione "PC Facile".
    """
    def __init__(self):
        super().__init__()
        try:
            # Imposta la locale predefinita del sistema per poterla leggere correttamente
            locale.setlocale(locale.LC_ALL, '')
            # Ottiene la lingua in modo moderno, evitando la funzione deprecata
            lang_code, _ = locale.getlocale()
            if lang_code and lang_code.startswith('it'):
                self.current_lang = "it"
            else:
                self.current_lang = "en"
        except Exception:
            self.current_lang = "it"

        self.init_ui()

    def get_string(self, key):
        return LANGUAGES[self.current_lang].get(key, key)

    def init_ui(self):
        self.setFixedSize(350, 500)

        icon_path = resource_path('app_icon.png')
        self.setWindowIcon(QIcon(icon_path))

        image_path = resource_path('background.png')
        self.background_pixmap = QPixmap(image_path)
        
        button_style = """
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 rgba(0, 150, 255, 120), stop: 1 rgba(0, 40, 100, 150));
                color: white; 
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 5px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 rgba(0, 170, 255, 150), stop: 1 rgba(0, 60, 120, 180));
                border: 1px solid rgba(255, 255, 255, 120);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 rgba(0, 40, 100, 150), stop: 1 rgba(0, 150, 255, 120));
                border: 1px solid rgba(0, 150, 255, 150);
                padding-left: 6px;
                padding-top: 6px;
            }
        """

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        top_layout = QHBoxLayout()
        self.welcome_label = QLabel()
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.welcome_label.font()
        font.setPointSize(16)
        self.welcome_label.setFont(font)
        self.welcome_label.setStyleSheet("""
            background-color: transparent;
            color: #00E5FF;
            font-weight: bold;
        """)
        top_layout.addWidget(self.welcome_label)
        top_layout.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("🇮🇹 Italiano", "it")
        self.lang_combo.addItem("🇬🇧 English", "en")
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        top_layout.addWidget(self.lang_combo)
        self.main_layout.addLayout(top_layout)

        self.clean_button = QPushButton()
        self.pictures_button = QPushButton()
        self.docs_button = QPushButton()
        self.security_button = QPushButton()
        self.info_button = QPushButton()
        self.disk_analyzer_button = QPushButton()
        self.uninstall_button = QPushButton()
        self.support_button = QPushButton()

        buttons = [
            self.clean_button, self.pictures_button, self.docs_button, self.security_button,
            self.info_button, self.disk_analyzer_button, self.uninstall_button
        ]

        for button in buttons:
            font = button.font()
            font.setPointSize(12)
            button.setFont(font)
            button.setStyleSheet(button_style)
            self.main_layout.addWidget(button)

        font = self.support_button.font()
        font.setPointSize(12)
        self.support_button.setFont(font)
        self.support_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f09819, stop: 1 #ff5858);
                color: white;
                border: 1px solid rgba(255, 255, 255, 150);
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.main_layout.addWidget(self.support_button)

        self.clean_button.clicked.connect(self.run_cleaning)
        self.pictures_button.clicked.connect(self.open_pictures_folder)
        self.docs_button.clicked.connect(self.open_documents_folder)
        self.security_button.clicked.connect(self.run_security_check)
        self.info_button.clicked.connect(self.show_system_info)
        self.disk_analyzer_button.clicked.connect(self.run_disk_analyzer)
        self.uninstall_button.clicked.connect(self.open_uninstall_panel)
        self.support_button.clicked.connect(self.open_donation_link)

        if self.current_lang == "en":
            self.lang_combo.setCurrentIndex(1)
        
        self.retranslate_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)
        super().paintEvent(event)

    def change_language(self, index):
        lang_code = self.lang_combo.itemData(index)
        self.current_lang = lang_code
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.get_string("window_title"))
        self.welcome_label.setText(self.get_string("welcome_label"))
        self.clean_button.setText(self.get_string("clean_button_text"))
        self.clean_button.setToolTip(self.get_string("clean_button_tooltip"))
        self.pictures_button.setText(self.get_string("pictures_button_text"))
        self.pictures_button.setToolTip(self.get_string("pictures_button_tooltip"))
        self.docs_button.setText(self.get_string("documents_button_text"))
        self.docs_button.setToolTip(self.get_string("documents_button_tooltip"))
        self.security_button.setText(self.get_string("security_button_text"))
        self.security_button.setToolTip(self.get_string("security_button_tooltip"))
        self.info_button.setText(self.get_string("info_button_text"))
        self.info_button.setToolTip(self.get_string("info_button_tooltip"))
        self.disk_analyzer_button.setText(self.get_string("analyzer_button_text"))
        self.disk_analyzer_button.setToolTip(self.get_string("analyzer_button_tooltip"))
        self.uninstall_button.setText(self.get_string("uninstall_button_text"))
        self.uninstall_button.setToolTip(self.get_string("uninstall_button_tooltip"))
        self.support_button.setText(self.get_string("support_button_text"))
        self.support_button.setToolTip(self.get_string("support_button_tooltip"))

    def run_cleaning(self):
        reply = QMessageBox.question(self, self.get_string("confirm_clean_title"), 
                                     self.get_string("confirm_clean_text"),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                freed_space_mb = self.clean_temporary_folders()
                QMessageBox.information(self, self.get_string("clean_success_title"), 
                                        self.get_string("clean_success_text").format(mb=freed_space_mb))
            except Exception as e:
                QMessageBox.critical(self, self.get_string("clean_error_title"), self.get_string("clean_error_text").format(e=e))

    def open_pictures_folder(self):
        self.open_user_folder("immagini")

    def open_documents_folder(self):
        self.open_user_folder("documenti")

    def run_security_check(self):
        if sys.platform != "win32":
            QMessageBox.warning(self, self.get_string("unsupported_os_title"), self.get_string("unsupported_os_text"))
            return

        is_defender_active = self.check_windows_defender_status()
        if is_defender_active:
            QMessageBox.information(self, self.get_string("defender_active_title"), self.get_string("defender_active_text"))
        else:
            QMessageBox.warning(self, self.get_string("defender_inactive_title"), self.get_string("defender_inactive_text"))

    def show_system_info(self):
        try:
            disk_usage = psutil.disk_usage('C:/')
            total_disk_gb = round(disk_usage.total / (1024**3), 1)
            free_disk_gb = round(disk_usage.free / (1024**3), 1)
            ram = psutil.virtual_memory()
            total_ram_gb = round(ram.total / (1024**3), 1)
            info_message = self.get_string("sysinfo_text").format(free=free_disk_gb, total=total_disk_gb, ram=total_ram_gb)
            QMessageBox.information(self, self.get_string("sysinfo_title"), info_message)
        except Exception as e:
            QMessageBox.critical(self, self.get_string("clean_error_title"), self.get_string("sysinfo_error_text").format(e=e))

    def run_disk_analyzer(self):
        self.progress_dialog = QDialog(self)
        self.progress_dialog.setWindowTitle(self.get_string("analysis_progress_title"))
        progress_layout = QVBoxLayout(self.progress_dialog)
        progress_label = QLabel(self.get_string("analysis_progress_text"))
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        self.progress_dialog.setModal(True)
        self.progress_dialog.show()

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.find_large_files)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.progress.connect(self.set_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def set_progress(self, value):
        self.progress_bar.setValue(value)

    def on_analysis_finished(self, large_files):
        self.progress_dialog.close()
        if not large_files:
            QMessageBox.information(self, self.get_string("analysis_no_files_title"), self.get_string("analysis_no_files_text"))
            return
        results_dialog = ResultsDialog(large_files, self)
        results_dialog.exec()

    def open_uninstall_panel(self):
        if sys.platform != "win32":
            QMessageBox.warning(self, self.get_string("unsupported_os_title"), self.get_string("unsupported_os_text"))
            return
        try:
            subprocess.run(['control', 'appwiz.cpl'])
        except Exception as e:
            QMessageBox.critical(self, self.get_string("clean_error_title"), f'Impossibile aprire il pannello di disinstallazione: {e}')

    def open_donation_link(self):
        url = "https://ko-fi.com/screemerss" 
        webbrowser.open(url)

    def open_user_folder(self, folder_name):
        if sys.platform != "win32":
            QMessageBox.warning(self, self.get_string("unsupported_os_title"), self.get_string("unsupported_os_text"))
            return
        folder_map = {
            "immagini": "shell:My Pictures",
            "documenti": "shell:Personal",
        }
        path_to_open = folder_map.get(folder_name.lower())
        try:
            subprocess.run(['explorer', path_to_open])
        except Exception as e:
            QMessageBox.critical(self, self.get_string("clean_error_title"), self.get_string("open_folder_error_text").format(e=e))

    def clean_temporary_folders(self):
        if sys.platform != "win32":
            return 0
        total_bytes_freed = 0
        dirs_to_clean = [tempfile.gettempdir()]
        home_dir = os.path.expanduser('~')
        browser_caches = {
            "chrome": os.path.join(home_dir, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            "edge": os.path.join(home_dir, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            "firefox_profiles": os.path.join(home_dir, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles')
        }
        if os.path.isdir(browser_caches["chrome"]):
            dirs_to_clean.append(browser_caches["chrome"])
        if os.path.isdir(browser_caches["edge"]):
            dirs_to_clean.append(browser_caches["edge"])
        if os.path.isdir(browser_caches["firefox_profiles"]):
            for profile in os.listdir(browser_caches["firefox_profiles"]):
                firefox_cache = os.path.join(browser_caches["firefox_profiles"], profile, 'cache2')
                if os.path.isdir(firefox_cache):
                    dirs_to_clean.append(firefox_cache)
        for directory in dirs_to_clean:
            if not os.path.isdir(directory):
                continue
            for item_name in os.listdir(directory):
                item_path = os.path.join(directory, item_name)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        file_size = os.path.getsize(item_path)
                        os.unlink(item_path)
                        total_bytes_freed += file_size
                    elif os.path.isdir(item_path):
                        dir_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, _, filenames in os.walk(item_path) for filename in filenames)
                        shutil.rmtree(item_path)
                        total_bytes_freed += dir_size
                except (PermissionError, OSError):
                    continue
        return round(total_bytes_freed / (1024 * 1024), 2)

    def check_windows_defender_status(self):
        if sys.platform != "win32":
            return False
        command = "powershell -Command \"Get-MpComputerStatus | Select-Object -ExpandProperty 'AntispywareEnabled'\""
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=5)
            status = result.stdout.strip().lower()
            return status == 'true'
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"Impossibile controllare lo stato di Defender: {e}")
            return False

# --- Punto di ingresso dell'applicazione ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PCFacileWindow()
    window.show()
    sys.exit(app.exec())
