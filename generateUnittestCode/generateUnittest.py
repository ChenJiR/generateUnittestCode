from string import Template


def singleUrlCreate(MethodList):
    code = Template('''
        self.${testcase}_url = '${url}'
    ''')

    string = code.substitute(testcase=MethodList["testcase"], url=MethodList['url'])
    return string


def urlListCreate(MethodParaList):
    string = ""
    for MethodPara in MethodParaList:
        string = string + singleUrlCreate(MethodParaList[MethodPara])
    return string


def singleMethodCreate(MethodList):
    code = Template('''
    def test_${testcase}(self):
        """${testcaseName}"""
        
        url = self.${testcase}_url
        ${submitList}
    ''')

    string = code.substitute(testcase=MethodList["testcase"], testcaseName=MethodList["TestcaseName"],
                             method=MethodList['method'],
                             submitList=submitCreate(MethodList['submit'], MethodList['method']))
    return string


# 拼接单个的测试用例函数字符串为完整字符串并传回主函数
# MethodParaList获取测试用例部分list
def methodCreate(MethodParaList):
    string = ""
    for MethodPara in MethodParaList:
        string = string + singleMethodCreate(MethodParaList[MethodPara])
    return string


def singleSubmitCreate(SubmitPara, method):
    code = Template('''
        headers = $headers
        data = $data
        re = requests.$method(url=url, headers=headers, data=data)
        result = re.json()
        print(result)
        ''')

    string = code.substitute(headers=SubmitPara['headers'], data=SubmitPara['params'], method=method)
    return string


def submitCreate(SubmitList, method):
    string = ""
    for submit in SubmitList:
        string = string + singleSubmitCreate(SubmitList[submit], method)
    return string


# 构造单个测试集
def singleTestsuitCreate(MethodList, parameters):
    code = Template('''
    suite.addTest(${className}("test_${testcase}"))
    ''')
    string = code.substitute(testcase=MethodList["testcase"], className=parameters['className'])
    return string


# 添加测试集
def addtestsuit(MethodParaList, parameters):
    string = ""
    for MethodPara in MethodParaList:
        string = string + singleTestsuitCreate(MethodParaList[MethodPara], parameters)
    return string


# 生成测试用例类函数字符串
def modelClassCreate(parameters, generateDirName='testCode'):
    code = Template('''
import unittest,requests,logging,time
from HTMLTestRunner import HTMLTestRunner


class ${className}(unittest.TestCase):
    
    def setUp(self):
        ${url_list}
        logging.info('--begin test--')
        
    def tearDown(self):
        logging.info('--end test--')
    ${model}    
if __name__ == "__main__":

    suite = unittest.TestSuite()
    ${testsuite}
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = '${report_file_path}/' + now + '_result.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                                title='${report_file_title}',
                                description='${report_file_description}'
                                )
        runner.run(suite)
''')
    fileStr = code.substitute(className=parameters['className'],
                              testsuite=addtestsuit(parameters['testCaseList'], parameters),
                              url_list=urlListCreate(parameters['testCaseList']),
                              model=methodCreate(parameters['testCaseList']),
                              report_file_path=parameters['report_file_path'] or '',
                              report_file_title=parameters['report_file_title'] or None,
                              report_file_description=parameters['report_file_description'] or None)
    f = open(generateDirName + '/' + parameters['className'] + ".py", 'w')
    f.write(fileStr)
    f.close()
