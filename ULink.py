#!/usr/bin/env python
import numpy as np
from ULinkBase import ULinkBase

class ULink(ULinkBase):        
    def bet(self,t):
        self.bet_list.clear()
        self.choice.clear()
        for user in self.user_list:
            a = user.guess()
            if a == (0,0):
                continue
            self.pool += a[1]
            self.bet_list[user.num]=a[1]
            self.choice[user.num]=a[0]
        
        self.back_cost -= round(self.pool*self.w,2)
        self.pool -= round(self.pool * self.w,2)
        self.pool_list[t] = self.pool
        self.allowance_list[t] = self.new_cost + self.acc_cost
        self.back_list[t] = self.back_cost
        
    def draw(self,t):
        winsum = 0
        n = 0
        for c in self.choice:
            if self.choice[c] == 1:
                winsum += self.bet_list[c]
        if winsum != 0:
            n = min(self.pool/winsum,8)*100//1/100
        for user in self.user_list:
            if  (user.num in self.choice) and (self.choice[user.num] == 1):
                self.pool -= user.get_profit(n)
            user.new_game()
            user.new_day()
        self.l_list[t]=n
        if self.pool < 0:
            self.diff_cost += abs(self.pool)
            self.pool = 0
        self.df_cost_list[t] = self.diff_cost
        self.cost_list[t] = self.new_cost + self.back_cost + self.acc_cost + self.diff_cost
    
    def capital_change(self):
        for user in self.user_list:
            user.change_money()
    
    def reset_w(self):
        self.w = 0.03
        q = 0.5
        a = list(self.cost_list.values())
        b = np.array(list(self.df_cost_list.values()))
        c = np.diff(b[-min(b.size//2,10):])
        if a != [] and c.size > 0:
            d = max(a[-1]/len(self.user_list)/10,0)
            e = max(c.mean()/1000,0)
            self.w = max(0,min(0.05,q*d+(1-q)*e))
