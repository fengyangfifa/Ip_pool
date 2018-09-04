import time
from multiprocessing import Process
from ip_pool.Getter import Getter
from ip_pool.test_ip import Tester
from ip_pool.setting import *


class Scheduler:
    def schedule_test(self, cycle=TESTER_CYCLE):
        test = Tester()
        while True:
            print('测试器开始运行')
            test.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            test_process = Process(target=self.schedule_test)
            test_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

