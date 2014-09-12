def main():
    from games.blackjack import Table, Player
    from strategy.blackjack import PlayerStrategy, DealerStrategy
    from pprint import pformat

    ps=PlayerStrategy()
    ds=DealerStrategy()

    p1 = Player('player1',1000)
    p2 = Player('player2',1000)
    p3 = Player('player3',1000)
    p4 = Player('player4',1000)
    p5 = Player('player5',1000)
    p6 = Player('player6',1000)

    t = Table()

    t.sit(p1)
    t.sit(p2)
    t.sit(p3)
    t.sit(p4)
    t.sit(p5)
    t.sit(p6)

    i=0
    while True:
        i += 1
        print "Round: %s"%i

        t.checkshoe(factor=.2)

        t.bet(1,p1)
        t.bet(1,p2)
        t.bet(1,p3)
        t.bet(1,p4)
        t.bet(1,p5)
        t.bet(1,p6)

        t.setdeal()

        t.newdeal(numcards=2)

        #print t

        while t.dealer.hand.actable:
            #print t.dealer.hand
            data = t.data()
            
            if t.dealing == t.dealer:
                advise = ds.advise(data[0].hand) and 'H' or 'S'
                act = t.act(advise)
                print "data: %s | former advise: %s "%(data,advise)
            elif t.dealing.hand.actable:
                advise = ps.advise(data[0].hand,int(data[1]))
                act = t.act(advise)
                print "data: %s | former advise: %s "%(data,advise)
            else:
                t.nextdeal()
            t.checkhand()
            #print t.shoe
        t.resolve()

if __name__ == '__main__':
    main()