import math


class Statisticer:
    def __init__(self, bad_time=0.002):
        self.length_list = []
        self.time_list = []
        self.bad_time = bad_time
        self.bottleneck_list = []
        self.count = 0
        self.bad_count = 0
        self.edit1_list = []
        self.edit2_list = []

    def get_average(self):
        return math.ceil(len(self.length_list) / sum(self.time_list))

    def print_full_information(self):
        print('Всего слов: ', self.count)
        print('Забанено слов: ', self.bad_count)
        print('Считали edit1_dist для слов:\n', self.edit1_list)
        print('Считали edit2_dist для слов:\n', self.edit2_list)
        print('Долго обрабатывали слова:\n', self.bottleneck_list)
