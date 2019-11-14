import sys
from PyQt5.QtWidgets import QApplication, QWidget

 
class ConvertService(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Конверт Сервис')    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConvertService()
    ex.show()
    sys.exit(app.exec())  