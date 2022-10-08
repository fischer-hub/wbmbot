from re import A
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QDialog

class BrowseLog(QDialog):
    set_log = pyqtSignal(str)

    def __init__(self):
        super().__init__()


        self.setWindowTitle("Log file")
        self.display_log = QTextEdit(readOnly=True)
        self.display_log.setLineWrapMode(QTextEdit.NoWrap)

        self.set_log_btn = QPushButton("Set as log")
        self.set_log_btn.clicked.connect(self.handle_set_log)
        self.set_log_btn.clicked.connect(self.close)
        self.cancel_btn  = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        
        main = QVBoxLayout()
        log_lay = QHBoxLayout()
        buttons = QHBoxLayout()
        log_lay.addWidget(self.display_log)
        buttons.addWidget(self.set_log_btn)
        buttons.addWidget(self.cancel_btn)
        main.addLayout(log_lay, 2)
        main.addLayout(buttons, 1)

        self.setLayout(main)

    def set_text(self, log_file_path):

        with open(log_file_path, "r") as log_file:
            log = log_file.read()
            self.log_file_path = log_file_path
        self.display_log.setText(log)


    def handle_set_log(self):
        self.set_log.emit(self.log_file_path)
