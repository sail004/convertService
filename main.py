import sys
import json
import os.path
import sqlite3
import logging
import constants
import settings
import xmlSaver as saver
from PyQt5 import uic,QtWidgets,QtCore
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
                
        self.start_button.clicked.connect(self.save_xml)
        self.settingsWindow = settings.Settings(self.appSettings)
        FORMAT = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=FORMAT,filename="convertService.log", level="DEBUG")
        logger = logging.getLogger('converService')
        logger.debug('Init')
        

    def show_settings(self):
        self.settingsWindow.show()
        
    def save_xml(self):
        xmlSaver = saver.XmlSaver(self.appSettings)
        xmlSaver.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())
