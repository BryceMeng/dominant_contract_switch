# encoding: UTF-8
"""
分析tb分钟线数据中的主力切换点

https://github.com/mhxueshan/dominant_contract_switch

其中VtBarData引用于Vnpy项目

"""
import os
from datetime import datetime

EMPTY_STRING = ""
EMPTY_FLOAT = 0.0
EMPTY_INT = 0

TB_MIN_FILE = "./data/rb888_1分钟.csv"


class VtBarData(object):
    """K线数据"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(VtBarData, self).__init__()

        self.vtSymbol = EMPTY_STRING        # vt系统代码
        self.symbol = EMPTY_STRING          # 代码
        self.exchange = EMPTY_STRING        # 交易所

        self.open = EMPTY_FLOAT             # OHLC
        self.high = EMPTY_FLOAT
        self.low = EMPTY_FLOAT
        self.close = EMPTY_FLOAT

        # 2018.6.20 方便和tick.lastPrice，这样有些函数就可以通用
        self.lastPrice = EMPTY_FLOAT

        self.date = EMPTY_STRING            # bar开始的时间，日期
        self.time = EMPTY_STRING            # 时间
        self.datetime = None                # python的datetime时间对象

        self.volume = EMPTY_INT             # 成交量
        self.openInterest = EMPTY_INT       # 持仓量


def line2bar(line):

    splits = line.strip().split(",")

    bar = VtBarData()
    bar.datetime = datetime.strptime(splits[0] + " " + "%d" % int(float(splits[1])*10000), "%Y%m%d %H%M")
    bar.date = bar.datetime.strftime("%Y%m%d")
    bar.time = bar.datetime.strftime("%H:%M")

    bar.open = float(splits[2].strip())
    bar.high = float(splits[3].strip())
    bar.low = float(splits[4].strip())
    bar.close = float(splits[5].strip())
    bar.volume = int(splits[6].strip())
    bar.openInterest = int(splits[7].strip())

    return bar


def analysis_file(file_path):

    if not os.path.exists(file_path):
        print "%s not exist" % file_path
        return False

    pre_bar = None

    for line in open(file_path, "r"):
        cur_bar = line2bar(line)

        if pre_bar is not None and pre_bar.datetime.hour < 21 and cur_bar.datetime.hour == 21 and cur_bar.datetime.minute < 6:
            if abs((cur_bar.openInterest - pre_bar.openInterest)/float(pre_bar.openInterest)) > 0.018 and \
                    abs((pre_bar.close - cur_bar.open)/float(cur_bar.open)) > 0.00:
                print "may be contract swich"
                print pre_bar.__dict__
                print cur_bar.__dict__
                print "*"*50

        pre_bar = cur_bar


if __name__ == "__main__":
    print analysis_file(TB_MIN_FILE)
