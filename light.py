from PyQt5.QtWidgets import QPushButton, QWidget
class Light(QWidget):
    
  def __init__(self,  parent = None):      
    super().__init__()
    self.button = QPushButton(parent)
    self.is_light_lit = False
    self.change_color()
    
  def change_color(self):
    '''Paints the button in a different color'''
    if self.is_light_lit:
        self.button.setStyleSheet("background-color: gray; height: 120px; width: 120px")
    else: #paint in white
        self.button.setStyleSheet("background-color: white; height: 120px; width: 120px")
    self.is_light_lit = not(self.is_light_lit)
