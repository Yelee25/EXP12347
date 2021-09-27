from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):

    def vars_for_template(self):
        return {
            'redemption_code': self.participant.label or self.participant.code,
            'eur': self.participant.payoff_plus_participation_fee()
        }

page_sequence = [PaymentInfo]
