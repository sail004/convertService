import sys
import json
import os.path
import logging
import constants
import settings
import saverResolver
import loaders
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
import datetime
import requests


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
        self.version = '1.01'
        self.initUI()
        fileName = "settings.json"
        self.appSettings = {}
        if (os.path.exists(fileName)):
            with open(fileName, "r") as read_file:
                self.appSettings = json.load(read_file)

        self.start_button.clicked.connect(self.save_xml)
        self.settingsWindow = settings.Settings(self.appSettings)
        self.test_button.clicked.connect(self.test)
        self.delete_button.clicked.connect(self.delete_all)

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
    
    def initUI(self):
        self.setWindowTitle('Convert service ' + self.version)

    def add_line(self, msg):
        item = QtWidgets.QListWidgetItem()
        item.setText(msg)
        self.logView.addItem(item)

    def delete_all(self):
        self.logger.debug("Evotor api clear all data...")

        self.headers = {'Content-type': 'application/json', 'x-authorization': self.appSettings[constants.apiKey]}
        StoreUuid = self.get_store_uuid()
        self.logger.debug("Got store uuid:"+StoreUuid)
        url = "https://api.evotor.ru/api/v1/inventories/stores/"+StoreUuid+"/products/delete"

        requestResult = requests.post(url, data="[]", headers=self.headers)
        self.logger.debug(requestResult)
    
    def get_store_uuid(self):
        url = 'https://api.evotor.ru/api/v1/inventories/stores/search'
        response = requests.get(url, headers = self.headers)
        StoreUuid = response.json()[0]['uuid']
        return StoreUuid

    def test(self):
        self.logger.debug("Evotor api test...")

        self.headers = {'Accept': 'application/vnd.evotor.v2+json',
                        'Content-type': 'application/vnd.evotor.v2+json', 'x-authorization': self.appSettings[constants.apiKey] 
                        }
        StoreUuid = self.get_store_uuid()
        self.logger.debug("Got store uuid:"+StoreUuid)
        url = "https://api.evotor.ru/api/v1/inventories/stores/"+StoreUuid+"/products"

        requestResult = requests.get(url, headers=self.headers)
        self.logger.debug(requestResult.text)

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
            dataLoader = loaders.LoaderResolver(self.appSettings, self.logger).GetLoader()
            model = dataLoader.Load()
            saver = saverResolver.SaverResolver(self.appSettings, model, self.logger).GetSaver()
            saver.save()
            self.appSettings[constants.lastExportTime] = str(datetime.datetime.now())
            self.save_settings()
            self.logger.debug('Export finished')
        except Exception as e:
            self.logger.error('%s' % e)  

     
    def save_settings(self):
        with open("settings.json", "w") as read_file:
            json.dump(self.appSettings, read_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())
