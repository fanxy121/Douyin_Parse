#-*-coding:utf-8-*-
from PyQt5.QtWidgets import QApplication
from Logic_panel import MainLogic
import sys

class mainWindow(MainLogic):
   pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

