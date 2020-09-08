# @Author: Saco Song
# @Time: 2020/9/8-11:33 上午
# @Description:
from math import floor
from random import random

from Common import snowflake


class ImportDailyAndOvertimeRelatedData:
    def lets_see_snow(self):
        snow = snowflake.Generator(worker_id=floor(random() * 32))
        flake = snow.generate()
        print(flake)


if __name__ == '__main__':
    show = ImportDailyAndOvertimeRelatedData()
    show.lets_see_snow()
