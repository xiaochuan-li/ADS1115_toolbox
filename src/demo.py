import smbus

'''--------------------------------------des libraries--------------------------------------'''
from src.ADS1115 import *
from src.utils import *

'''-----------------------------------------------------------------------------------------'''


def test_demo():
    bus = smbus.SMBus(1)
    id = get_ids(bus)[0]
    ads = ADS1115()
    ads.set_AIN(0, -1)
    ads.set_FSR(1)
    ads.refresh_description()

    print(ads.descriptor())

    if not write_config(bus, id, ads):
        print("error when write")
        return 0
    voltages = [ana2volt(read_analogique(bus, id), ads) for i in range(10)]

    return voltages


def test_demo_plot():
    plt.figure(figsize=(8, 6), dpi=80)
    plt.ion()
    bus = smbus.SMBus(1)
    id = get_ids(bus)[0]
    ads = ADS1115()
    ads.set_AIN(0, -1)
    ads.set_FSR(1)
    ads.refresh_description()
    FS = float(ads.FSR[:-1])
    # print the configuration

    print(ads.descriptor())
    # write config into bus
    if not write_config(bus, id, ads):
        print("error when write")
        return 0

    while True:
        if voltages is None:
            voltages = []
        if distances is None:
            distances = []
        plt.cla()
        plt.grid(True)
        voltage = ana2volt(read_analogique(bus, id), ads)
        distance = cal_curve(voltage)[0]
        voltages.append(voltage)
        distances.append(distance)
        plt.title("Voltage entre {} et {}\ncurrent voltage : {}\ncurrent distance : {}".format(ads.AINP, ads.AINN,
                                                                                               str(voltage)[:6],
                                                                                               str(distance)[:4]))
        if len(voltages) < 100:
            plt.plot(np.arange(len(voltages)) * 0.1, voltages, label='voltage')
            plt.plot(np.arange(len(voltages)) * 0.1, distances, label='distance')
        else:
            plt.plot(np.arange(10), voltages[-100:], label='voltage')
            plt.plot(np.arange(10), distances[-100:], label='distance')
        plt.legend()
        plt.axis([-1, 11, -1.2 * FS, 1.2 * FS])
        print("voltage = %f" % voltage)
        plt.pause(0.0001)
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    test_demo_plot()
