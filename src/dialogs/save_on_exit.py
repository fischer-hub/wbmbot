from PyQt5.QtWidgets import QMessageBox, QCheckBox


class SaveOnExit:
    def __init__(self):
        
        self.cb = QCheckBox()
        self.cb.setText("Don't show this again.")

        self.msgBox = QMessageBox()
        self.msgBox.setText("The current configuration has been modified but not saved!")
        self.msgBox.setWindowTitle("Save current configuration?")
        self.msgBox.setCheckBox(self.cb)
        self.msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        self.msgBox.setDefaultButton(QMessageBox.Save)

    
    def exec(self):
        self.cb.isChecked()
        return self.msgBox.exec(), self.cb.isChecked()
