#!/usr/bin/env python3
from os import setuid
from sqlite3 import connect
import sys
from src import ui, worker, utils, settings
from src.user import User


from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDateEdit, QFrame, QTextEdit,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton,
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QToolBar, QAction, QStatusBar, QWidget
)
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread, QTimer
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
        super(MainWindow, self).__init__()

        self.setWindowTitle("WBMBOT")
        self.setFixedSize(QSize(700, 500))
        self.bot_running_bool = False
        self.worker_created = False
        self.bot_stopped = True
        self.input_ls = [''] * 12
        self.gui_user = User()
        self.settings = settings.CustomDialog()
        self.settings.interval.connect(self.set_interval)
        self.test_run = False
        self.interval = 5

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        #timer.connect(timer,QTimer::timeout(),OnTimerDone(...);
        self.timer.timeout.connect(self.update_user)

        self.setup_worker()

        ui.setup(self)

        sys.stdout = Stream(newText=self.onUpdateText)
    
    def handle_open_settings(self):
        self.settings.exec()
        #settings.open(self)
    
    # maybe set these in self and wait for bot to be in wait part to change them in worker obj?
    def set_interval(self, interval):
        self.interval = interval
        self.worker.interval = interval
    
    # maybe set these in self and wait for bot to be in wait part to change them in worker obj?
    def set_test_run(self, checked):
        self.test_run = checked
        self.worker.test = checked

    def update_user(self):
        new_user = User()
        print(self.input_ls)
        new_user.parse_user_input(self.input_ls)
        user_invalid_msg = new_user.check()
        if user_invalid_msg:            
            print(f"[{utils.date()}] ERROR: {user_invalid_msg}")
        else:
            self.gui_user = new_user
            self.worker.user = self.gui_user
        

    def text_edited(self, text, position):
        self.input_ls[position] = text
        self.timer.start(3000)


    def setup_worker(self):
        # 1 - create Worker and Thread inside the Form
        self.worker = worker.Worker()  # no parent!
        self.thread = QThread()  # no parent!
        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.worker.console_out_sig.connect(self.onUpdateText)
        # 3 - Move the Worker workerect to the Thread workerect
        self.worker.moveToThread(self.thread)
        # 4 - Connect Worker Signals to the Thread slots
        self.worker.finished.connect(self.handle_bot_stopped)
        self.worker.finished.connect(self.thread.quit)
        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.worker.run_wbmbot)


    def handle_bot_stopped(self):
        #self.thread.quit
        self.bot_stopped = True
        self.start_bot_btn.setEnabled(True)
        print("Done!")
    

    def handle_start_stop_btn(self):
        if not self.worker.running:
            self.update_user()
            self.thread.start()
            self.start_bot_btn.setText("Stop bot")
            self.start_bot_btn.setStyleSheet("background-color: rgb(222,82,82)")
            self.worker.running = True
            self.bot_stopped = False
        else:
            print("Stopping bot ..")
            self.start_bot_btn.setEnabled(False)
            self.start_bot_btn.setText("Start bot")
            self.start_bot_btn.setStyleSheet("background-color: rgb(128,242,159)")
            self.worker.running = False        
    

    def closeEvent(self, event):
        self.thread.quit
        sys.stdout = sys.__stdout__
        event.accept()


    def onUpdateText(self, text):
        if self.worker.running or self.bot_stopped: 
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
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()