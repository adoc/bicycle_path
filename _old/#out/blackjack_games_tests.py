def main():
    from games.blackjack import Table, Player
    from strategy.blackjack import PlayerStrategy, DealerStrategy
    from pprint import pformat

    ps=PlayerStrategy()
    ds=DealerStrategy()

    p1 = Player('player1',10000)
    p2 = Player('player2',20000)
    p3 = Player('player3',30000)
    p4 = Player('player4',40000)
    p5 = Player('player5',50000)
    p6 = Player('player6',60000)

    g = Game()

    g.table.sit(p1)
    g.table.sit(p2)
    g.table.sit(p3)

    g.openbets() # clear table

    g.table.bet(200,p2)
    g.table.bet(300,p3)
    
    g.closebets()

    g.table.sit(p4)     # Player seated
    g.table.bet(100,p4) # Bet not accepted
    g.table.bet(100,p1) # Bet not accepted


    g=Game()
    g.table.sit(p1)
    g.table.sit(p2)
    g.table.sit(p3)
    g.table.sit(p4)
    g.table.sit(p5)
    g.table.sit(p6)

    i=0
    while True:
        i += 1
        print "Round: %s"%i

        #g.newround()

        g.openbets()

        g.table.bet(1,p1)
        g.table.bet(1,p2)
        g.table.bet(1,p3)
        g.table.bet(1,p4)
        g.table.bet(1,p5)
        g.table.bet(1,p6)

        g.closebets()

        g.table.newdeal()

        while g.table.dealer.hand.actable:
            
            data = g.data()
            
            print "data: %s"%data
            
            if g.table.dealing == g.table.dealer:
                advise = ds.advise(data[0].hand) and 'H' or 'S'
                act = g.act(advise)

            if g.table.dealing.hand.actable:
                advise = ps.advise(data[0].hand,int(data[1]))
                act = g.act(advise)

            else:
                g.table.nextdeal()

        g.resolve()

if __name__ == '__main__':
    main()