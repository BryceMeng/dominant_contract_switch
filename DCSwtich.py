# encoding: UTF-8
"""
2019.01.07 负责主力合约切换相关功能

https://github.com/mhxueshan/dominant_contract_switch

"""
from rb import SHFE_RB

CLASS_DIC = {"SHFE.RB": SHFE_RB}


class DCSwitch(object):

    def __init__(self, symbol):
        """
        init
        :param symbol: 品种 SHFE.RB.bar.60
        """
        t1 = symbol.index(".")
        t2 = symbol[t1 + 1:].index(".")
        key = symbol[:t1 + t2 + 1]

        self.handler = CLASS_DIC[key]() if key in CLASS_DIC else None

    def is_last_half_an_hour_switch(self, bar):

        return self.handler.is_last_half_an_hour_switch(bar)

    def is_switch_time_and_sign(self, bar):
        """
        判断symbol品种在time这个时刻
        :param bar: k线
        :return: true/false
        """

        ret = self.handler.is_time_in(bar.datetime)

        if ret:
            bar.__dict__[DCSwitch.SIGN] = True

        return ret



