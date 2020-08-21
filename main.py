import sys
from gameui import GameUI
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameUI()
    sys.exit(app.exec_())
