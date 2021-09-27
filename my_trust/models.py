import math
from random import random,randint

from settings import SESSION_CONFIGS

#import self as self
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from otree.models import subsession, player, participant, session

import settings

author = 'Your name here'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = None
    num_rounds = 20
    roleA = '全能者'
    roleB = '普通者'
    roleA_limit = 5 #全能者的分配人数
    roleB_limit = 7 #普通者的分配人数
    A = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    B = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

roleA_players = 0
roleB_players = 0
ourRound = 1
class Subsession(BaseSubsession):
    def creating_session(self):
        global roleA_players, roleB_players, ourRound
        for player in self.get_players():
            player.participant.vars['hasWin'] = []  # 初始化跨轮次的变量，之后如果赢了就设置一下这个变量
            player.player_round = self.round_number

            if self.round_number > ourRound:
                print('round changed to:', self.round_number)
                roleA_players = 0
                roleB_players = 0
                ourRound = self.round_number

            n = randint(1, 2)
            if n==1:
                player.auto_role = Constants.roleA
                roleA_players += 1
                #print('A+1=',roleA_players)
                if roleA_players > Constants.roleA_limit:
                    roleA_players -= 1
                    roleB_players += 1
                    #print('A-1=', roleA_players)
                    player.auto_role = Constants.roleB
            else:
                player.auto_role = Constants.roleB
                roleB_players += 1
                #print('B+1=', roleB_players)
                if roleB_players > Constants.roleB_limit:
                    roleB_players -= 1
                    roleA_players += 1
                    #print('B-1=', roleB_players)
                    player.auto_role = Constants.roleA
            print('-------***********------->' + str(player.auto_role))

            if player.auto_role == Constants.roleA:
                player.base_amount = 10
            else:
                player.base_amount = 5
            print('===>ROUND:AR:BR',self.round_number,roleA_players,roleB_players)



selected_A_nums = []
selected_B_nums = []
class Group(BaseGroup):
    total_selected_A = models.IntegerField()
    total_selected_B = models.IntegerField()

    def set_payoffs(self):
        selected_A_nums = []
        selected_B_nums = []
        for player in self.get_players():
            selected_AB = player.selected_id
            if selected_AB == 1:
                n = randint(0, 19)
                m = Constants.A[n]
                player.selected_num = m
                i = player.base_amount + m
                selected_A_nums.append(i)
            else:
                n = randint(0, 10)
                m = Constants.B[n]
                player.selected_num = m
                i = player.base_amount + m
                selected_B_nums.append(i)
            player.payoff = player.base_amount + m


        self.total_selected_A = len(selected_A_nums)
        self.total_selected_B = len(selected_B_nums)

        for player in self.get_players():
            selected_AB = player.selected_id
            if selected_AB == 1:#选A
                selected_A_nums.sort()
                print("Asort:",selected_A_nums)
                me = player.payoff.__int__()
                index = selected_A_nums.index(me)
                totalcount = len(selected_A_nums)
                player.player_payoff_index_in_A = totalcount - index
                ###################
                if totalcount == 1:#只有一个人，算赢
                    isMeWin = True
                elif totalcount > 1:
                    if totalcount % 2 == 0:  # 偶数
                        if player.player_payoff_index_in_A <= totalcount / 2:
                            isMeWin = True
                        else:
                            isMeWin = False
                    else:#奇数
                        if player.player_payoff_index_in_A < (totalcount + 1) / 2:
                            isMeWin = True
                        else:
                            isMeWin = False


                if isMeWin:#赢了奖励70元
                    player.player_bonus_in_A = 70
                    player.participant.vars['hasWin'].append(70)
                else:#输了奖励20元
                    player.player_bonus_in_A = 20
                    player.participant.vars['hasWin'].append(20)
                ###################
                player.player_total_points_in_A = player.payoff.__int__()# + player.player_bonus_in_A
                #现在假定反选AB==》#选B
                n = randint(0, 10)
                m = Constants.B[n]
                player.selected_num_temp = m
                i = player.base_amount + m
                temp = selected_B_nums.copy()#这里要COPY一下否则会影响正选的数据乱套了
                temp.append(i)
                temp.sort()
                index = temp.index(i)
                totalcount = len(temp)
                player.player_payoff_index_in_B = totalcount - index
                ###################
                if totalcount == 1:#只有一个人，算赢
                    isMeWin = True
                elif totalcount > 1:
                    if totalcount % 2 == 0:  # 偶数
                        if player.player_payoff_index_in_B <= totalcount / 2:
                            isMeWin = True
                        else:
                            isMeWin = False
                    else:#奇数
                        if player.player_payoff_index_in_B < (totalcount + 1) / 2:
                            isMeWin = True
                        else:
                            isMeWin = False


                if isMeWin:#赢了奖励5元
                    player.player_bonus_in_B = 5
                else:#输了奖励0元
                    player.player_bonus_in_B = 0
                ###################
                player.player_total_points_in_B = i# + player.player_bonus_in_B


            elif selected_AB == 2:
                selected_B_nums.sort()
                print("Bsort:", selected_B_nums)
                me = player.payoff.__int__()
                index = selected_B_nums.index(me)
                totalcount = len(selected_B_nums)
                player.player_payoff_index_in_B = totalcount - index

                ###################
                if totalcount == 1:#只有一个人，算赢
                    isMeWin = True
                elif totalcount > 1:
                    if totalcount % 2 == 0:  # 偶数
                        if player.player_payoff_index_in_B <= totalcount / 2:
                            isMeWin = True
                        else:
                            isMeWin = False
                    else:#奇数
                        if player.player_payoff_index_in_B < (totalcount + 1) / 2:
                            isMeWin = True
                        else:
                            isMeWin = False


                if isMeWin:#赢了奖励70元
                    player.player_bonus_in_B = 70
                    player.participant.vars['hasWin'].append(70)
                else:#输了奖励20元
                    player.player_bonus_in_B = 20
                    player.participant.vars['hasWin'].append(20)
                ###################

                player.player_total_points_in_B = player.payoff.__int__()# + player.player_bonus_in_B
                # 现在假定反选AB==》#选AA
                n = randint(0, 19)
                m = Constants.A[n]
                player.selected_num_temp = m
                i = player.base_amount + m
                temp = selected_A_nums.copy()
                temp.append(i)
                temp.sort()
                index = temp.index(i)
                totalcount = len(temp)
                player.player_payoff_index_in_A = totalcount - index

                ###################
                if totalcount == 1:#只有一个人，算赢
                    isMeWin = True
                elif totalcount > 1:
                    if totalcount % 2 == 0:  # 偶数
                        if player.player_payoff_index_in_A <= totalcount / 2:
                            isMeWin = True
                        else:
                            isMeWin = False
                    else:#奇数
                        if player.player_payoff_index_in_A < (totalcount + 1) / 2:
                            isMeWin = True
                        else:
                            isMeWin = False


                if isMeWin:#赢了奖励5元
                    player.player_bonus_in_A = 5
                else:#输了奖励0元
                    player.player_bonus_in_A = 0
                ###################

                player.player_total_points_in_A = i# + player.player_bonus_in_A







class Player(BasePlayer):
    auto_role = models.StringField()
    base_amount = models.IntegerField()

    student_id = models.StringField(label='你的编号是：')
    student_collage = models.StringField(label='你的学院是：')
    student_age = models.IntegerField(label='你的年龄是：')
    selected_id = models.IntegerField(initial=0,label='请从A、B中选择一个的组数，你的选择得分将是其中的随机数<br/>A(1,2,3...20)<br/>B(5,6...15)', choices=[[1, 'A'], [2, 'B']])
    selected_num = models.IntegerField()

    player_payoff_index_in_A = models.IntegerField()
    player_payoff_index_in_B = models.IntegerField()
    player_bonus_in_A = models.IntegerField()
    player_bonus_in_B = models.IntegerField()

    player_total_points_in_A = models.IntegerField(initial=0)
    player_total_points_in_B = models.IntegerField(initial=0)

    selected_num_temp = models.IntegerField()

    player_round = models.IntegerField(initial=0)


    # def role(self):
    #     n = randint(1, 2)
    #     print(n)
    #     if n == 1:
    #         return Constants.roleA
    #     elif n == 2:#self.id_in_group
    #         return Constants.roleB