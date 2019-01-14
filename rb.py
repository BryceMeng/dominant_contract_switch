# coding:utf-8
"""
TradeBlazer rb品种主力合约(rb888)的主力切换日期，供回测使用
时间从分钟线中提取，所以在list当中的时间对应的分钟线是一定存在的
注意：并非官方数据，不保证准确性

20150101 之前的数据取的是openInterest隔夜增加5%以上的数据
20150101 之后的数据取的是openInterest隔夜增加1.8%以上的数据，然后人工去除了20160308的一条数据
"""

from lib.base import DominantContractBase
from datetime import datetime, timedelta


class SHFE_RB(DominantContractBase):

    switch_time_list = [
        "20090720_0900", "20090810_0900", "20090901_0900", "20091012_0900", "20091110_0900", "20091201_0900",
        "20100309_0900", "20101014_0900",
        "20110210_0900", "20110808_0900", "20111103_0900",
        "20120302_0900", "20120712_0900", "20121023_0900",
        "20130219_0900", "20130704_0900", "20131031_0900",
        "20140305_0900", "20140708_0900", "20141021_0900",
        # 夜盘开始
        "20150311_2100", "20150720_2100", "20151104_2100",
        "20160311_2100", "20160817_2100", "20161125_2100",
        "20170322_2100", "20170807_2100", "20171108_2100",
        "20180328_2100", "20180816_2100", "20181129_2100",
    ]

    def __init__(self):
        super(SHFE_RB, self).__init__(SHFE_RB.switch_time_list)

    def is_last_half_an_hour_switch(self, bar):
        """
        2014.12.26 21:00 开始夜盘 21:00~1:00
        http://www.shfe.com.cn/news/notice/911321750.html
        2016.5.3 调整时间 21:00~23:00
        http://www.shfe.com.cn/news/notice/911325006.html
        :param bar:
        :return:
        """
        if bar.datetime > datetime(year=2014, month=12, day=26) and bar.datetime.hour == 14 and bar.datetime.minute > 30:
            # 2015年后从21点开始
            switch_time = datetime(year=bar.datetime.year, month=bar.datetime.month, day=bar.datetime.day, hour=21)
            return self.is_time_in(switch_time), switch_time
        elif bar.datetime < datetime(year=2014, month=12, day=26) and bar.datetime.hour == 14 and bar.datetime.minute > 30:
            # 2015年前
            switch_time = (bar.datetime + timedelta(days=1)).replace(hour=9,minute=0,second=0,microsecond=0)
            return self.is_time_in(switch_time), switch_time
        else:
            return False, None


if __name__ == "__main__":
    rb = SHFE_RB()
    print rb._switch_time_list