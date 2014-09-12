from .. import Suits,Ranks,Card,Deck,Shoe

class Test(object):
    Suits=Suits
    Ranks=Ranks
    Card=Card
    Deck=Deck
    Shoe=Shoe
    def __init__(self):
        """ Base Cards Test """
        Suits=self.Suits
        Ranks=self.Ranks
        Card=self.Card
        Deck=self.Deck
        Shoe=self.Shoe

        print "cards.tests"

        print type(Suits)
        print type(Ranks)
        print type(Card())
        print type(Deck())
        print type(Shoe())

        print "Suits: %s"%[suit for suit in Suits]
        assert len(Suits)==4
        print "Ranks: %s"%[rank for rank in Ranks]
        assert len(Ranks)==13

        print 'Card("A") == Card("a")'
        assert Card("A") == Card("a")

        

        print 'Card("AC") == Card("ac") == Card(rank="a",suit="c") == Card(rank=0,suit=1)'
        assert Card("AC") == Card("ac") == Card(rank='a',suit='c') == Card(rank=1,suit=1)

        print 'Card("AC") != Card("as")'
        assert Card("AC") != Card("as")

        d = Deck()
        print "Deck: %s"%d

        print "len(d)==d.initlen==52"
        assert len(d)==d.initlen==52
        print "Card() in Deck()"
        assert Card() in d
        print "Card('a') in Deck()"
        assert Card('a') in d
        print "Card('ac') in Deck()"
        assert Card('ac') in d

        d2 = Deck()
        print "Deck() == Deck()"
        assert d == d2
        d2.shuffle()
        print "Shuffled Deck: %s"%d2
        print "Shuffled Deck() != Deck()"
        assert d != d2

        c = d.pop()
        print type(c)
        print "Deal One: %s"%c
        assert c == Card('KD')
        print "c == Card('KD')"

        s = Shoe()
        print "Shoe card type: %s"%type(s[0])