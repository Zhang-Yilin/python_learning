import random
from collections import Counter

class poker(object):
    def __init__(self, num, suit):
        self.__num = num
        if suit in ("heart", "spade", "club", "diamond"):
            self.__suit = suit
        else:
            raise TypeError

    __slots__ = ("__num", "__suit")

    def get_num(self):
        return self.__num

    def get_suit(self):
        return self.__suit

    def __str__(self):
        return "number is %d, suit is %s" % (self.__num, self.__suit)

    __repr__ = __str__

    def __eq__(self, obj):
        if self.__num == obj.get_num() and self.__suit == obj.get_suit():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.__num < other.get_num():
            return True
        else:
            return False

    def __gt__(self, other):
        if self.__num > other.get_num():
            return True
        else:
            return False

    def __le__(self, other):
        if self.__num <= other.get_num():
            return True
        else:
            return False

    def __ge__(self, other):
        if self.__num >= other.get_num():
            return True
        else:
            return False


class poke_suit(object):
    pokerlist = list()
    suitlist = ("heart", "spade", "club", "diamond")
    for i in range(13):
        for j in range(4):
            pokerlist.append(poker(i+1, suitlist[j]))

    def test(self):
        print(self.pokerlist[0])

    def shuffle(self):
        random.shuffle(self.pokerlist)

    def deal(self):
        p = self.pokerlist.pop()
        return p

    def resetpoker(self):
        self.pokerlist = []
        for i in range(13):
            for j in range(4):
                self.pokerlist.append(poker(i + 1, self.suitlist[j]))


class Texas_Holdem(poke_suit):
    def __init__(self, num = 6):
        if isinstance(num, int):
            self.__number = num
            self.player = []
            self.turn = 0
            self.playerresult = []
            for i in range(num):
                self.player.append([])
        else:
            raise TypeError


    def pub_assign(self, num, suit):
        p = poker(num, suit)
        for i in self.player:
            i.append(p)
        self.pokerlist.remove(p)
        self.turn += 1

    def reset(self):
        for i in range(self.__number):
            self.player[i] = []
        self.resetpoker()
        self.__number = 0

    def get_info(self):
        for i in self.player:
            print(i)

    def checkst(self):
        if self.turn > 2:
            print("Error, automatic reset")
            self.reset()
            return False
        else:
            return True

    def private_assign(self, num, suit, player_no = 0):
        p = poker(num, suit)
        self.player[player_no].append(p)
        self.pokerlist.remove(p)

    def finish_public(self):
        x = self.checkst()
        if x == False:
            raise ValueError
        else:
            while self.turn < 2:
                x = self.pokerlist.pop()
                for i in self.player:
                    i.append(x)
                self.turn += 1

    def finish_private(self):
        if self.turn > 2:
            raise ValueError
        else:
            for i in self.player:
                while len(i) < 7:
                    i.append(self.pokerlist.pop())

    def conpair(self):
        pass

    def check_result(self):
        for i in self.player:
            x = list(map(lambda j: (j.get_num(), j.get_suit()), i))
            self.playerresult.append(x)








if __name__ == "__main__":


    p = Texas_Holdem(4)
    p.shuffle()
    print(p.pokerlist)
    p.pub_assign(1, "diamond")
    p.get_info()
    print(p.turn)
    p.finish_public()
    p.private_assign(5, "club")
    p.private_assign(11, "club")
    p.finish_private()
    print(len(p.player[0]))
    p.check_result()
    print(p.playerresult[0])