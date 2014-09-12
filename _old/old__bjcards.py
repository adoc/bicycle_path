class Hand(_Hand):
  def __int__(self):
    #val = super(Hand, self).__int__()
    #val = int(super(Hand, self))
    #val = int(self)
    val = 0
    for card in self.hand:
      val += int(card)
    ace = Card(rank='A')
    aces = self.find(ace)
    if val <= 11 and len(aces) > 0:  val += 10
    return val


class Player(Hand):
  def __init__(self, cash=100):
    self.hand = Hand()
    self.money = cash
    self.betAmnt = 0
  def addBet(self):
    self.money += self.betAmnt
    self.money = int(self.money)
    print "You now have %i."%self.money
  def addBetMult(self,mult): #takes (int)mult returns NULL
    self.money += bet*mult + 0.5
    self.money = int(self.money)
    print "You now have %i."%self.money
  def bet(self, player): #Asks the user how much they would like to bet and stores the val in betAmnt
    if player.money <= 0: #Oops, ran out of cash. End of the line for you.
      print "You are broke."
      return None
    print "You have %i."%player.money
    cash = raw_input("How much money would you like to bet? ")
    try:
      cash = int(cash)
      if cash > player.money:
        print "You really shouldn't spend money you don't have."
    except ValueError:
      if cash in ['Yes', 'yes', 'Y', 'y']:
        print "Bet defaulted to 5."
        cash = 5
      else:
        print "That's not a number..."
        return self.bet()
    self.betAmnt = cash
    return None
  def loseBet(self):
    self.money += self.betAmnt
    self.money = int(self.money)
    print "You now have %i."%self.money 

class BJPlayer(Player):
  def anotherCard(self):
    anotherCard = raw_input("Would you like another Card? ")
    if anotherCard in ['Yes', 'Y', 'Hit', 'H', 'yes', 'y' , 'hit', 'h']:
      return True
    elif anotherCard in ['No', 'N', 'Stand', 'S', 'no', 'n', 'stand', 's']:
      return False
    else:
      print "I'm sorry, I didn't understand that. Please use (Y)es, (H)it, or (N)o, (S)tand."
      return self.anotherCard()
  def cardTotal(self): return int(self.hand)
  def endTurn(self): #returns bool
    ph = int(self.hand) #player's hand total
    if ph == 21: 
      print "BLACKJACK!!!"
      self.addBetMult(1.5)
      return True
    if ph > 21:
      print "Ouch. You busted."
      self.loseBet()
      return True
    if ph < 21:
      return False if self.anotherCard() else True
  def play(self):
    while not self.endTurn():
      print repr(self.hand)
    return None
  
class Dealer(BJPlayer):
  """ Creates a Dealer

      Usage:
        Dealer() - Defaults to creating a Dealer with 6 decks in a shoe
        Dealer(number_of_decks) - Specify number of decks."""
  def __init__(self, *args):
    if len(args) == 0: self.shoe = Shoe(6)
    if len(args) == 1: self.shoe = Shoe(args[0])
    self.hand = Hand()
    self.shoe.shuffle()
  def deal(self): #dealer deals HIMSELF a hand
    if int(self.hand) < 17:
      self.shoe.deal(1,[self])
  def endTurn(self): return True if int(self.hand)<17 else False
  def play(self):
    self.deal()
    print repr(self.hand[0])
    while not self.endTurn():
      self.deal()

class Game(object):
  """ Performs actions common to most card Games.

      Usage:
        Game() - Defaults to creating a game with 1 Dealer and 1 Player
        Game(number_of_players,number_of_decks) - Specify number of players and decks."""
  def __init__(self, *args):
    self.players = []
    if len(args) == 0:
      self.dealer = Dealer(1)
      self.players.append(Player())
    if len(args) == 2:
      self.dealer = Dealer(args[1])
      for i in range(args[0]):
        self.players.append(Player())
  def again(self, player): #would you like to play again?
    inpt = raw_input("Would you like to play again? ")
    if inpt in ['Yes', 'Y', 'yes', 'y']: 
      del self.player.hand
      del self.dealer.hand
      return True
    elif inpt in ['No', 'N', 'no','n']:
      print "Thanks for playing!"
      print "Goodbye."
      return False
    else :
      print "Sorry, I didn't understand that. Please use (Y)es, or (N)o."
      self.again()
  def deal(self,numCards=1): self.dealer.shoe.deal(numCards,self.players)


class Blackjack(Game):
  """ Performs actions specific to Blackjack.

      Usage:
        Blackjack() - Defaults to creating a game with 1 Dealer and 1 Player
        Blackjack(number_of_players,number_of_decks) - Specify number of players and decks."""
  def __init__(self,*args):
    self.players = []
    if len(args) == 0:
      self.dealer = Dealer(1)
      self.players.append(BJPlayer())
    if len(args) == 2:
      self.dealer = Dealer(args[1])
      for i in range(args[0]):
        self.players.append(BJPlayer())
  def play(self):
    go = True
    while go:
      for p in self.players:
        self.pPlay(p)
        self.dealer.play()
        self.whoWon(dealer,p)
        go = again()
  def pPlay(self,p): #takes a PlayerType p
    self.dealer.shoe.deal(2,[p])
    print repr(p.hand)
    while not p.endTurn():
      self.dealer.shoe.deal(1,[p])
  def whoWon(self,dealer,player):
    ph = int(player.hand) #player's hand total
    dh = int(dealer.hand) #dealer's hand total
    if ph > 21: #covered in endGame
      return None
    if dh < 21:
      if ph > dh:
        print "You won!"
        player.addBet()
        return None
      if ph < dh:
        print "Sorry, you lost."
        player.loseBet()
        return None
      if ph == dh:
        print "It's a push."
        return None
    if dh > 21 and ph < 21:
      print "Dealer busted. You won!"
      player.addBet()
      return None