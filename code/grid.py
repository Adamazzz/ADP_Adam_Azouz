import numpy as np

class Grid:

    def __init__(self, n, m, arr=None):
        self.rows = n
        self.cols = m
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.toTile= n*m
        if arr is not None:
            self.grid= arr
            for i in range(n):
                for j in range(m):
                    if self.grid[i][j] == 1:
                        self.toTile= self.toTile-1

    def get(self, x, y):
        """

        :param x: x coordinate
        :param y: y coordinate
        :return: the value in the cell (x,y)
        """
        return self.grid[x][y]

    def get_dims(self):
        """

        :return: return back a tuple (n,m)
        """
        return self.rows, self.cols

    def get_tilableSpace(self):
        """

        :return: the number of cells that must tiled
        """
        return self.toTile

    def add_obstacle(self, x, y):
        """
        Add an obstacle to the (x,y) grid cell
        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """
        if self.grid[x][y] == 0:
            self.grid[x][y] = 1
            self.toTile = self.toTile - 1

    def add_obstacles(self, list):
        for (x,y) in list:
            self.add_obstacle(x,y)

    def add_row_wall(self, x):
        """

        :param x: add obstacles in all the row
        :return: None
        """
        for e in range(self.cols):
            self.add_obstacle(x,e)

    def add_column_wall(self, y):
        """

        :param y: add obstacles in all the column
        :return: None
        """
        for e in range(self.rows):
            self.add_obstacle(e,y)

    def remove_obstacle(self,x,y):
        if self.grid[x][y]==1:
            self.grid[x][y] = 0
            self.toTile = self.toTile + 1

    def print_grid(self):
        for row in self.grid:
            print(row)