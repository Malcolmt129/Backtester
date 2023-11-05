import unittest
from src.OANDA_API import *
from utils.defs import *


class TestOANDA_API(unittest.TestCase) :

    practice = OANDA_API(ACCESS_KEY,0) # Use this for testing with practice endpoint
    live = OANDA_API(ACCESS_KEY,1) # Use this for testing with live endpoint
    
    
    def test_initPractice(self):

        expected_URL = "https://api-fxpractice.oanda.com"
        actual = self.practice.baseURL
        self.assertEqual(actual,expected_URL)

    def test_initLive(self):

        expected_URL = "https://api-fxtrade.oanda.com"
        actual = self.live.baseURL
        self.assertEqual(actual,expected_URL)
    
    def test_getAccountID(self):

        expected = ACCOUNT_ID
        actual = self.practice.getAccountID()
        self.assertEqual(actual,expected)

        


    

