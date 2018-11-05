#!/usr/bin/env python
import numpy as np

class Simu_user:
    def __init__(self, T, p0=[10000, 0.16, 3]):
        self.p0 = p0
        self.T = T
    
    def diff_logist(self,t,p):
        n,k,b=p
        d = k*t-b
        return ((1+np.exp(d))**(-2)*np.exp(d)*k*n).astype(int)
    
    def simu(self,i):
        return (self.diff_logist(np.arange(self.T), self.p0)*i).tolist()


class Counter:
    count = 0
 
    
class Observer(Counter):
    def __init__(self, fund, p, k, b, strsub):
        self.first = 1
        Counter.count += 1
        self.num = Counter.count
        self.fund = fund
        self.yesterday = fund
        self.today_dyn = 0
        self.buy_acc = 0
        self.p = p
        self.k = k
        self.sub = strsub
        self.sub.Attach(self)
        self.like_change = 0
        self.recast = 0
        if np.random.binomial(1,b) == 1:
            self.like_change = 1
        self.cheat = 0

    def new_day(self):
        if self.recast == 1:
            self.recast = 0
            return
        self.today_dyn = 0

    def new_game(self):
        self.buy_acc = 0

    def __repr__ (self):
        return 'User %d: %5.2f'%(self.num,self.fund)


class User(Observer):
    def guess(self):
        if self.cheat > 3:
            return (0,0)
        a = 0
        if self.first == 1:
            self.today_dyn += 0.03
            self.sub.add_new_cost(0.03*self.yesterday/365)
            self.first = 0

        if self.like_change == 1 and self.fund < 2000:
            self.buy_acc = self.yesterday//1000/10
            self.sub.add_acc_cost(self.buy_acc)
            self.today_dyn += self.sub.y + 0.02
            a = self.today_dyn*self.yesterday/365
            return (np.random.randint(1,4), a)

        self.today_dyn += np.random.randint(0,3)/100
        a = self.today_dyn*self.yesterday/365
        if np.random.binomial(1,self.p) == 1:
            self.buy_acc = self.yesterday//1000/10
            self.sub.add_acc_cost(self.buy_acc)
            self.today_dyn += self.sub.y
            a += self.sub.y * self.yesterday / 365
            if a == 0:
                return (0,0)
        return (np.random.randint(1,4), a)

    def get_profit(self,n):
        if self.today_dyn < 0.01:
            return 0
        if np.random.binomial(1,self.k) == 0 or self.like_change == 1:
            if self.like_change == 1 and self.fund > self.yesterday:
                self.cheat += 1
            self.recast = 0
            a = n*self.today_dyn*self.fund/365*100//1/100
            self.fund += a
            self.yesterday = self.fund
            return a
        else:
            self.today_dyn *= n
            self.recast = 1
            return 0

    def change_money(self):
        if self.like_change == 0:
            return
        if self.fund>=26000:
            self.fund = 1000
            return
        b = 29000
        self.fund += b
