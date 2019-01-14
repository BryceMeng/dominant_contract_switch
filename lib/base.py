# coding:utf-
import abc
from datetime import datetime


def DATE_FUNC(x): return datetime.strptime(str(x), "%Y%m%d_%H%M")


class DominantContractBase(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, switch_time_list):
        self._switch_time_list = [DATE_FUNC(d) for d in switch_time_list]

    def is_time_in(self, ptime):
        if ptime in self._switch_time_list:
            return True
        else:
            return False

    @abc.abstractmethod
    def is_last_half_an_hour_switch(self, bar):
        pass
