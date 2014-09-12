def main():
    from cards.blackjack import Shoe, Card
    from players.blackjack import Player, Seat

    s=Shoe()
    
    s.shuffle()

    p1 = Player('player1')
    p2 = Player('player2')
    
    s1 = Seat(p1)
    s2 = Seat(player=p2)

    s1.hand.append(s.pop())
    s1.hand.append(s.pop())
    s1.hand.append(s.pop())

    s2.hand.append(s.pop())
    s2.hand.append(s.pop())
    s2.hand.append(s.pop())
    
    print s1.hand
    for card in s1.hand:
        assert type(card)==Card
        assert card in s
        
    print s2.hand
    for card in s2.hand:
        assert type(card)==Card
        assert card in s

    table = [Seat() for _ in range(10)]

    for seat in table:
        assert seat.empty

if __name__ == '__main__':
    main()