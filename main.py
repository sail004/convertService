import sys
import json
import os.path
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog

class Settings(QDialog):
    def __init__(self, settings):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.settings = settings
        self.pushButton.clicked.connect(self.run)
        self.db_way.setText(self.settings["dbPath"])
<<<<<<< HEAD
    
=======
        self.setModal(True)
>>>>>>> 5b00ee247ba4f1a11d4b71bc0bbdb4c21212c08c

    def run(self):
        if (os.path.exists(self.db_way.text())):
            self.settings["dbPath"] = self.db_way.text()
            with open("settings.json", "w") as read_file:
                json.dump(self.settings, read_file)
            self.close()
            con = sqlite3.connect(self.settings["dbPath"] )
            cur = con.cursor()
            result = cur.execute(self.sql_request.text()).fetchall()
            print(result)
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setModal(True)
            error_dialog.showMessage('Ошибка! Нет такого файла в системе.')
            error_dialog.exec_()

class ConvertService(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.settings_open_button.clicked.connect(self.show_settings)
        fileName = "settings.json"
        self.settings = {}
        if (os.path.exists(fileName)):
            with open(fileName, "r") as read_file:
                self.settings = json.load(read_file)

        self.settingsWindow = Settings(self.settings)

    def show_settings(self):
        self.settingsWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())
