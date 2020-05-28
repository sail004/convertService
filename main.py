import sys
import json
import os.path
import logging
import constants
import settings
import xmlSaver as saver
import loaders
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
import datetime

class LogHandler(logging.Handler):
    def __init__(self, func, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.func = func

    def handle(self, record):
        logging.Handler.handle
        self.func(self.format(record))


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
        logging.basicConfig(
            format=FORMAT, filename="convertService.log", level="DEBUG")
        baseLogger = logging.getLogger('convertService')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        baseLogger.addHandler(handler)
        logHandler = LogHandler(self.add_line)
        logHandler.setFormatter(formatter)
        baseLogger.addHandler(logHandler)
        self.logger = baseLogger
        self.logger.debug('Init')

    def add_line(self, msg):
        item = QtWidgets.QListWidgetItem()
        item.setText(msg)
        self.logView.addItem(item)

    def show_settings(self):
        self.settingsWindow.refresh(self.appSettings)
        result = self.settingsWindow.exec()
        if (result):
            self.save_settings()
        
        
    def testClose(self, events):
        self.logger.debug('close')

    def save_xml(self):
        self.logger.debug('Export started')

        try:
            dataLoader = loaders.SampleLoader(self.appSettings, self.logger)
            model = dataLoader.Load()
            xmlSaver = saver.XmlSaver(self.appSettings, model, self.logger)
            xmlSaver.save()
            self.appSettings[constants.lastExportTime] = str(datetime.datetime.now())
            self.save_settings()
            self.logger.debug('Export finished')
        except IOError as e:
            self.logger.error('%s' % e)  

     
    def save_settings(self):
        with open("settings.json", "w") as read_file:
            json.dump(self.appSettings, read_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())
