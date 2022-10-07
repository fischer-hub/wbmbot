from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QLabel, QDialog

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

        latency_input = QDoubleSpinBox()

        latency_input.setMinimum(0.01)
        latency_input.setMaximum(42000)

        latency_input.setSuffix(" sec")
        latency_input.setSingleStep(0.1)
        latency_input.setValue(1.5)
        #latency_input.valueChanged.connect(self.handle_interval_input)

        main = QVBoxLayout()
        interval_label = QHBoxLayout()
        latency_label  = QHBoxLayout()
        latency_label.addWidget(QLabel('Latency wait'))
        latency_label.addWidget(latency_input)
        interval_label.addWidget(QLabel('Interval'))
        interval_label.addWidget(interval_input)
        main.addLayout(interval_label)
        main.addLayout(latency_label)
        self.setLayout(main)

    def handle_interval_input(self, interval):
        self.interval.emit(interval)

