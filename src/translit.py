
translit_dict = {u'@' : u'а',
                 u'*' : u'ж',
                 u'3' : u'з',
                 u'4' : u'а',
                 u'6' : u'б',
                 u'0' : u'о',
                 u'a' : u'а',
                 u'b' : u'б',
                 u'c' : u'с',
                 u'd' : u'д',
                 u'e' : u'е',
                 u'f' : u'ф',
                 u'g' : u'д',
                 u'h' : u'х',
                 u'i' : u'и',
                 u'j' : u'й',
                 u'k' : u'к',
                 u'l' : u'л',
                 u'm' : u'м',
                 u'n' : u'н',
                 u'o' : u'о',
                 u'p' : u'р',
                 u'q' : u'ку',
                 u'r' : u'г',
                 u's' : u'с',
                 u't' : u'т',
                 u'u' : u'у',
                 u'v' : u'в',
                 u'w' : u'в',
                 u'x' : u'х',
                 u'y' : u'у',
                 u'z' : u'з'}

def translit(word):
    translist_word = u''
    for c in word:
        if c in translit_dict:
            translist_word += translit_dict[c]
        else:
            translist_word += c
    return translist_word