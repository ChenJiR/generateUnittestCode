# coding:utf-8
import unittest
import time
from HTMLTestRunner import HTMLTestRunner
import os


if __name__ == "__main__":

    path = os.path.split(os.path.realpath(__file__))[0]
    case_path = path + "\\..\\testCode\\"

    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = path + "\\..\\report\\" + now + '_result.html'

    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                                title='info后台接口自动化测试报告',
                                description='description:'
                                )
        suit = unittest.defaultTestLoader.discover(case_path, "asd.py")
        runner.run(suit)
