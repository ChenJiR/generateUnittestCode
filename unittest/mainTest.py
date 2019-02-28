# coding:utf-8
import unittest
import time
from HTMLTestRunner import HTMLTestRunner
import testCode.TestCreatGoods as TestCreatGoods

def suite():
    CreatGoods = unittest.makeSuite(TestCreatGoods.TestCreatGoods)

    alltest_info = unittest.TestSuite()
    alltest_info.addTest(CreatGoods)

    return alltest_info


if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = '../report/' + now + '_result.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                                title='info后台接口自动化测试报告',
                                description='description:'
                                )
        runner.run(suite())