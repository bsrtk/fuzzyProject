# Opsiyonel, GUI'yi başlatmak için terminalden çalıştırılabilir
from ara_yuz import TasarrufApp
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
win = TasarrufApp()
win.show()
sys.exit(app.exec_())
