from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QHBoxLayout,QLabel, QDialog

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

        main = QHBoxLayout()
        main.addWidget(QLabel('Interval'))
        main.addWidget(interval_input)
        self.setLayout(main)

    def handle_interval_input(self, interval):
        self.interval.emit(interval)

