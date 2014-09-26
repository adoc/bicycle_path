import unittest
import inspect
import bicycle.cards


class TestDeckTypeStandard(unittest.TestCase):

    def test_init(self):
        dt = bicycle.cards.DeckTypeStandard()
        self.assertEqual(dt._DeckTypeStandard__suits, ['S','D','C','H'])
        self.assertEqual(dt._DeckTypeStandard__ranks, ['A', '2', '3', '4', '5',
                                    '6', '7', '8', '9', '10', 'J', 'Q', 'K'])

        dt = bicycle.cards.DeckTypeStandard(suits=['1', '2', '3', '4'],
                        ranks=['A', 'B', 'C', 'D'])
        self.assertEqual(dt._DeckTypeStandard__suits, ['1', '2', '3', '4'])
        self.assertEqual(dt._DeckTypeStandard__ranks, ['A', 'B', 'C', 'D'])

    def test_build(self):
        dt = bicycle.cards.DeckTypeStandard()
        
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
        dt = bicycle.cards.DeckTypeStandard()
        self.assertIsInstance(dt.ranks_index('A'), int)

    def test_suits_index(self):
        dt = bicycle.cards.DeckTypeStandard()
        self.assertIsInstance(dt.suits_index('S'), int)

    def test_get_rank(self):
        dt = bicycle.cards.DeckTypeStandard()
        self.assertIsInstance(dt.get_rank(0), str)

    def test_get_suit(self):
        dt = bicycle.cards.DeckTypeStandard()
        self.assertIsInstance(dt.get_suit(0), str)


class TestCardClass(unittest.TestCase):

    def test_init(self):
        c = bicycle.cards.Card(suit=0, rank=0, up=True, private=False)

        self.assertIsInstance(c.deck_type, bicycle.cards.DeckTypeStandard)
        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_from_str(self):
        c = bicycle.cards.Card.from_str('AC')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 2)

        c = bicycle.cards.Card.from_str('AS')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 0)

        c = bicycle.cards.Card.from_str('AS', up=True, private=False)

        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_eq(self):
        c1 = bicycle.cards.Card.from_str('AS')
        c2 = bicycle.cards.Card.from_str('AS')
        self.assertEqual(c1, c2)

    def test_ne(self):
        c1 = bicycle.cards.Card.from_str('AS')
        c2 = bicycle.cards.Card.from_str('KS')
        self.assertNotEqual(c1, c2)

    def test_lt(self):
        c1 = bicycle.cards.Card.from_str('AS')
        c2 = bicycle.cards.Card.from_str('KC')
        self.assertLess(c1, c2)

    def test_gt(self):
        c1 = bicycle.cards.Card.from_str('AS')
        c2 = bicycle.cards.Card.from_str('KC')
        self.assertLess(c1, c2)

    def test_le(self):
        c1 = bicycle.cards.Card.from_str('AS')
        c2 = bicycle.cards.Card.from_str('KC')
        self.assertLessEqual(c1, c2)

        c3 = bicycle.cards.Card.from_str('KC')
        self.assertLessEqual(c1, c3)

    def test_ge(self):
        c1 = bicycle.cards.Card.from_str('KC')
        c2 = bicycle.cards.Card.from_str('AS')
        self.assertGreaterEqual(c1, c2)

        c3 = bicycle.cards.Card.from_str('AC')
        self.assertGreaterEqual(c1, c3)

    def test_serialize(self):
        c = bicycle.cards.Card.from_str('AS')

        self.assertEqual(c.serialize(), 'XX')
        self.assertEqual(c.serialize(snoop=True), 'AS')

        c = bicycle.cards.Card.from_str('KC', up=True)

        self.assertEqual(c.serialize(), 'KC')

    def test_json(self):
        c = bicycle.cards.Card.from_str('AS')
        self.assertEqual(c.__json__(), 'XX')

        c = bicycle.cards.Card.from_str('KC', up=True)
        self.assertEqual(c.__json__(), 'KC')

    def test_iter(self):
        pass

    def test_repr(self):
        pass


class TestCards(unittest.TestCase):

    def test_init(self):
        h = bicycle.cards.Cards()
        self.assertFalse(h)
        self.assertIsInstance(h, list)
        self.assertEqual(h.initlen, 0)

    def test_serialize(self):
        pass

    def test_repr(self):
        pass


class TestActions(unittest.TestCase):

    def test_build(self):
        d = bicycle.cards.build(bicycle.cards.Cards())
        