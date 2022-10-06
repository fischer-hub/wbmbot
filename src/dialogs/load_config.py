from PyQt5.QtGui import QPalette, QColor, QTextCursor, QKeySequence
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDateEdit, QFrame, QTextEdit,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton,
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QToolBar, QAction, QStatusBar, QWidget, QDialog, QDialogButtonBox
)

class LoadConfig(QDialog):
    interval = pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Load configuration from file")
