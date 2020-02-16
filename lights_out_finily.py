import sys
from PyQt5.QtWidgets import (QDesktopWidget, QWidget, QLineEdit, QMainWindow, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QGridLayout, QSpacerItem, QSizePolicy, QAction)
from PyQt5.QtCore import  pyqtSignal
import time
import numpy as np
import scipy
from scipy import ndimage
from numpy.linalg import inv


def lightsoutbase(n):
    """Base of the LightsOut problem of size (n,n)"""
    a = np.eye(n*n)
    a = np.reshape(a, (n*n, n, n))
    a = np.array(list(map(ndimage.binary_dilation, a)))
    #print(np.reshape(a, (n*n, n*n)))
    return np.reshape(a, (n*n, n*n))

class GameUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.settingsMenu = self.menuBar().addMenu('Menu')
        self.createNewGameFieldAction = QAction('Create new game field')
        self.output_solution_in_console_action = QAction('temp')
        self.settingsMenu.addAction(self.createNewGameFieldAction)
        self.settingsMenu.addAction(self.output_solution_in_console_action)
        self.setWindowTitle('Buttons')
        self.edit = QLineEdit_("3")
        self.createNewGameFieldAction.triggered.connect(self.edit.show)
        self.output_solution_in_console_action.triggered.connect(self.get_matrix_of_grid)
        self.edit.textEditDone.connect(self.creatingGameField)
        self.desktopWidget = QDesktopWidget()
        self.lights = []
        self.dimension_of_grid = 2
        self.creatingGameField(self.dimension_of_grid)
        
    def creatingGameField(self, dimension): 
        '''Create a game field size of nXn'''
       # print('Начало')
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
        #print('До цикла')
        #print(self.lights)
        for row in range(1, dimension + 1):#
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
        #print('Work')
        self.show()
        #centerPoint = self.desktopWidget.availableGeometry().center()
        #self.move(centerPoint.x() - (dimension / 2) * 120, centerPoint.y() - (dimension / 2) * 120)
        
    def get_matrix_of_grid(self):
        matrix_of_grid = []
        for row_of_lights in self.lights:
            for light in row_of_lights:
                matrix_of_grid.append(light.is_light_lit)
        #print(matrix_of_grid)
        #return GF2array(matrix_of_grid)
        base = GF2array(lightsoutbase(self.dimension_of_grid))
        print('base delaet')
        #print(base)
        #row_matrix = np.reshape(base, (1,self.dimension_of_grid*self.dimension_of_grid*self.dimension_of_grid*self.dimension_of_grid))
        #row_matrix_gf2 = (list(map(GF2,row_matrix[0])))
        #matrix = [row_matrix_gf2]
        #matrix = np.reshape(matrix, (self.dimension_of_grid*self.dimension_of_grid,self.dimension_of_grid*self.dimension_of_grid))
        e = GF2array(np.eye(self.dimension_of_grid*self.dimension_of_grid))
        print('e delaet')
        #print(e)
        res_matrix = np.hstack((base,e))
        print(res_matrix)
        res_matrix = gaussRowReduction(res_matrix)
        print('gauss')
        #print(res_matrix)
        inverse = res_matrix[:,self.dimension_of_grid*self.dimension_of_grid:]
        print(np.reshape(np.dot(inverse,matrix_of_grid), (self.dimension_of_grid,self.dimension_of_grid)))
                
        
class Light(QWidget):
    
  def __init__(self,  parent = None):      
    super().__init__()
    self.button = QPushButton(parent)
    self.is_light_lit = False
    self.change_color()
    #self.button.setStyleSheet("background-color: white; height: 120px; width: 120px")
    
  def change_color(self):
    '''Paints the button in a different color'''
    #current_color = self.button.palette().button().color().name()
    #if current_color == "#ffffff": #if white - paint in gray
    if self.is_light_lit:
        self.button.setStyleSheet("background-color: gray; height: 120px; width: 120px")
    else: #paint in white
        self.button.setStyleSheet("background-color: white; height: 120px; width: 120px")
    self.is_light_lit = not(self.is_light_lit)
        
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
        

            
def gaussRowReduction(A):
    #print(A)
    countRow = len(A)
    countColumn = len(A[0])
    current_column = 0
    current_row = 0
    #nulldim = 0
    #print(A)
    while current_column < countColumn and current_row < countRow:
        #find non zero entry in column
        for row in range(current_row, countRow):
            rowPivotEntry = row
            #print(row, ' ', current_column)
            if A[row,current_column] != 0:
                break
        #if not find move on next column
        print(A)
        if A[rowPivotEntry, current_column] != 0:
            #current_column += 1
            #current_row += 1
            #nulldim = len(A) - i
        #else:
            #swap rows
            #if rowPivotEntry == 14 and current_column == 16:
              #  A[rowPivotEntry, current_column] = 'F'
              #  print(A)
            #print(rowPivotEntry, 'rowPivotEntry ', current_column, 'current_column')
            #print(A[rowPivotEntry, current_column])
            A[[rowPivotEntry, current_column]] = A[[current_column, rowPivotEntry]]
            #
            #print(A)
            #print(current_column)
            for row in range(countRow):
                if row == current_row:
                    #print(row, 'row')
                    temp = A[current_column, current_column]#Запоминаем PivotEntry
                    for column in range(countColumn):
                        A[row, column] = A[row, column] / temp
                        #print(A[row,column])
                    #print(A)
                    continue
                coef = A[row, current_column] / A[current_column, current_column]
                
                for column in range(countColumn):
                    A[row, column] = A[row, column] - A[current_column, column] * coef
                    
        current_column += 1
        current_row += 1
    #print(A)
    return A


class GF2(object):
    """Galois field GF(2)."""
    
    def __init__(self, a=0):
        self.value = int(a) & 1
    
    def __add__(self, rhs):
        return GF2(self.value + GF2(rhs).value)
    
    def __mul__(self, rhs):
        return GF2(self.value * GF2(rhs).value)
    
    def __sub__(self, rhs):
        return GF2(self.value - GF2(rhs).value)
    
    def __truediv__(self, rhs):
        return GF2(self.value / GF2(rhs).value)
    
    def __repr__(self):
        return str(self.value)
    
    def __eq__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value == rhs.value
        return self.value == rhs
    
    def __le__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value <= rhs.value
        return self.value <= rhs
    
    def __lt__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value < rhs.value
        return self.value < rhs
    
    def __int__(self):
        return self.value
    
    def __long__(self):
        return self.value
#def GF2inv(A):
 #   """Inversion and eigenvectors of the null-space of a GF2 matrix."""
  #  n = len(A)
   # assert n == A.shape[1], "Matrix must be square"
    
    #A = np.hstack([A, np.eye(n)])
    #B = gaussRowReduction(GF2array(A))
    
    #inverse = np.int_(B[-n:, -n:])
    #E = B[:n, :n]
    #null_vectors = []
    #if nulldim > 0:
     #   null_vectors = E[:, -nulldim:]
      #  null_vectors[-nulldim:, :] = GF2array(np.eye(nulldim))
       # null_vectors = np.int_(null_vectors.T)
    
    #return inverse#, null_vectors    
GF2array = np.vectorize(GF2)
    
if __name__ == '__main__':
	print('HIfsdfsdfgdfgfdghdfjfgh')
    app = QApplication(sys.argv)
    ex = GameUI()
    #array = np.array([[0,0,0], [0,0,0]])
    b = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1],])
    m = GF2array(lightsoutbase(4))
    e = GF2array(np.eye(4*4))
    res = np.hstack((m,e))
    res_ = gaussRowReduction(res)
	#changes for git
    #print(np.linalg.inv(b))
    #size_of_matrix = 2
    #base = GF2array(lightsoutbase(3))
    #matrix = base
    #print(matrix)
    #row_matrix = np.reshape(base, (1,9*9))
    #m = []
    #print(row_matrix[0])
    #row_matrix_gf2 = (list(map(GF2,row_matrix[0])))
    #matrix = [row_matrix_gf2]
    #matrix = np.reshape(matrix, (9,9))
    #e = GF2array(np.eye(9))
    #print(type(e[1,0]))
    #res_matrix = np.hstack((matrix,e))
    #print(res_matrix)
	#gbgbjjglgl;sadjl;gadfhkhgadfj;gdajfgbdgla'hdslg;sGds
    #res_matrix = gaussRowReduction(res_matrix)
    #inverse = res_matrix[:,9:]
    #b = GF2array(np.array([1,1,1,1,1,1,1,1,1]))
    #print(ex.get_matrix_of_grid())
    #print(np.dot(inverse,b))
    #print(row_matrix_gf2)
    #m = np.array([[3,4], [5,6]])
    #e = np.eye(2)
    #A = gaussRowReduction(np.hstack((m,e)))
    #inversion = GF2inv(matrix)
    #gaussRowReduction(GF2array(matrix))
    #sys.exit(app.exec_())
