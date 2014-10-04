"""
"""

import unittest
import inspect

import bicycle
import bicycle.card


class TestModule(unittest.TestCase):
    def test_random(self):
        self.assertIs(bicycle.card.random, bicycle.random)

    def test_shuffle(self):
        self.assertEqual(bicycle.card.shuffle, bicycle.random.shuffle)

    def test_exceptions(self):
        self.assertTrue(issubclass(bicycle.card.DeckEmpty, Exception))
        self.assertTrue(issubclass(bicycle.card.DeckLow, Exception))


class TestDeckTypeStandard(unittest.TestCase):

    def test_init(self):
        dt = bicycle.card.DeckTypeStandard()
        self.assertEqual(dt._DeckTypeStandard__suits, ['S','D','C','H'])
        self.assertEqual(dt._DeckTypeStandard__ranks, ['A', '2', '3', '4', '5',
                                    '6', '7', '8', '9', '10', 'J', 'Q', 'K'])

        dt = bicycle.card.DeckTypeStandard(suits=['1', '2', '3', '4'],
                        ranks=['A', 'B', 'C', 'D'])
        self.assertEqual(dt._DeckTypeStandard__suits, ['1', '2', '3', '4'])
        self.assertEqual(dt._DeckTypeStandard__ranks, ['A', 'B', 'C', 'D'])

    def test_build(self):
        dt = bicycle.card.DeckTypeStandard()
        
        self.assertTrue(
                inspect.isgeneratorfunction(dt.build))

        self.assertEqual(list(dt.build()), [(0, 0), (0, 1), (0, 2), (0, 3),
                (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
                (0, 11), (0, 12), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
                (1, 12), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12),
                (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12)])

    def test_ranks_index(self):
        dt = bicycle.card.DeckTypeStandard()
        self.assertIsInstance(dt.ranks_index('A'), int)
        self.assertRaises(ValueError, lambda: dt.ranks_index('X'))

    def test_suits_index(self):
        dt = bicycle.card.DeckTypeStandard()
        self.assertIsInstance(dt.suits_index('S'), int)
        self.assertRaises(ValueError, lambda: dt.suits_index('X'))


    def test_get_rank(self):
        dt = bicycle.card.DeckTypeStandard()
        self.assertIsInstance(dt.get_rank(0), str)
        self.assertRaises(IndexError, lambda: dt.get_rank(10000000000000))

    def test_get_suit(self):
        dt = bicycle.card.DeckTypeStandard()
        self.assertIsInstance(dt.get_suit(0), str)
        self.assertRaises(IndexError, lambda: dt.get_suit(10000000000000))


class TestCardClass(unittest.TestCase):

    def test_init(self):
        c = bicycle.card.Card(1, 1)
        self.assertIsInstance(c.deck_type, bicycle.card.DeckTypeStandard)
        self.assertEqual(c.suit, 1)
        self.assertEqual(c.rank, 1)
        self.assertFalse(c.up)
        self.assertTrue(c.private)

        c = bicycle.card.Card(suit=0, rank=0, up=True, private=False)
        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_build(self):
        assert False, "Should be test code here."

    def test_from_str(self):
        c = bicycle.card.Card.from_str('AC')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 2)

        c = bicycle.card.Card.from_str('AS')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 0)

        c = bicycle.card.Card.from_str('AS', up=True, private=False)

        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_int(self):
        c = bicycle.card.Card.from_str('AD')
        self.assertEqual(int(c), 1)

        c = bicycle.card.Card.from_str('KH')
        self.assertEqual(int(c), 13)

    def test_eq(self):
        c1 = bicycle.card.Card.from_str('AS')
        c2 = bicycle.card.Card.from_str('AS')
        self.assertEqual(c1, c2)

    def test_lt(self):
        c1 = bicycle.card.Card.from_str('AS')
        c2 = bicycle.card.Card.from_str('KC')
        self.assertLess(c1, c2)

    # provided by functools.totalordering
    def test_ne(self):
        c1 = bicycle.card.Card.from_str('AS')
        c2 = bicycle.card.Card.from_str('KS')
        self.assertNotEqual(c1, c2)

    def test_gt(self):
        c1 = bicycle.card.Card.from_str('AS')
        c2 = bicycle.card.Card.from_str('KC')
        self.assertLess(c1, c2)

    def test_le(self):
        c1 = bicycle.card.Card.from_str('AS')
        c2 = bicycle.card.Card.from_str('KC')
        self.assertLessEqual(c1, c2)

        c3 = bicycle.card.Card.from_str('KC')
        self.assertLessEqual(c1, c3)

    def test_ge(self):
        c1 = bicycle.card.Card.from_str('KC')
        c2 = bicycle.card.Card.from_str('AS')
        self.assertGreaterEqual(c1, c2)

        c3 = bicycle.card.Card.from_str('AC')
        self.assertGreaterEqual(c1, c3)

    def test_serialize(self):
        c = bicycle.card.Card.from_str('AS')
        self.assertEqual(c.serialize(), 'XX')
        self.assertEqual(c.serialize(snoop=True), 'AS')

        c = bicycle.card.Card.from_str('KC', up=True)
        self.assertEqual(c.serialize(), 'KC')
        self.assertEqual(c.serialize(snoop=True), 'KC')

    def test_json(self):
        c = bicycle.card.Card.from_str('AS')
        self.assertEqual(c.__json__(), 'XX')

        c = bicycle.card.Card.from_str('KC', up=True)
        self.assertEqual(c.__json__(), 'KC')

    def test_persist(self):
        c = bicycle.card.Card.from_str('AS')
        self.assertEqual(c.__persist__(), 'AS')
        
        c = bicycle.card.Card.from_str('KC', up=True)
        self.assertEqual(c.__persist__(), 'KC')

    def test_repr(self):
        assert False, "Should be test code here."


class TestCards(unittest.TestCase):

    def test_init(self):
        h = bicycle.card.Cards()
        self.assertFalse(h)
        self.assertIsInstance(h, list)
        self.assertEqual(h.initlen, 0)
        self.assertEqual(h._deal_idx, 0)

        h = bicycle.card.Cards(deal_idx=-1)
        self.assertEqual(h._deal_idx, -1)
        self.assertRaises(AssertionError, lambda: bicycle.card.Cards(deal_idx=1))

    def test_int(self):
        h = bicycle.card.Cards()
        h.build()
        self.assertEqual(int(h), 364)

    def test_diff_check(self):
        assert False, "Cards.diff_check is completely wrong. Revisit this"
        # There are more checks that can be put here.
        h = bicycle.card.Cards()

        self.assertTrue(h.diff_check(1.0))
        self.assertTrue(h.diff_check(0.0))

        h.build()

        self.assertTrue(h.diff_check(1.0))
        self.assertFalse(h.diff_check(0.0))

        h.pop()

        self.assertTrue(h.diff_check(1.0))
        self.assertFalse(h.diff_check(0.0))

        h.discard([])

        self.assertTrue(h.diff_check(1.0))
        self.assertTrue(h.diff_check(0.0))

    def test_build(self):
        h = bicycle.card.Cards()

        h.build()
        self.assertEqual(len(h), 52)
        self.assertEqual(h.initlen, 52)

        h.build()
        self.assertEqual(len(h), 104)
        self.assertEqual(h.initlen, 104)
        self.assertRaises(AssertionError,
                          lambda: h.build(card_cls=bicycle.blackjack.card.Card))

        h = bicycle.card.Cards()
        h.build(numdecks=3)
        self.assertEqual(len(h), 156)
        self.assertEqual(h.initlen, 156)
        self.assertRaises(AssertionError,
                          lambda: h.build(card_cls=bicycle.blackjack.card.Card))

        h = bicycle.card.Cards()
        initdeck = h.build()[:]
        h = bicycle.card.Cards()
        h.build()
        self.assertEqual(initdeck, h)
        h = bicycle.card.Cards()
        h.build(do_shuffle=True)
        self.assertNotEqual(initdeck, h)

    def test_shuffle(self):
        h = bicycle.card.Cards()
        initdeck = h.build()[:]

        h = bicycle.card.Cards()
        h.build()
        h.shuffle()
        self.assertNotEqual(initdeck, h)

    def test_deal(self):
        d = bicycle.card.Cards()
        h = bicycle.card.Cards()
        d.build()

        d.deal(h)
        self.assertEqual(int(h[0]), 1)
        d.deal(h)
        self.assertEqual(int(h[1]), 2)

        d.deal(h, flip=True)
        self.assertTrue(h[2].up)

        d.deal(h, up=True)
        self.assertTrue(h[3].up)

        d.discard([])
        self.assertRaises(bicycle.card.DeckEmpty, lambda: d.deal([]))

    def test_deal_n(self):
        d = bicycle.card.Cards()
        h = bicycle.card.Cards()
        d.build()

        d.deal_n(h, 5)
        self.assertEqual(len(h), 5)

        d.deal_n(h, 10, flip=True)
        self.assertTrue(h[14].up)

    def test_discard(self):
        d = bicycle.card.Cards()
        h = bicycle.card.Cards()
        d.build()

        d.discard(h)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(h), 52)

        h.discard(d, flip=True)
        self.assertTrue(d[0].up)

        d.discard(h, up=False)
        self.assertFalse(h[0].up)

    def test_serialize(self):
        d = bicycle.card.Cards()
        d.build()
        self.assertEqual(d.serialize(), ['XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'])
        self.assertEqual(d.serialize(snoop=True), ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH'])

    def test_json(self):
        d = bicycle.card.Cards()
        d.build()
        self.assertEqual(d.__json__(), ['XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'])

    def test_persist(self):
        d = bicycle.card.Cards()
        d.build()
        self.assertEqual(d.__persist__(), ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH'])

    def test_repr(self):
        assert False, "Should be test code here."


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved