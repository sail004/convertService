import sys
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog

class Settings(QDialog):
    def __init__(self, settings):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.settings=settings


class ConvertService(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.settings_open_button.clicked.connect(self.show_settings)
        with open("settings.json", "r") as read_file:
            self.settings = json.load(read_file)
        self.settingsWindow = Settings(self.settings)
        pushButton.clicked.connect.self.run()

    def run(self):
        self.dbname = db_way.text()
        self.settings = dbname
        

    def show_settings(self):
        self.settingsWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())  


