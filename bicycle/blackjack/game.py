"""
"""

import itertools

import bicycle.game
import bicycle.blackjack.card
import bicycle.blackjack.table


# Allow betting during the prep step.
class PrepareStep(bicycle.game.WagerGameStepMixin, bicycle.game.PrepareStep):
    def __init__(self, engine):
        bicycle.game.PrepareStep.__init__(self, engine)
        bicycle.game.WagerGameStepMixin.__init__(self)


class InsuranceStep(bicycle.game.GameStep):
    """
    """

    __timeout__ = 10

    @property
    def to_execute(self):
        return self.table.dealer_hand[1] == bicycle.blackjack.card.ace

    def insurance(self, player, amount):
        pass

    def __call__(self):
        return True


class HandActionStepMixin(object):
    """
    """

    @property
    def player(self):
        return self._play_item[0]

    @property
    def hand(self):
        return self._play_item[1]

    # def _correlate(self, player):
    #     """Ensure only the current player is acting.
    #     """
    #     # This kind of check might be better done elsewhere.
    #     if player is not self.player:
    #         raise bicycle.game.CannotAct()

    # Player Actions
    # ==============
    def hit(self):
        """
        """
        self.table.deal(self.hand)
        self.engine.set_timer()


# Some pieces here can moved back in to bicycle.game.
class PlayerStep(HandActionStepMixin, bicycle.game.PlayerStep):
    """
    Iterates through 
    """

    __timeout__ = 60

    def __init__(self, engine):
        bicycle.game.PlayerStep.__init__(self, engine)
        HandActionStepMixin.__init__(self)

    @property
    def to_execute(self):
        """If the dealer does not have a blackjack, we continue.
        """

        return not self.table.dealer_hand.blackjack

    def next(self):
        n = bicycle.game.PlayerStep.next(self)

        if n is True:
            if self.hand.stop is True:
                self.engine.execute_step()

        return n

    def stand(self):
        """
        """
        self.engine.execute_step()

    def double(self, player):
        """
        """
        # Double the wager here too using self.wager!

        self.hit(player)
        self.engine.execute_step()

    def split(self, player):
        """
        """

        raise NotImplementedError()

    def surrender(self, player):
        """
        """

        raise NotImplementedError()


class DealerStep(HandActionStepMixin, bicycle.game.GameStep):
    """
    """

    __timeout__ = 0
    to_execute = True

    def __init__(self, engine):
        """
        """
        bicycle.game.GameStep.__init__(self, engine)
        HandActionStepMixin.__init__(self)

        self._play_item = self.table.dealer, self.table.dealer_hand

    def __call__(self):
        """
        """
        self.table.dealer_hand.up()

        while (int(self.hand) < 17 or
               self.hand.soft is True and int(self.hand) <= 17):
            self.hit()

        return True


class ResolveStep(bicycle.game.ResolveStep):
    """
    """

    def __init__(self, engine):
        bicycle.game.ResolveStep.__init__(self, engine)

    def __call__(self):
        return True


class StandardBlackjack(bicycle.game.GameState):
    """
    """

    # The Engine will use these wisely.
    __game__ = (PrepareStep,
                bicycle.game.WagerStep,
                bicycle.game.DealStep,
                InsuranceStep,
                PlayerStep,
                DealerStep,
                ResolveStep,
                bicycle.game.CleanupStep)
    __table__ = bicycle.blackjack.table.BlackjackTable


# (c) 2011-2014 StudioCoda & Nicholas Long. All Rights Reserved