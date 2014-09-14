import unittest
import bicycle.cards


class TestSuitsRanks(unittest.TestCase):

    def test_cls_NoneList(self):
        n1 = bicycle.cards.NoneList([1,2,3])

        self.assertEqual(n1[0], 1)
        self.assertEqual(n1[1], 2)
        self.assertEqual(n1[2], 3)
        self.assertEqual(n1[None], None)

    def test_cls_Suits(self):
        s = bicycle.cards.Suits()

        self.assertEqual(s, ['S','C','H','D'])
        self.assertEqual(s[None], None)

    def test_cls_Ranks(self):
        r = bicycle.cards.Ranks()

        self.assertEqual(r, ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                              'J', 'Q', 'K'])
        self.assertEqual(r[None], None)


class TestCardClass(unittest.TestCase):

    def test_init(self):
        c = bicycle.cards.Card()

        self.assertIsInstance(c.suits, bicycle.cards.Suits)
        self.assertIsInstance(c.ranks, bicycle.cards.Ranks)
        self.assertIsNone(c.suit)
        self.assertIsNone(c.rank)
        self.assertFalse(c.up)
        self.assertTrue(c.private)

        c = bicycle.cards.Card(suit=0, rank=0, up=True, private=False)

        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_from_str(self):
        c = bicycle.cards.Card.from_str('A')

        self.assertEqual(c.rank, 0)
        self.assertIsNone(c.suit)

        c = bicycle.cards.Card.from_str('AS')

        self.assertEqual(c.rank, 0)
        self.assertEqual(c.suit, 0)

        c = bicycle.cards.Card.from_str('AS', up=True, private=False)

        self.assertEqual(c.suit, 0)
        self.assertEqual(c.rank, 0)
        self.assertFalse(c.private)
        self.assertTrue(c.up)

    def test_eq(self):
        c1 = bicycle.cards.Card.from_str('A')
        c2 = bicycle.cards.Card.from_str('A')
        self.assertEqual(c1, c2)

        c3 = bicycle.cards.Card() # Wild card (for now)
        self.assertEqual(c1, c3)

        c4 = bicycle.cards.Card.from_str('AS')
        self.assertEqual(c1, c4)

        c5 = bicycle.cards.Card.from_str('KS')
        self.assertNotEqual(c1, c5)

    def test_serialize(self):
        c = bicycle.cards.Card()

        self.assertEqual(c.serialize(), 'XX')
        self.assertEqual(c.serialize(snoop=True), '**')

        c = bicycle.cards.Card.from_str('AS')

        self.assertEqual(c.serialize(), 'XX')
        self.assertEqual(c.serialize(snoop=True), 'AS')

        c = bicycle.cards.Card.from_str('KC', up=True)

        self.assertEqual(c.serialize(), 'KC')

    def test_json(self):
        pass

    def test_iter(self):
        pass

    def test_repr(self):
        pass


class TestDeckClass(unittest.TestCase):
    pass


class TestShoeClass(unittest.TestCase):
    pass