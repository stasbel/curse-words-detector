from pymystem3 import Mystem

mystem = Mystem()


# TODO add mystem

def normal_form1(word):
    return mystem.lemmatize(word.lower())[0]


if __name__ == '__main__':
    print(normal_form1('ебошить'))
