from PyQt5.QtCore import  pyqtSignal
from PyQt5.QtWidgets import QLineEdit
class QLineEdit_(QLineEdit):
    
    textEditDone = pyqtSignal(int)
    
    def __init__(self, str = ""):
        super().__init__()
        self.setText(str)
        
    def keyPressEvent(self, event):
        if(event.key() == 16777220):#if enter is clicked
            self.textEditDone.emit(int(self.text()))
        else:
            QLineEdit.keyPressEvent(self, event)
