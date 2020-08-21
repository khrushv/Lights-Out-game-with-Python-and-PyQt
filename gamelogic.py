import numpy as np
from gf2 import GF2
from scipy import ndimage

GF2array = np.vectorize(GF2)
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
    null_space_dim = 0
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
                    temp = A[current_column, current_column]#Remember PivotEntry
                    for column in range(countColumn):
                        A[row, column] = A[row, column] / temp
                
                    continue
                coef = A[row, current_column] / A[current_column, current_column]
  
                for column in range(countColumn):
                    A[row, column] = A[row, column] - A[current_column, column] * coef
        else:
            null_space_dim = len(A) - current_row
            break
        current_column += 1
        current_row += 1
    return A, null_space_dim

def get_solution(row_grid, dim_grid):
    base = GF2array(lightsoutbase(dim_grid))
    e = GF2array(np.eye(dim_grid**2))
    res_matrix = np.hstack((base,e))
    res_matrix, dim = gaussRowReduction(res_matrix)
    inverse = res_matrix[:,dim_grid**2:]
    basis_of_null_space = []
    sol = np.dot(inverse,row_grid)
    print('Solution for full rank ')
    print(sol.reshape((dim_grid, dim_grid)))
    if dim > 0:
        basis_of_null_space = res_matrix[-dim:,dim_grid**2:]
        print('Solutions with non-zero rank of null space')
        for l in basis_of_null_space:
            print(np.array([x + y for x,y in zip(sol, l)]).reshape((dim_grid, dim_grid)))
    
