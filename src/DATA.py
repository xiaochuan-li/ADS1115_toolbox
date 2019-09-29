import matplotlib.pyplot as plt
import numpy as np

"""----------------------------------------une list de data mesure----------------------------------------"""
DATA2 = [[1.4, 0.062412499999999996], [1.5, 0.461125], [1.6, 0.7871749999999998], [1.7, 1.0042500000000003],
         [1.8, 1.1736499999999999], [1.9, 1.2444625], [2.0, 1.33915], [2.1, 1.4020500000000002],
         [2.2, 1.4457250000000001], [2.3, 1.484325], [2.4, 1.508475],
         [2.5, 1.535375], [2.6, 1.5461624999999999], [2.7, 1.561675], [2.8, 1.5735125], [2.9, 1.5832125000000001],
         [3.0, 1.5939999999999999], [3.1, 1.5983750000000003], [3.2, 1.6051250000000004], [3.3, 1.6108250000000002],
         [3.4, 1.6160375000000002], [3.5, 1.6198374999999998], [3.6, 1.622875], [3.7, 1.6262250000000003],
         [3.8, 1.628975], [3.9, 1.6313375], [4.0, 1.632975], [4.1, 1.6346875], [4.2, 1.63625],
         [4.3, 1.6375249999999997],
         [4.4, 1.6386125], [4.5, 1.6398374999999998], [4.6, 1.6405874999999999]]


def transfer_data(data_list=DATA2):
    """
    to transfer a list of data_list into an array of tuple
    :param data_list: list, une list of data_list
    :return: an array of tuple
    """
    data_read = [(float(x[0]), float(x[1])) for x in data_list]
    data_get = np.array(data_read, dtype=[("x", float), ("y", float)])
    data_get.sort(order=["x", "y"])
    return data_get


def read_data(path="..//data//inter.txt"):
    """
    to read data from a text
    :param path: string, path of the text
    :return: an array of tuple
    """
    with open(path) as f:
        data_read = [(float(line.split()[0]), float(line.split()[1])) for line in f]
    data_get = np.array(data_read, dtype=[("x", float), ("y", float)])
    data_get.sort(order=["x", "y"])
    return data_get


def plot_data(data, x="distance", y="voltage"):
    """
    to plot a plan of the data
    :param data: array, an array of tuple
    :param x: description of axis x
    :param y: description of axis y
    :return: void
    """
    title = "relation entre {} et {}".format(x, y)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.grid()
    plt.plot(data["x"], data["y"])
    plt.show()


if __name__ == "__main__":
    data = read_data()
    plot_data(data, "voltage", "distance")
