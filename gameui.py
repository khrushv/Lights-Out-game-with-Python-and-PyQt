from PyQt5.QtWidgets import (QDesktopWidget, QWidget, QLineEdit, QMainWindow, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QAction)
from PyQt5.QtCore import  pyqtSignal
from light import Light
import gamelogic as gl
import random
from qline import QLineEdit_ 

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
        

    def create_random_field(self):
        for row_of_lights in self.lights:
            for light in row_of_lights:
                if random.random() > 0.5:
                        light.change_color()
                        
    def get_solution(self):
        row_of_grid = []
        for row_of_lights in self.lights:
            for light in row_of_lights:
                row_of_grid.append(light.is_light_lit)
        gl.get_solution(row_of_grid, self.dimension_of_grid)
        
               

                
