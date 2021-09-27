from random import random, randint

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class FinalPage(Page):
    def vars_for_template(self):
        m = len(self.player.participant.vars['hasWin']) - 1
        n = randint(0, m)
        r = self.player.participant.vars['hasWin'][n]
        return {'randombona': r}
    def is_displayed(self):
        return self.round_number == 20
class PlayerInfo(Page):
    form_model = 'player'
    form_fields = ['student_id','student_collage','student_age']
    def is_displayed(self):
        return self.round_number == 1
    def app_after_this_page(self, upcoming_apps):
        #self.player.participant.vars.student_id = self.player.student_id#跨伦次保存变量
        self.player.participant.vars['student_id'] = self.player.student_id
        # if self.round_number == 1:
        #     # player.participant.vars.student_id = 111222222222222
        #     player.participant.vars['student_id'] = player.student_id


class SelectAB(Page):
    timeout_seconds = 180  # 页面限制3分钟
    form_model = 'player'
    form_fields = ['selected_id']


class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1

class WaitForP1(WaitPage):
    pass

class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return dict(
            tripled_amount=self.group.sent_amount * self.group.multiplication_factor
        )

class ResultsWaitPage(WaitPage):
    #group_by_arrival_time = True
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass
    # def vars_for_template(self):
    #     return {'selected_A_nums': selected_A_nums, 'selected_B_nums': selected_B_nums}

# page_sequence = [Send, WaitForP1, SendBack, ResultsWaitPage, Results]

page_sequence = [PlayerInfo, SelectAB, ResultsWaitPage, Results, FinalPage]
