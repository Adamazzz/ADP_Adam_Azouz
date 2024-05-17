import csv
import random
import utility_funcs

def generateData_Varying_p(tilability_func, file_name=f"../inputs/varying_p.csv", n_arr=[5,12,18],m_arr=[7,8,14], iter=50, paral=1):
    """
    Generate data, for a defined set of (n,m) produced by (n_arr X m_arr), with varying probability. And save it into a file.
    :param tilability_func: a function that is called to get the probability of tilability for a given (n,m,p)
    :param file_name: string
    :param n_arr: array
    :param m_arr: array
    :param iter: number of times the tilability experience should be held to make the probability of tilability approximation
    :param paral: number of parallel threads to be ran
    :return: None
    """
    data_var_p = []
    p_arr = []

    
    for i in range(10, 100, 3):
        p_arr.append(i / 10000.0)
    for i in range(100, 250, 7):
        p_arr.append(i / 10000.0)
    for i in range(250, 5000, 110):
        p_arr.append(i / 10000.0)

    for p in p_arr:
        for n in n_arr:
            for m in m_arr:
                tilability_probability = tilability_func(n, m, p, iter, paral)
                data_var_p.append([n, m, p, tilability_probability])

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['n', 'm', 'p', 'probability'])
        writer.writerows(data_var_p)

def generateData_Varying_dim(tilability_func, file_name=f"../inputs/varying_dim.csv", p_obstacle=[0.01], n_arr=[5,12,17,18], m_range=(2,20), iter=50, paral=1):
    """
    Generate data, for a defined set of (p,n) produced by (p_obstacle X n_arr), with m spanning the range defined by the tuple m_range. And save it into a file.
    :param tilability_func: a function that is called to get the probability of tilability for a given (n,m,p)
    :param file_name: string
    :param p_obstacle: array
    :param n_arr: array
    :param m_range: a tuple
    :param iter: number of times the tilability experience should be held to make the probability of tilability approximation
    :param paral: number of parallel threads to be ran
    :return:
    """
    data_var_dim = []
    for p in p_obstacle:
        for n in n_arr:
            for m in range(m_range[0], m_range[1]):
                tilability_probability = tilability_func(n, m, p, iter, paral)
                data_var_dim.append([n, m, p, tilability_probability])

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['n', 'm', 'p', 'probability'])
        writer.writerows(data_var_dim)

def generateData_ML_model(tilability_func, file_name = f"../inputs/tilability_data.csv",data_points=500, iter=50, paral=1):
    """
    Generate data that will be fed to the Machine learning models
    :param tilability_func: a function that is called to get the probability of tilability for a given (n,m,p)
    :param file_name: string
    :param data_points: int, number of data points to be generated
    :param iter: number of times the tilability experience should be held to make the probability of tilability approximation
    :param paral: number of parallel threads to be ran
    :return: None
    """
    count = 0
    data = []
    for _ in range(data_points):
        n = random.randint(1, 20)
        m = random.randint(1, 20)
        p = random.random()
        if count % 4 == 0:
            p = p / 1000
        elif count % 4 == 1:
            p = p / 100
        elif count % 4 == 2:
            p = p / 10

        tilability_probability = tilability_func(n, m, p, iter, paral)
        data.append([n, m, p, tilability_probability])
        count = count + 1
        print(count)
    for _ in range(int(data_points / 25)):
        n = random.randint(20, 30)
        m = random.randint(5, 25)
        p = random.random()
        if count % 4 == 0:
            p = p / 1000
        elif count % 4 == 1:
            p = p / 100
        elif count % 4 == 2:
            p = p / 10
        tilability_probability = tilability_func(n, m, p, iter, paral)
        data.append([n, m, p, tilability_probability])
        count = count + 1
        print(count)

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['n', 'm', 'p', 'probability'])
        writer.writerows(data)


#***********************************************************************************************************************

generateData_Varying_p(utility_funcs.cellObstaclesTilability_likelihood,file_name=f"../inputs/varying_p_cell.csv")
generateData_Varying_p(utility_funcs.wallObstaclesTilability_likelihood,file_name=f"../inputs/varying_p_wall.csv")

generateData_Varying_dim(utility_funcs.cellObstaclesTilability_likelihood,file_name=f"../inputs/varying_dim_cell_2.csv",p_obstacle=[0.1,0.3,0.5])
generateData_Varying_dim(utility_funcs.wallObstaclesTilability_likelihood,file_name=f"../inputs/varying_dim_wall_2.csv",p_obstacle=[0.1,0.3,0.5])

data_points=500
generateData_ML_model(utility_funcs.cellObstaclesTilability_likelihood,file_name=f"../inputs/tilability_data_{data_points}_cell.csv",data_points=data_points)
generateData_ML_model(utility_funcs.wallObstaclesTilability_likelihood,file_name=f"../inputs/tilability_data_{data_points}_wall.csv",data_points=data_points)

