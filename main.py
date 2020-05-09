import sys
import json
import os.path
import sqlite3
import constants
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import settings
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog


class ConvertService(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.settings_open_button.clicked.connect(self.show_settings)
        fileName = "settings.json"
        self.appSettings = {}
        if (os.path.exists(fileName)):
            with open(fileName, "r") as read_file:
                self.appSettings = json.load(read_file)

        self.settingsWindow = settings.Settings(self.appSettings)

    def show_settings(self):
        self.settingsWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())
