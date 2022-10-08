#!/usr/bin/env python3
import sys, os, yaml
from src import ui, worker, utils
from src.user import User
from src.dialogs import save_on_exit, settings, browse_log

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QFileDialog
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread, QTimer, QSettings
from PyQt5.QtGui import QPalette, QColor



class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class Input:
    def __init__(self, text, field):
        self.text = text
        self.field = field


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        # Window own vars
        super(MainWindow, self).__init__()
        self.setWindowTitle("WBMBOT")
        self.setFixedSize(QSize(700, 500))

        # Objects
        self.settings_dlg = settings.AdvancedSettings()
        self.settings_dlg.interval.connect(self.set_interval)
        self.settings_dlg.latency.connect(self.set_latency)

        self.browse_log_dlg   = browse_log.BrowseLog()
        self.browse_log_dlg.set_log.connect(self.set_log)

        self.save_on_exit_dlg = save_on_exit.SaveOnExit()


        #self.load_conf_dlg = load_config.LoadConfig()
        #self.load_conf_dlg.interval.connect(self.handle_load_conf_dlg)
        self.qsettings = QSettings("acab", "wbmbot")

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_user)

        self.gui_user = User()

        # Custom vars
        self.bot_running_bool = False
        self.bot_created = False
        self.bot_stopped = True
        self.input_ls = [''] * 12
        self.test_run = False
        self.interval = 5
        self.latency = 1.5
        self.config_file = self.qsettings.value("config_file_path", 'config.yaml')
        self.log_file_path = self.qsettings.value("log_file_path", 'log.txt')
        self.cb_checked = self.qsettings.value('save_on_exit', False, type=bool)
        self.user_saved = True

        # Setup stuff
        self.setup_bot()

        sys.stdout = Stream(newText=self.onUpdateText)

        ui.setup(self)
        print(f"Loading config file {self.config_file} ..", end='')
        self.update_user(self.config_file)
        self.set_config()


    def set_log(self, log_file_path):
        self.log_file_path = log_file_path
        self.qsettings.setValue("log_file_path", log_file_path)
        print(f"Log file {log_file_path} set.")
    

    def set_config(self):
        self.firstname_input.setText(self.gui_user.first_name)
        self.lastname_input.setText(self.gui_user.last_name)
        self.email_input.setText((',').join(self.gui_user.email))
        if self.gui_user.zip_code: self.zip_code_input.setText(self.gui_user.zip_code)
        if self.gui_user.phone: self.phone_input.setText(self.gui_user.phone)
        if self.gui_user.street: self.street_input.setText(self.gui_user.street)
        if self.gui_user.city: self.city_input.setText(self.gui_user.city)
        if self.gui_user.filter: self.filter_input.setText((',').join(self.gui_user.filter))
        #self.firstname_input.setText("new config")


    def handle_save_log_dlg(self):
        file_name, _ = QFileDialog.getSaveFileName(self,"Save current log to file",f"{os.getcwd()}", "Text Files (*.txt);; Any (*)")
        if file_name.endswith('.yaml') or file_name.endswith('.yml'):
            with open(file_name, 'w') as outfile: # user vars() to create dict of member vars of user
                yaml.dump(vars(self.bot.user), outfile, default_flow_style=False)
            self.user_saved = True
            return True
        else:
            return False


    def handle_load_log_dlg(self):
        log_file, _ = QFileDialog.getOpenFileName(self, "Open log from file", f"{os.getcwd()}", "Text Files (*.txt);; Any (*)")
        
        self.browse_log_dlg.set_text(log_file)
        self.browse_log_dlg.exec()


    def handle_save_conf_dlg(self):
        file_name, _ = QFileDialog.getSaveFileName(self,"Save current configuration to file",f"{os.getcwd()}", "YAML Files (*.yaml *.yml);; Any (*)")
        if file_name.endswith('.yaml') or file_name.endswith('.yml'):
            with open(file_name, 'w') as outfile: # user vars() to create dict of member vars of user
                yaml.dump(vars(self.bot.user), outfile, default_flow_style=False)
            self.user_saved = True
            return True
        else:
            QMessageBox.critical(self, "Save failed.", "Failed to save current configuration to file!", buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)
            return False


    def handle_load_conf_dlg(self):
        self.config_file, _ = QFileDialog.getOpenFileName(self, "Open configuration from file", f"{os.getcwd()}", "YAML Files (*.yaml *.yml);; Any (*)")
        
        # If config is loaded successfully set config file as standard config 
        if self.update_user(self.config_file):
            self.qsettings.setValue("config_file_path", self.config_file)
            self.set_config()


    def handle_open_settings(self):
        self.settings_dlg.exec()
    

    def set_latency(self, latency):
        self.latency = latency
        self.bot.latency = latency


    # maybe set these in self and wait for bot to be in wait part to change them in worker obj?
    def set_interval(self, interval):
        self.interval = interval
        self.bot.interval = interval
    

    # maybe set these in self and wait for bot to be in wait part to change them in worker obj?
    def set_test_run(self, checked):
        self.test_run = checked
        self.bot.test = checked

    
    def update_user(self, config_file = ''):
        add_msg = f"\nCould not load config from file {config_file} because it contains invalid fields."
        new_user = User()
        
        new_user.parse_config_file(config_file) if config_file else new_user.parse_user_input(self.input_ls)
        new_user.merge(self.gui_user)
        user_invalid_msg = new_user.check()

        if user_invalid_msg:            
            print(f"[{utils.date()}] ERROR: {user_invalid_msg}{add_msg if config_file else ''}", end='')
            return False
        else:
            self.gui_user = new_user
            self.bot.user = self.gui_user
            print(f"[{utils.date()}] Config changes saved.", end='')
            self.user_saved = False
            return True
        

    def text_edited(self, text, position):
        self.input_ls[position] = text
        self.timer.start(3000)


    def setup_bot(self):
        # 1 - create Worker and Thread inside the Form
        self.bot = worker.Worker()  # no parent!
        self.thread = QThread()  # no parent!
        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.bot.console_out_sig.connect(self.onUpdateText)
        # 3 - Move the Worker workerect to the Thread workerect
        self.bot.moveToThread(self.thread)
        # 4 - Connect Worker Signals to the Thread slots
        self.bot.finished.connect(self.handle_bot_stopped)
        self.bot.finished.connect(self.thread.quit)
        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.bot.run)


    def handle_bot_stopped(self):
        self.bot_stopped = True
        self.start_bot_btn.setEnabled(True)
        print("Done!", end='')
    

    def handle_start_stop_btn(self):
        if not self.bot.running:
            self.update_user()
            self.thread.start()
            self.start_bot_btn.setText("Stop bot")
            self.start_bot_btn.setStyleSheet("background-color: rgb(222,82,82)")
            self.bot.running = True
            self.bot_stopped = False
        else:
            print("Stopping bot ..", end='')
            self.start_bot_btn.setEnabled(False)
            self.start_bot_btn.setText("Start bot")
            self.start_bot_btn.setStyleSheet("background-color: rgb(128,242,159)")
            self.bot.running = False        
    

    def closeEvent(self, event):
        if not self.user_saved and not self.cb_checked:
            response, self.cb_checked = self.save_on_exit_dlg.exec()
            
            self.qsettings.setValue('save_on_exit', self.cb_checked)

            if response == QMessageBox.Cancel:
                event.ignore()
                return
            elif response == QMessageBox.Save:

                if not self.handle_save_conf_dlg():
                    event.ignore()
                    return

        self.thread.quit
        sys.stdout = sys.__stdout__
        event.accept()


    def onUpdateText(self, text):
        if self.bot.running or self.bot_stopped: 
            self.console_out.append(f"{text.strip()}")
    

    def __del__(self):
        sys.stdout = sys.__stdout__


    def show_wbs_conf_box(self, state):
        if state == Qt.Checked:
            self.input_ls[7] = 'True'
            self.wbs_conf_frame.show() 
        else:
             self.wbs_conf_frame.hide()
             self.input_ls[7] = ''