import numpy

class Matrix:
    def __init__(self, m, n, matrix=None):
        self.m = m
        self.n = n
        if matrix is None:
            self.matrix = []
            for _ in range(m):
                matrix.append([0 for _ in range(n)])
        else:
            if len(matrix) != m or any(len(row) != n for row in matrix):
                raise ValueError(f'Given matrix is not {m} * {n}')
            self.matrix = matrix


