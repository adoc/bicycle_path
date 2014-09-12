class Dealer(object):
    def __init__(self, numdecks=1):
        self.shoe = Shoe(numdecks)

    def deal(self,count,*players): # Deal properly to multiple players [ hooray for poker next?? ]
        for i in range(count): # num of cards
          for p in players: # in to player's hands
            p.hand.append(self.cards[0])
  
    def shuffle(self):
        self.shoe.shuffle()


class Hand(object):
  """ A Hand. """
  
  def __init__(self):  self.hand = []
  def append(self,card):  self.hand.append(card)
  def find(self,card):
    index = []
    for each in self.hand:
      if each == card: index.append(self.hand.index(each))
    return index
  
  def __getitem__(self,index):  return self.hand[index]
  def __repr__(self):
    string = ''
    for card in self.hand:
      string = "%s%s,"%(string, repr(card))
    return string[:-1]
