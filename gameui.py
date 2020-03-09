import sys
from PyQt5.QtWidgets import (QDesktopWidget, QWidget, QLineEdit, QMainWindow, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QGridLayout, QSpacerItem, QSizePolicy, QAction)
from PyQt5.QtCore import  pyqtSignal
from gf2 import GF2
from light import Light
import gamelogic as gl
import numpy as np
import random
#from numpy.linalg import inv

class GameUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.settingsMenu = self.menuBar().addMenu('Menu')
        self.create_new_size_field_Action = QAction('Change size of game field')
        self.output_solution_in_console_action = QAction('get solution')
        self.create_random_field_action = QAction('Create random field')
        self.settingsMenu.addAction(self.create_new_size_field_Action)
        self.settingsMenu.addAction(self.output_solution_in_console_action)
        self.settingsMenu.addAction(self.create_random_field_action)
        self.setWindowTitle('Buttons')
        self.edit = QLineEdit_("3")
        self.create_new_size_field_Action.triggered.connect(self.edit.show)
        self.output_solution_in_console_action.triggered.connect(self.get_solution)
        self.create_random_field_action.triggered.connect(self.create_random_field)
        self.edit.textEditDone.connect(self.creatingGameField)
        self.desktopWidget = QDesktopWidget()
        self.lights = []
        self.dimension_of_grid = 4
        self.creatingGameField(self.dimension_of_grid)
        
    def creatingGameField(self, dimension): 
        '''Create a game field size of nXn'''
        self.dimension_of_grid = dimension
        self.lights = []
        self.centralWidget = QWidget(self)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.top_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)#limit button size changes 
        self.bot_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.left_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.right_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.top_spacer, 0, 0)
        self.gridLayout.addItem(self.bot_spacer, dimension + 1, 1)
        self.gridLayout.addItem(self.left_spacer, 1, 0)
        self.gridLayout.addItem(self.right_spacer, 1, dimension + 1)
        self.setCentralWidget(self.centralWidget)
        for row in range(1, dimension + 1):
            self.lights.append([])
            for column in range(1, dimension + 1):
                item = Light(self.centralWidget)
                self.lights[row - 1].append(item)
                self.gridLayout.addWidget(item.button, row, column)
        for row in range(dimension):
            for column in range(dimension):
                self.lights[row][column].button.clicked.connect(self.lights[row][column].change_color)
                if column != 0:
                    self.lights[row][column].button.clicked.connect(self.lights[row][column - 1].change_color)
                    self.lights[row][column - 1].button.clicked.connect(self.lights[row][column].change_color)
                if row != 0:
                    self.lights[row][column].button.clicked.connect(self.lights[row - 1][column].change_color)
                    self.lights[row - 1][column].button.clicked.connect(self.lights[row][column].change_color)
        self.centralWidget.setLayout(self.gridLayout)            
        self.resize(self.centralWidget.minimumSizeHint())     
        self.adjustSize()
        self.show()
        #centerPoint = self.desktopWidget.availableGeometry().center()
        #self.move(centerPoint.x() - (dimension / 2) * 120, centerPoint.y() - (dimension / 2) * 120)
        
    def get_solution(self):
        matrix_of_grid = []
        for row_of_lights in self.lights:
            for light in row_of_lights:
                matrix_of_grid.append(light.is_light_lit)
        base = GF2array(gl.lightsoutbase(self.dimension_of_grid))
        e = GF2array(np.eye(self.dimension_of_grid*self.dimension_of_grid))
        res_matrix = np.hstack((base,e))
        res_matrix, dim = gl.gaussRowReduction(res_matrix)
        print(dim)
        try:
            inverse = res_matrix[:,self.dimension_of_grid*self.dimension_of_grid:]
            basis_of_null_space = []
            sol = np.dot(inverse,matrix_of_grid)
            print('solution',sol)
            if dim > 0:
               basis_of_null_space = res_matrix[-dim:,self.dimension_of_grid*self.dimension_of_grid:]
               print(basis_of_null_space, 'basis_of_null')
               for l in basis_of_null_space:
                    print(np.array([x + y for x,y in zip(sol, l)]).reshape((self.dimension_of_grid,self.dimension_of_grid)))
            #print(basis_of_null_space)
            #print(np.reshape(np.dot(inverse,matrix_of_grid), (self.dimension_of_grid,self.dimension_of_grid)))
        except BaseException:
            print(BaseException)
        
    def create_random_field(self):
        for row_of_lights in self.lights:
            for light in row_of_lights:
                if random.random() > 0.5:
                        light.change_color()
        

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
            
GF2array = np.vectorize(GF2)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameUI()
    sys.exit(app.exec_())

                
