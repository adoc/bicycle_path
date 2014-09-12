import csv, os

class DealerStrategy(object):
    def advise(self, hand):
        """ Returns:
                True: Hit
                False: Stand"""
        #print "hand.soft: %s"%hand.soft
        #print "hand.total: %s"%hand.total
        #print "(hand.soft and hand.total < 18): %s"%(hand.soft and hand.total < 18)
        #print "(not hand.soft and hand.total < 17): %s"%(not hand.soft and hand.total < 17)
        #print "(hand.soft and hand.total < 18) or (not hand.soft and hand.total < 17): %s"%((hand.soft and hand.total < 18) or (not hand.soft and hand.total < 17))
        return (hand.soft and hand.total < 18) or (not hand.soft and hand.total < 17)

class PlayerStrategy(object):
    def __init__(self,strattype='basic'):
        def parse_strat(reader):
            head = reader.next()
            strat = {}
            for row in reader:
                newrow = {}
                for col in head[1:]:
                    newrow.update( {int(head[int(col)]) : row[int(col)]} )

                rowsplit = row[0].split(':')
                start = int(rowsplit[0])
                try:    stop = int(rowsplit[1])
                except: stop = int(rowsplit[0])

                for i in range(start,stop+1):
                    strat.update( {i:newrow} )
            return strat

        import cardgames
        dir_module_container = os.path.dirname(cardgames.__file__)

        hardfile = open('%s/data/blackjack/%s_hard.csv'%(dir_module_container,strattype),'rb')
        softfile = open('%s/data/blackjack/%s_soft.csv'%(dir_module_container,strattype),'rb')
        pairsfile = open('%s/data/blackjack/%s_pairs.csv'%(dir_module_container,strattype),'rb')

        self.hard = parse_strat(csv.reader(hardfile))
        self.soft = parse_strat(csv.reader(softfile))
        self.pairs = parse_strat(csv.reader(pairsfile))

        hardfile.close()
        softfile.close()
        pairsfile.close()

    def advise(self, hand, dealer_show):
        """ Returns: {action table}"""
        try:
            if hand.pair:
                return self.pairs[hand.total][dealer_show]
            elif hand.soft:
                return self.soft[hand.total][dealer_show]
            else:
                return self.hard[hand.total][dealer_show]   
        except KeyError, e:
            print "Error: %s"%e
            