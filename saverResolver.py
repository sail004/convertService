import xmlSaver
import evotorSaver
import constants

class SaverResolver:
    def __init__(self, settings, model, logger):
        self.settings = settings
        self.model = model
        self.logger = logger

    def GetSaver(self):
        if (self.settings[constants.ExchangeType] == 0):
            return evotorSaver.EvotorSaver(self.settings, self.model, self.logger)
        if (self.settings[constants.ExchangeType] == 1):
            return xmlSaver.XmlSaver(self.settings, self.model, self.logger)
        if (self.settings[constants.ExchangeType] == 2):
            return evotorSaver.EvotorSaver(self.settings, self.model, self.logger)
        return xmlSaver.XmlSaver(self.settings, self.model, self.logger)