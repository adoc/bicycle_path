def main():
    from games import Table,Player
    
    from pprint import pformat

    p1 = Player('player1')
    p2 = Player('player2')
    p3 = Player('player3')

    g = Table()

    g.sit(p1)
    g.sit(p2)
    g.sit(p3)

    g.clear() # clear table

    g.bet(100,p1)
    g.bet(200,p2)
    g.bet(300,p3)
    
    g.setdeal()

    g.newdeal()

    print pformat(g.seats)



if __name__ == '__main__':
    main()