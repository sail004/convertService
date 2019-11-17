import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog

class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)


class ConvertService(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.settings_open_button.clicked.connect(self.show_settings)
        self.settingsWindow = Settings()

    def show_settings(self):
        self.settingsWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())  


