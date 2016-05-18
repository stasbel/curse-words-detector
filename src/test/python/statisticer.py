import math


class Statisticer:
    def __init__(self, bad_time=0.002):
        self.length_list = []
        self.time_list = []
        self.bad_time = bad_time
        self.bottleneck_list = []
        self.count = 0

    def get_average(self):
        return math.ceil(len(self.length_list) / sum(self.time_list))
