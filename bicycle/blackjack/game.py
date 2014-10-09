"""Blackjack Game.
"""

import bicycle.game
import bicycle.blackjack.card
import bicycle.blackjack.table


class PrepareStep(bicycle.game.WagerGameStepMixin, bicycle.game.PrepareStep):
    """Prepare the game round.
    Allow betting during the `PrepareStep`
    """
    def __init__(self, engine):
        bicycle.game.PrepareStep.__init__(self, engine)
        bicycle.game.WagerGameStepMixin.__init__(self)


class InsuranceStep(bicycle.game.GameStep):
    """Ask the table for insurance.
    """

    __timeout__ = 10

    @property
    def to_execute(self):
        """Execute when the dealer is showing an Ace.
        """

        return self.table.dealer_hand[1] == bicycle.blackjack.card.ace

    def insurance(self, player, amount):
        """
        """

        pass

    def __call__(self):
        """
        """

        return True


class HandActionStepMixin(object):
    """
    """

    @property
    def player(self):
        """
        """

        return self._play_item[0]

    @property
    def hand(self):
        """
        """

        return self._play_item[1]

    def hit(self):
        """
        """

        self.table.deal(self.hand)
        if self.hand.stop is True:
            self.execute()  # Finish step.
        else:
            self.delay()    # Reset timer.


class PlayerStep(HandActionStepMixin, bicycle.game.PlayerStep):
    """
    """

    __timeout__ = 22

    def __init__(self, engine):
        """
        """

        bicycle.game.PlayerStep.__init__(self, engine)
        HandActionStepMixin.__init__(self)

    @property
    def to_execute(self):
        """If the dealer does not have a blackjack, we continue.
        """

        return not self.table.dealer_hand.blackjack

    def next(self):
        """
        """

        n = bicycle.game.PlayerStep.next(self)

        if n is True:
            self.hand.up()
            if self.hand.stop is True:
                self.execute()

        return n

    def stand(self):
        """
        """

        self.execute()

    def double(self):
        """
        """
        # Double the wager here too using self.wager!

        self.hit()
        self.execute()

    def split(self):
        """
        """

        raise NotImplementedError()

    def surrender(self):
        """
        """

        raise NotImplementedError()


class DealerStep(HandActionStepMixin, bicycle.game.GameStep):
    """
    """

    def __init__(self, engine):
        """
        """

        bicycle.game.GameStep.__init__(self, engine)
        HandActionStepMixin.__init__(self)

        self._play_item = self.table.dealer, self.table.dealer_hand

        self.table.dealer_hand.up()

    @property
    def to_execute(self):
        """Execute if 
        """

        return not all([hand.busted for hand in self.table.hands])

    def __call__(self):
        """
        """

        while (int(self.hand) < 17 or
               self.hand.soft is True and int(self.hand) <= 17):
            self.hit()

        return True


class ResolveStep(bicycle.game.WagerGameStepMixin, bicycle.game.ResolveStep):
    """
    """

    __timeout__ = 4

    def __init__(self, engine):
        """
        """

        bicycle.game.ResolveStep.__init__(self, engine)
        bicycle.game.WagerGameStepMixin.__init__(self)

    def __call__(self):
        """
        """

        return True


class StandardBlackjack(bicycle.game.GameState):
    """
    """

    # The Engine will use these wisely.
    __game__ = (PrepareStep,
                bicycle.game.WagerStep,
                bicycle.game.DealStep,
                # InsuranceStep,
                PlayerStep,
                DealerStep,
                ResolveStep,
                bicycle.game.CleanupStep)
    __table__ = bicycle.blackjack.table.BlackjackTable


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved