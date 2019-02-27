
import unittest,requests,logging,time
from HTMLTestRunner import HTMLTestRunner


class asd(unittest.TestCase):
    
    def setUp(self):
        
        self.baidu_url = 'dsaf'
    
        self.baiduw_url = 'dsaf'
    
        logging.info('--begin test--')
        
    def tearDown(self):
        logging.info('--end test--')
    
    def test_baidu(self):
        """asd"""
        headers = {}
        data = {'sd': 'd'}
        re = requests.post(url=self.baidu_url, headers=headers, data=data)
        result = re.json()
        print(result)
    
    def test_baiduw(self):
        """asd"""
        headers = {}
        data = {'sd': 'd'}
        re = requests.post(url=self.baiduw_url, headers=headers, data=data)
        result = re.json()
        print(result)
    
    
if __name__ == "__main__":

    suite = unittest.TestSuite()
    
    suite.addTest(asd("test_baidu"))
    
    suite.addTest(asd("test_baiduw"))
    
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = '/' + now + '_result.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                                title='None',
                                description='None'
                                )
        runner.run(suite)
