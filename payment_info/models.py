from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class Constants(BaseConstants):
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass
    # def creating_session(self):
    #     # Ticketnumber
    #     for p in self.get_players(self):
    #         self.tn = self.participant.vars['tn']

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass
    # tn = models.IntegerField(min=0, max=999999)


