"""----------------------------------des paramètres de ads----------------------------------"""
DICT_AIN = [[0, 1], [0, 3], [1, 3], [2, 3], [0, 4], [1, 4], [2, 4], [3, 4]]
DICT_FSR = ["6.144V", "4.096V", "2.048V", "1.024V", "0.512V", "0.256V"]
DICT_RATE = ["8 SPS", "16 SPS", "32 SPS", "64 SPS", "128 SPS", "250 SPS", "475 SPS", "860 SPS"]
"""-----------------------------------------------------------------------------------------"""


class ADS1115:

    def __init__(self, AINP="AIN0", AINN="GND", FSR="2.048V", MODE="CONTINUS", RATE="128 SPS",
                 CODE=0b1100010010000011):
        """
        :param AINP: str, AIN positive
        :param AINN: str, AIN negative
        :param FSR: str, FS
        :param MODE: str, MODE
        :param RATE: str, sample rate
        :param CODE: int, code de configuration
        """
        self.AINP = AINP
        self.AINN = AINN
        self.FSR = FSR
        self.MODE = MODE
        self.RATE = RATE
        self.CODE = CODE

    def descriptor(self):
        """
        :return: str, une string de description
        """
        return ("AINP = {}\n"
                "AINN = {}\n"
                "FSR = {}\n"
                "MODE = {}\n"
                "SAMPLE RATE = {}\n"
                "CONFIG CODE = {}\n".format(self.AINP,
                                            self.AINN,
                                            self.FSR,
                                            self.MODE,
                                            self.RATE,
                                            bin(self.CODE)[2:]))

    def set_AIN(self, ainp, ainn):
        """
        to set the AIN pair
        :param ainp: int, the index of positive AIN
        :param ainn: int, the index of negative AIN
        :return: boolean, if the pair has been set successfully
        """
        if ainp < 0 or ainp == ainn:
            print("input error")
            return False
        else:
            if ainn < 0:
                code_ain = 4 + ainp
            elif ainn == 3:
                code_ain = 1 + ainp
            elif ainp == 0 and ainn == 1:
                code_ain = 0
            else:
                print("input error")
                return False
            self.CODE = (self.CODE & 0b1000111111111111) | (code_ain << 12)
            return True

    def set_FSR(self, niveau):
        """
        to set the FS level
        :param niveau: int, index of level
        :return: boolean, if the level has been set successfully
        """
        if niveau < 0 or niveau > 5:
            print("input error")
            return False
        else:
            self.CODE = (self.CODE & 0b1111000111111111) | (niveau << 9)
            return True

    def set_rate(self, niveau):
        """
        to set the sample rate
        :param niveau: int, index of level
        :return: boolean, if the level has been set successfully
        """
        if niveau < 0 or niveau > 7:
            print("input error")
            return False
        else:
            self.CODE = (self.CODE & 0b1111111100011111) | (niveau << 5)
            return True

    def refresh_description(self):
        """
        to refresh all the description
        :return: void
        """
        # AIN
        code_ain = (self.CODE >> 12) & 0b0111
        # DICT_AIN = [[0, 1], [0, 3], [1, 3], [2, 3], [0, 4], [1, 4], [2, 4], [3, 4]]
        ind_p, ind_n = DICT_AIN[code_ain]
        self.AINP = "AIN" + str(ind_p)
        self.AINN = "AIN" + str(ind_n)
        if (ind_n == 4): self.AINN = "GND"

        # FSR
        code_fsr = (self.CODE >> 9) & 0b0000111
        # DICT_FSR = ["6.144V", "4.096V", "2.048V", "1.024V", "0.512V", "0.256V"]
        self.FSR = DICT_FSR[code_fsr]

        # MODE

        # rate
        code_rate = (self.CODE >> 5) & 0b00000000111
        # DICT_RATE = ["8 SPS", "16 SPS", "32 SPS", "64 SPS", "128 SPS", "250 SPS", "475 SPS", "860 SPS"]
        self.RATE = DICT_RATE[code_rate]

    @staticmethod
    def help_description():
        """
        to print a table of description
        :return:void
        """
        # for ain
        print("--------TABLE FOR AIN(AIN4=GND)-------")
        print("--------------------------------------")
        print("| CODE (10) |  CODE (2) | AINP | AINN |")
        for i in range(8):
            print("|     {}     |    {}    | AIN{} | AIN{} |".format(str(i), bin(i)[2:].zfill(3), DICT_AIN[i][0],
                                                                     DICT_AIN[i][1]))
        print("--------------------------------------")
        print("------------TABLE FOR FSR------------")
        print("--------------------------------------")
        print("| CODE (10) |  CODE (2) |     FSR     |")
        for i in range(6):
            print("|     {}     |    {}    |   {}    |".format(str(i), bin(i)[2:].zfill(3), DICT_FSR[i]))
        print("--------------------------------------")
        print("------------TABLE FOR RATE------------")
        print("--------------------------------------")
        print("| CODE (10) |  CODE (2) |    RATE     |")
        for i in range(8):
            print("|     {}     |    {}    |  {}    |".format(str(i), bin(i)[2:].zfill(3), DICT_RATE[i].rjust(7, ' ')))
        print("--------------------------------------")


if __name__ == "__main__":
    ads = ADS1115()
    print(ads.descriptor())
    ads.help_description()
