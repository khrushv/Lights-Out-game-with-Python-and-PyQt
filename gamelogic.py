import numpy as np
from scipy import ndimage
def lightsoutbase(n):
    """Base of the LightsOut problem of size (n,n)"""
    a = np.eye(n*n)
    a = np.reshape(a, (n*n, n, n))
    a = np.array(list(map(ndimage.binary_dilation, a)))
    return np.reshape(a, (n*n, n*n))
                            
def gaussRowReduction(A):
    countRow = len(A)
    countColumn = len(A[0])
    current_column = 0
    current_row = 0
    while current_column < countColumn and current_row < countRow:
        #find non zero entry in column
        for row in range(current_row, countRow):
            rowPivotEntry = row
            if A[row,current_column] != 0:
                break
        #if not find move on next column
        if A[rowPivotEntry, current_column] != 0:
            A[[rowPivotEntry, current_column]] = A[[current_column, rowPivotEntry]]
            for row in range(countRow):
                if row == current_row:
                    temp = A[current_column, current_column]#Запоминаем PivotEntry
                    for column in range(countColumn):
                        A[row, column] = A[row, column] / temp
                
                    continue
                coef = A[row, current_column] / A[current_column, current_column]
  
                for column in range(countColumn):
                    A[row, column] = A[row, column] - A[current_column, column] * coef                 
        current_column += 1
        current_row += 1
    return A
