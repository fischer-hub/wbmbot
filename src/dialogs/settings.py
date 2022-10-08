from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QCheckBox
from PyQt5.QtCore import Qt


class AdvancedSettings(QDialog):
    interval = pyqtSignal(float)
    latency = pyqtSignal(float)
    cheat_sig = pyqtSignal(bool)

    def __init__(self):
        super().__init__()


        self.setWindowTitle("Advanced settings")

        # Widgets
        interval_input = QDoubleSpinBox()
        interval_input.setMinimum(0.01)
        interval_input.setMaximum(42000)
        interval_input.setSuffix(" min")
        interval_input.setSingleStep(1)
        interval_input.setValue(5)
        interval_input.valueChanged.connect(self.handle_interval_input)

        latency_input = QDoubleSpinBox()
        latency_input.setMinimum(0.01)
        latency_input.setMaximum(42000)
        latency_input.setSuffix(" sec")
        latency_input.setSingleStep(0.1)
        latency_input.setValue(1.5)
        latency_input.valueChanged.connect(self.handle_latency_input)

        self.cheat_input = QCheckBox()
        self.cheat_input.setCheckState(Qt.Unchecked)
        self.cheat_input.stateChanged.connect(self.handle_cheat_input)

        # Layouts
        main = QVBoxLayout()
        interval_label = QHBoxLayout()
        latency_label  = QHBoxLayout()
        cheat_label  = QHBoxLayout()
        cheat_label.addWidget(QLabel('Experimental'))
        cheat_label.addWidget(self.cheat_input)
        latency_label.addWidget(QLabel('Latency wait'))
        latency_label.addWidget(latency_input)
        interval_label.addWidget(QLabel('Interval'))
        interval_label.addWidget(interval_input)
        main.addLayout(interval_label)
        main.addLayout(latency_label)
        main.addLayout(cheat_label)
        self.setLayout(main)


    def handle_interval_input(self, interval):
        self.interval.emit(interval)
    
    def handle_latency_input(self, latency):
        self.latency.emit(latency)

    def handle_cheat_input(self, state):
        self.cheat_sig.emit(True) if state == Qt.Checked else self.cheat_sig.emit(False)