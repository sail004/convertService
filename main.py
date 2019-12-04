import sys
import json
import os.path
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog



class Settings(QDialog):
    def __init__(self, settings):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.settings = settings
        self.pushButton.clicked.connect(self.run)
        self.db_way.setText(self.settings["dbPath"])
    

    def run(self):
        if (os.path.exists(self.db_way.text())):
            self.settings["dbPath"] = self.db_way.text()
            with open("settings.json", "w") as read_file:
                json.dump(self.settings, read_file)
            self.close()
            con = sqlite3.connect("script.sql")
            cur = con = sqlite3.connect("films.db")
            result = cur.execute(sql_request.text()).fetchall()
            print(result)
        else:
            error_dialog = QtWidgets.QErrorMessage
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
