from PyQt5.QtWidgets import QMessageBox


class SaveOnExit:
    def __init__(self):

        self.msgBox = QMessageBox()
        self.msgBox.setText("The current configuration has been modified but not saved!");
        self.msgBox.setInformativeText("Save current configuration?")
        self.msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        self.msgBox.setDefaultButton(QMessageBox.Save)

    
    def exec(self):
        return self.msgBox.exec()
