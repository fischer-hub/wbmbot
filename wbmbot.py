#!/usr/bin/env python3
from os import setuid
import sys
from src import ui, worker

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDateEdit, QFrame, QTextEdit,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton,
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QToolBar, QAction, QStatusBar, QWidget
)
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QPalette, QColor, QTextCursor

class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

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

        # 1 - create Worker and Thread inside the Form
        self.worker = worker.Worker()  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.worker.console_out_sig.connect(self.onUpdateText)

        # 3 - Move the Worker workerect to the Thread workerect
        self.worker.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.worker.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.worker.run_wbmbot)

        # * - Thread finished signal will close the app if you want!
        #self.thread.finished.connect(app.exit)

        # 6 - Start the thread
        #self.thread.start()


        ui.setup(self)

        sys.stdout = Stream(newText=self.onUpdateText)
    
    def handle_start_stop_btn(self):
        if not self.bot_running_bool:
            self.thread.start()
            self.start_bot_btn.setText("Stop bot")
            self.start_bot_btn.setStyleSheet("background-color: rgb(222,82,82)")
            self.bot_running_bool = True
        else:
            self.thread.quit()
            self.start_bot_btn.setText("Start bot")
            self.start_bot_btn.setStyleSheet("background-color: rgb(128,242,159)")
            self.bot_running_bool = False
    
    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        event.accept()


    def onUpdateText(self, text):
        #self.console_out.append(text.strip())
        self.console_out.append(f"{text.strip()}")

    
    def __del__(self):
        sys.stdout = sys.__stdout__

    def show_wbs_conf_box(self, state):
        print("checkbox clicked")
        self.wbs_conf_frame.show() if state == Qt.Checked else self.wbs_conf_frame.hide()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()