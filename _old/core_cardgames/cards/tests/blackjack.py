from . import Test as TestCards
from ..blackjack import Suits,Ranks,Card,Deck,Shoe

class Test(TestCards):
    Suits=Suits
    Ranks=Ranks
    Card=Card
    Deck=Deck
    Shoe=Shoe
    def __init__(self):
        """ Also inits cards.tests.Test with .blackjack classes (where applicable) """

        print "\nBlackjack Tests - Base\n"

        super(Test,self).__init__()

        print "\nBlackjack Tests - Extended\n"

        c1 = Card("AC")
        c2 = Card("as")
        print 'Card("AC") == Card("as")'
        assert c1 == c2

        print 'int(Card("AC"))==1'
        assert int(Card("AC"))==1

        print 'int(Card("KS"))==10'
        assert int(Card("KS"))==10

        print 'int(Card("JC"))==10'
        assert int(Card("JC"))==10

        