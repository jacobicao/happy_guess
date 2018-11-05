#!/usr/bin/env python
'''
本程序考虑了：
1. 首日参加竞猜根据本金的补贴
2. 有些人经常变动本金
3. 有些人会买加速券参加竞猜
4. 参加竞猜的人投的动态加息率服从{0,1,2}的三点等权分布
5. 中奖用户复投率固定

未考虑：
1. 新用户1000元体验金
'''
from ULink import ULink
from User import User, Simu_user
# 抽成率
w = 0.03
# 首日本金补贴率
y = 0.038
# 人均资本
C = 3000
# 购买加速券比例
p_buy_acc = 0.1
# 作弊者出现概率
p_change = 0.03
# 复投率
p_k = 0.1
# 时间长度
T = 100

if __name__ == "__main__":
    ulink = ULink(w,y)
    R = Simu_user(T).simu(2)
    for t in range(0,T):
        for tt in range(0,R[t]):
            User(C, p_buy_acc, p_k, p_change, ulink)
        ulink.bet(t)
        ulink.capital_change()
        ulink.reset_w()
        ulink.draw(t)
    
#    ulink.plot_pool()
#    ulink.plot_user(R)
    ulink.plot_total_cost()
#    ulink.plot_user_fund()
#    ulink.printUserFund()
    ulink.show_plot()
