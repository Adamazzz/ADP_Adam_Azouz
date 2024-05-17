import grid
import graph
import random

def grid_to_graph(grd):
    """
    converts a grid to a graph
    :param grid: Grid
    :return: Graph
        a graph representing the layout
    """
    n,m= grd.get_dims()
    size= n*m
    g= graph.Graph(size+2)
    source=size
    sink=size+1
    for i in range(n):
        for j in range(m):
            if grd.get(i,j)==0:
                if(i%2==j%2):
                    g.add_edge(i*m+j,sink,1)
                else:
                    g.add_edge(source, i*m+j,1)
                    if(i-1>=0):
                        g.add_edge(i*m+j,(i-1)*m+j,1)
                    if(i+1<n):
                        g.add_edge(i*m+j,(i+1)*m+j,1)
                    if(j+1<m):
                        g.add_edge(i*m+j,i*m+j+1,1)
                    if(j-1>=0):
                        g.add_edge(i*m+j,i*m+j-1,1)

    return g

def is_tilable(grd):
    """
    Given a grid grd, outputs whether the layout is tilable with a 2:1 tiles or not.
    :param grd: Grid
    :return: boolean
    """
    graph= grid_to_graph(grd)
    to_cover= grd.get_tilableSpace()
    src= graph.get_numVertices()-2
    dst=  graph.get_numVertices()-1

    if(to_cover%2==1):
        return False

    flow= graph.FordFulkerson(src,dst)
    if(flow==(to_cover/2)):
        return True

    return False

def randomObstacles_grid(n,m,p):
    """
    constructs a grid of size n*m, with an obstable present with probability p in each cell
    :param n: int
        first dimension of the grid
    :param m: int
        second dimension of the grid
    :param p: float
        probability of obstacle existence. Required: 0<=p<1
    :return: Grid
        a randomely genrated Grid
    """
    arr = []
    for _ in range(n):
        row = []
        for _ in range(m):
            rand_num = random.random()
            cell_value = 1 if rand_num < p else 0
            row.append(cell_value)
        arr.append(row)

    return grid.Grid(n,m,arr)

def randomWalls_grid(n,m,p):
    """
    constructs a grid of size n*m, with an wall present with probability p for each row or column
        :param n: int
            first dimension of the grid
        :param m: int
            second dimension of the grid
        :param p: float
            probability of wall existence. Required: 0<=p<1
        :return: Grid
            a randomely genrated Grid
    """

    grd= grid.Grid(n,m)
    for x in range(n):
        rand_num = random.random()
        is_wall= 1 if rand_num < p else 0
        if(is_wall==1):
            grd.add_row_wall(x)
    for y in range(m):
        rand_num = random.random()
        is_wall = 1 if rand_num < p else 0
        if (is_wall == 1):
            grd.add_column_wall(y)

    return grd


def cellObstaclesTilability_likelihood(n,m,p,iter=100,repeat=2):
    """
    Gives bake an approximation of the likelihood that n*m room is tilable when we assime a probability p of an existence
    of an obstacle for each cell
    :param n: int
        first dimension of the room
    :param m: int
        second dimension of the room
    :param p: int
        probability of obstacle existence. Required: 0<=p<1
    :param iter: int
        number of grids to approximate the tilability
    :param repeat: int
        number of time to repeat creating iter grids, then averaging over all the instances
    :return: float
        approximated probability
    """
    res = 0
    for _ in range(repeat):
        num_tilable=0
        for _ in range(iter):
            grd= randomObstacles_grid(n,m,p)
            if is_tilable(grd):
                num_tilable = num_tilable + 1
        res = res + num_tilable/(iter * 1.0)
    return res/repeat

def wallObstaclesTilability_likelihood(n,m,p,iter=100,repeat=2):
    """
        Gives bake an approximation of the likelihood that n*m room is tilable when we assume a probability p of the
        existence of a wall for each row and column
        :param n: int
            first dimension of the room
        :param m: int
            second dimension of the room
        :param p: int
            probability of wall existence. Required: 0<=p<1
        :param iter: int
            number of grids to approximate the tilability probability
        :param repeat: int
            number of time to repeat creating iter grids, to then averaging over all the instances
        :return: float
            approximated probability
        """
    res = 0
    for _ in range(repeat):
        num_tilable=0
        for _ in range(iter):
            grd= randomWalls_grid(n,m,p)
            if is_tilable(grd):
                num_tilable = num_tilable + 1
        res = res + num_tilable/(iter * 1.0)
    return res/repeat





