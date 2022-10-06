from PyQt5.QtGui import QPalette, QColor, QTextCursor, QKeySequence
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDateEdit, QFrame, QTextEdit,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton,
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QToolBar, QAction, QStatusBar, QWidget, QDialog, QDialogButtonBox
)

class AdvancedSettings(QDialog):
    interval = pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced settings")
        interval_input = QDoubleSpinBox()

        interval_input.setMinimum(0.01)
        interval_input.setMaximum(42000)

        interval_input.setSuffix(" min")
        interval_input.setSingleStep(1)
        interval_input.setValue(5)
        interval_input.valueChanged.connect(self.handle_interval_input)

        #QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        main = QHBoxLayout()
        main.addWidget(QLabel('Interval'))
        main.addWidget(interval_input)
        self.setLayout(main)

    def handle_interval_input(self, interval):
        self.interval.emit(interval)

