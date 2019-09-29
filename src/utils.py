# coding=utf-8
import time

import os
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from sympy import *

from src.DATA import *

'''----------------------------------des function pour ADS----------------------------------'''


def get_ids(bus):
    """
    la function est pour trouver des ports available pour le moment
    :return: list, une list de ids des ports available pour bus,  0x48 par default
    """
    ids = []
    for i in range(128):
        try:
            bus.read_byte(i)
            ids.append(i)
        except:
            pass
    return ids


def write_config(bus, id, config):
    """
    la function est pour écrire une configuration au bus
    :param bus: SMBus, la structure utilisée pour localiser le bus
    :param id: int, id du port utilisé
    :param config: ADS1115, la class de ADS1115 qui contient la configuration
    :return: boolean, si on l'écrit avec success ou pas
    """
    try:
        data = [config.CODE >> 8, config.CODE & 0b0000000011111111]
        bus.write_i2c_block_data(id, 0x01, data)
        return True
    except:
        return False


def read_analogique(bus, id):
    """
    la function est pour lire un signal venant du bus
    :param bus: SMBus, la structure utilisée pour localiser le bus
    :param id: int, id du port utilisé
    :return: boolean, si on le lit avec success ou pas
    """
    try:
        data = bus.read_i2c_block_data(id, 0x00, 2)
        raw_adc = data[0] * 256 + data[1]
        return raw_adc
    except:
        return False


def code_sup(x):
    """
    la function est pour transmettre un entier à son code complémentaire
    :param x: int, l'entier entré
    :return: int, son code complémentaire
    """
    if x >= 2 ** 16 or x < 0:
        return 0
    if x >= 2 ** 15:
        return x % (2 ** 15) - 2 ** 15
    else:
        return x


def ana2volt(x, config):
    """
    la function est pour transmettre un signal à sa propre échelle de mesure
    :param x: int, la valeur analogique du signal
    :param config: ADS1115, la class de configuration
    :return: float, la valeur réelle du signal
    """
    fs = float(config.FSR[:-1])
    return code_sup(x) * fs / 2 ** 15


'''-----------------------------------------------------------------------------------------'''

'''--------------------------------des functions pour le fit--------------------------------'''


def get_coe(isCurve=True, path='..//data//curve.txt'):
    """
    la function est pour load les coéfficients calculé
    :param isCurve: Booléan, si la méthode est curve_fit ou interpolation
    :param path: str, l'adresse de fiche des coéfficients
    :return: list, une list de coéfficients
    """
    file_ = open(path, 'r')
    if isCurve:
        coe = [float(x) for x in file_.readlines()]
        coe = np.array(coe, dtype=[("coefficient", float)])
    else:
        coe = [(float(line.split()[0]), float(line.split()[1])) for line in file_.readlines()]
        coe = np.array(coe, dtype=[("voltage", float), ("distance", float)])
    return coe


def cal_curve(x, coe=get_coe()):
    """
    la function est pour calculer la distance avec la tension
    :param x: float, la tension
    :param coe: list, une list de coeficients
    :return: a list of resonable distance
    """
    res = (solve_dis(x, coe["coefficient"]))
    return check_res(res)


def save(isCurve, data):
    """
    la function est pour sauvegarder les coefficients
    :param isCurve: Booléan, si la méthode est curve_fit ou interpolation
    :param data: list, une list de coefficients
    :return: void
    """
    if isCurve:
        file_ = open('curve.txt', 'w')
        for coe in data:
            file_.write("{}\n".format(str(coe)))
        file_.close()
    if not isCurve:
        file_ = open('inter.txt', 'w')
        for coe in data:
            file_.write("{} {}\n".format(str(coe[0]), str(coe[1])))
        file_.close()


def func(x, a, b, c, d, e, f):
    """
    la function a fit
    :param x: np.array, les variables de distances
    :param a: float, coefficient
    :param b: float, coefficient
    :param c: float, coefficient
    :param d: float, coefficient
    :param e: float, coefficient
    :param f: float, coefficient
    :return: np.array, les tensions
    """
    coe = [a, b, c, d, e]
    res = np.zeros(x.shape)
    res += f * x ** (-1)
    for i in range(len(coe)):
        res += np.power(x, i) * coe[i]
    return res


def func_exp(x, a, b, c, d, e, f):
    """
    la function a fit
    :param x: np.array, les variables de distances
    :param a: float, coefficient
    :param b: float, coefficient
    :param c: float, coefficient
    :param d: float, coefficient
    :param e: float, coefficient
    :param f: float, coefficient
    :return: np.array, les tensions
    """
    res = np.zeros(x.shape)
    res += a * x * np.exp(b * x) + c / x + d + e * x ** (-2) + f * x ** (-3)  # e*x*np.exp(f*x)
    return res


def optimize_func(f, x, y):
    """
    optimization d'une function
    :param f: function, la function a fit
    :param x: np.array, les variables de distances
    :param y: np.array, les tensions
    :return:
    """
    popt, pcov = curve_fit(f, x, y)
    return popt


def solve_dis(y, popt):
    """
    calculer la distance avec la tension
    :param y: float, la tension
    :param popt: list, la list des coefficients
    :return: list, une list de distances possibles
    """
    [a, b, c, d, e, f] = popt
    x = Symbol('x', real=True)
    return solveset(f * x ** (-1) + a * x ** 0 + b * x ** 1 + c * x ** 2 + d * x ** 3 + e * x ** 4 - y, x,
                    domain=S.Reals)


def check_res(x, x_min=1.1, x_max=4.6):
    """
    regarder si les distances sont raisonable
    :param x: list, une list de distances possibles
    :param x_min: float, minimum de distance
    :param x_max: float, maximum de distance
    :return: les distances raisonable
    """
    res = []
    for x_o in x:
        if x_min <= x_o <= x_max:
            res.append(x_o)
    return res


def curve_exp_demo(x, y):
    x_min = min(x)
    x_max = max(x)
    x_test = np.linspace(x_min, x_max, 500)
    popt = optimize_func(func_exp, x, y)
    [a, b, c, d, e, f] = popt
    return x_test, func_exp(x_test, a, b, c, d, e, f)


def curve_demo(x, y):
    x_min = min(x)
    x_max = max(x)
    x_test = np.linspace(x_min, x_max, 500)
    popt = optimize_func(func, x, y)
    [a, b, c, d, e, f] = popt
    save(True, popt)
    return x_test, func(x_test, a, b, c, d, e, f)


def inter_demo(x, y):
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    x_test = np.linspace(y_min, y_max, 500)
    func_int = interp1d(y, x, kind='cubic')
    save(False, zip(x_test, func_int(x_test)))
    return func_int(x_test), x_test


def bi_min(input, path="..//data//inter.txt"):
    data = get_coe(False, path)
    voltage = data["voltage"]
    if input > voltage.max() or input < voltage.min():
        print("out of segment")
        return 0
    else:
        pur_valtage = voltage - input
        comp = pur_valtage[1:] * pur_valtage[:-1]
        index = np.argmin(comp)
        neg, pos = data[index:index + 2]
        if pos["voltage"] == neg["voltage"]:
            return 0.5 * (neg["distance"] + pos["distance"])
        else:
            ratio = (input - neg["voltage"]) / (pos["voltage"] - neg["voltage"])
            return (pos["distance"] - neg["distance"]) * ratio + neg["distance"]


def comp_curve_inter(issave=False,path=".//figure//comparison.png"):
    voltages = np.linspace(1.1, 1.6, 500)
    start_0 = time.time()

    distance_curve = [cal_curve(voltage)[0] for voltage in voltages]
    end_0 = time.time()

    distance_inter = [bi_min(voltage) for voltage in voltages]
    end_1 = time.time()

    plt.title("Comparison of Two Method With 500 Points")
    plt.plot(voltages, distance_curve, "b", label="curve using {} s".format(end_0 - start_0))
    plt.plot(voltages, distance_inter, "r", label="inter using {} s".format(end_1 - end_0))
    plt.legend()
    if issave:
        plt.savefig(path)
    plt.show()



'''-----------------------------------------------------------------------------------------'''

'''-----------------------------------------------------------------------------------------'''

if __name__ == "__main__":
    comp_curve_inter(issave=True,path="..//figure//cop.png")
    """
    print(get_coe(False,"inter.txt"))
    print(bi_min(1.3))
    #print(get_coe(False, "inter.txt"))
    """
    '''
    data=transfer_data()
    x=data["x"]
    y=data["y"]
    x_curve, y_curve = curve_demo(x, y)
    x_exp, y_exp = curve_exp_demo(x, y)
    x_inter, y_inter = inter_demo(x, y)
    f_data = plt.plot(x, y, 'r', label="data")
    f_curve = plt.plot(x_curve, y_curve, 'y', label="curve")
    f_exp = plt.plot(x_exp, y_exp, 'g', label='curve exp')
    f_inter = plt.plot(x_inter, y_inter, 'b', label="inter")
    plt.xlabel("distance")
    plt.ylabel("voltage")
    plt.legend()
    plt.show()
'''
