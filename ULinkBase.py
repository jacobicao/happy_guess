import matplotlib.pyplot as plt
import numpy as np

class ULinkBase:
    def __init__(self,w,y):
        self.new_cost = 0  # 新人补贴
        self.acc_cost = 0  # 加速券补贴
        self.back_cost = 0  # 累计抽成
        self.diff_cost = 0  # 奖金池派奖差额
        self.pool = 0
        self.user_list = []
        self.bet_list = dict()
        self.choice = dict()
        self.pool_list = dict()
        self.l_list = dict()
        self.cost_list = dict()
        self.df_cost_list = dict()
        self.back_list = dict()
        self.allowance_list = dict()
        self.w = w
        self.y = y
        self.dd = 1
    def Attach(self,new_user):
        self.user_list.append(new_user)
        
    def add_new_cost(self,v):
        self.new_cost += v
    
    def add_acc_cost(self,v):
        self.acc_cost += v*(self.y-0.0365)/365*10000
    
    def printUserFund(self):
        for user in self.user_list:
            print(user)
            
    def show_plot(self):
        plt.show()
        
    def plot_user_fund(self):
        plt.figure(3)
        user_fund = []
        for user in self.user_list:
            user_fund.append(user.yesterday)
        plt.hist(user_fund,bins=30)
        plt.title('Hist of user fund')

    def plot_pool(self):
        plt.figure(1)
        plt.plot(list(self.pool_list.keys()),list(self.pool_list.values()))
        plt.title('Pool')
        plt.xlabel('Days')

    def plot_user(self,R):
        plt.figure(4)
        plt.plot(np.array(R).cumsum())
        plt.title('User number')
        plt.xlabel('Days')

    def plot_total_cost(self):
        plt.figure(2)
        plt.plot(list(self.cost_list.keys()),list(self.cost_list.values()),label='Total')
        plt.plot(list(self.df_cost_list.keys()),list(self.df_cost_list.values()),label='Arbitrage')
        plt.plot(list(self.back_list.keys()),list(self.back_list.values()),label='Commission',color='k')
        plt.plot(list(self.allowance_list.keys()),list(self.allowance_list.values()),label='Allowance')
        plt.title('Cost analyze')
        plt.xlabel('Days')
        plt.legend()

    def sata_change_user(self):
        a = 0
        for c in self.user_list:
            if c.like_change == 1:
                a +=1
        return a/len(self.user_list)
