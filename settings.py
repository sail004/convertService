import sys
import json
import os.path
import constants
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
        self.refresh(settings)
        self.setModal(True)

    def refresh(self, settings):
        if constants.dbPath in self.settings.keys():
            self.db_way.setText(self.settings[constants.dbPath])
        if constants.HeaderQuery in self.settings.keys():
            self.heading_request.setText(self.settings[constants.HeaderQuery])
        if constants.PositionQuery in self.settings.keys():
            self.position_request.setText(
                self.settings[constants.PositionQuery])
        if constants.UploadDirectory in self.settings.keys():
            self.upload_directory.setText(
                self.settings[constants.UploadDirectory])
        if constants.ExchangePeriod in self.settings.keys():
            self.exchange_period.setText(
                self.settings[constants.lastExportTime])

    def run(self):
        self.settings[constants.dbPath] = self.db_way.text()
        self.settings[constants.HeaderQuery] = self.heading_request.text()
        self.settings[constants.PositionQuery] = self.position_request.text()
        self.settings[constants.UploadDirectory] = self.upload_directory.text()
        self.settings[constants.ExchangePeriod] = self.exchange_period.text()
        self.accept()
        