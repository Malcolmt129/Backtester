import unittest
from src.OANDA_API import *
from utils.defs import *


class TestOANDA_API(unittest.TestCase) :

    practice = OANDA_API(ACCESS_KEY,0) # Use this for testing with practice endpoint
    live = OANDA_API(LIVE_ACCESS_KEY,1) # Use this for testing with live endpoint
    
    
    def test_initPractice(self):

        expected_URL = "https://api-fxpractice.oanda.com"
        actual = self.practice.baseURL
        self.assertEqual(actual,expected_URL)

    def test_initLive(self):

        expected_URL = "https://api-fxtrade.oanda.com"
        actual = self.live.baseURL
        self.assertEqual(actual,expected_URL)
    
    def test_getAccountID(self):

        id = self.practice.getAccountID()
        self.assertEqual(id,ACCOUNT_ID_PRACTICE)
    

        
    def test_getFullAccountDetails(self):

        code = self.practice.getFullAccountDetails()[1] #Take the second param of what is being returned
        self.assertEqual(200,code.status_code)


    def test_getTradableInstruments(self):
        instruments = self.live.getTradableInstruments()[1]
        self.assertEqual(200,instruments.status_code)


    def test_getChangesSince(self):
        changes = self.live.getChangesSince(20)[1]
        self.assertEqual(200,changes.status_code)

    
    def test_fetchCandleStickData(self):

        starttime = localizeAndISOtime('2023-10-30')
        endtime = localizeAndISOtime('2023-10-31')

        candles = self.live.fetchCandleStickData("EUR_USD", "H4", starttime,endtime)[1]

        self.assertEqual(200, candles.status_code)

    

