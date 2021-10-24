import math


class SkyColour:

    @staticmethod
    def get_colour_for_temp(temp):
        temp = math.floor(temp)
        if temp <= 14:
            return (0, 0, 255)
        if temp > 14 and temp <= 17:
            return (10, 0, 250)
        if temp > 17 and temp <= 20:
            return (0, 150, 255)
        if temp > 20 and temp <= 25:
            return (96, 133, 255)
        if temp > 25 and temp <= 28:
            return (150, 70, 255)
        if temp > 28 and temp <= 33:
            return (200, 100, 5)
        if temp > 33 and temp <= 37:
            return (180, 29, 70)
        if temp > 37:
            return (255, 0, 0)

    @staticmethod
    def get_colour_for_skycondition(cloudcover, precip):
        cloudcover = math.floor(cloudcover * 100)
        precip = math.floor(precip * 100)



        if precip >= 40:
            if precip > 90:
                return (0, 255, 0)
            elif precip > 80:
                return (65, 255, 65)
            elif precip > 60:
                return (110, 255, 110)

            return (140, 255, 140)

        return (0, 0, 0)
