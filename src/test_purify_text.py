# coding=utf-8
from unittest import TestCase
from purifier import purify_text
import numpy as np
import matplotlib.pyplot as plt

STR1 = "Говно, залупа, пенис, хер, давалка, хуй, блядина, Головка, шлюха, жопа, член, еблан, петух, мудила, Рукоблуд," \
       " ссанина, очко, блядун, вагина, Сука, ебланище, влагалище, пердун, дрочила Пидор, пизда, туз, малафья, гомик," \
       " мудила, пилотка, манда, Анус, вагина, путана, педрила, шалава, хуила, мошонка, елда."
PURIFIED_STR1 = "*, *, *, *, *, *, *, Головка, *, *, член, *, петух, *, *, *, очко, *, *, *, *ище, *, *, * *, *, туз," \
                " *, *, *, *, *, *, *, *, *, *, *, *, *."
STR2 = "нормальное выражение"
PURIFIED_STR2 = STR2
SRT3 = "ах ты сука, пизда ебаная"
PURIFIED_STR3 = "ах ты *, * *"
STR4 = "тут не должно быть звездочек"
PURIFIED_STR4 = STR4

SCALE = 100
time_list = []


class TestTextPolicy(TestCase):
    def check(self, str1, str2):
        self.assertEqual(str1, purify_text(str2, time_list))

    def test1(self):
        self.check(PURIFIED_STR1, STR1)

    def test2(self):
        self.check(PURIFIED_STR2, STR2)

    def test3(self):
        self.check(PURIFIED_STR3, SRT3)

    def test4(self):
        self.check(PURIFIED_STR4, STR4)

    def test5(self):
        xs = [1, 2, 1]
        ys = [2, 3, 1]
        plt.title('Lines')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.plot(xs, ys)
        plt.show()
        # plt.hist(time_list, bins=[(float(i) / SCALE) for i in range(0, SCALE)])
        # plt.show()

    pass
