import requests
from utils.defs import *
from utils.timeFormatHandler import *
import DataFraming




class OANDA_API:

    def __init__(self, api_key, mode) -> None:
        
        self.api_key = api_key
        self.instruments = {}
        if (mode == 0):
            self.baseURL = "https://api-fxpractice.oanda.com"
        elif (mode == 1):
            self.baseURL = "https://api-fxtrade.oanda.com"

        self.header = {'Authorization': f'Bearer {api_key}'} 

    
    def getAccountID(self) -> str:

        endpoint = self.baseURL + "/v3/accounts"
        session = requests.Session()

        message = session.get(endpoint, headers=self.header)
        session.close()

        response = message.json() 
        
        id = response['accounts'][0]['id'] #Select the field we need
        
        return id #should be a string
    
    
    def getFullAccountDetails(self) -> dict:

        id = self.getAccountID()
        endpoint = self.baseURL + "/v3/accounts/" + id
        session = requests.Session()
        message = session.get(endpoint, headers=self.header)
        session.close()

        response = message.json()

        return response, message
    
    
    def getChangesSince(self, transID):

        id  = self.getAccountID()
        endpoint = self.baseURL + f"/v3/accounts/{id}/changes"
        
        payload = {'Accept-Datetime-Format': 'RFC3339', 
                   'sinceTransactionID': transID}
        
        session = requests.Session()

        message = session.get(endpoint,
                              headers=self.header,
                              params=payload)
        session.close()

        response = message.json()

        return response, message



#####################################################################
#                                                                   #    
#       Instrument Endpoints                                        #
#                                                                   #
#####################################################################

    # Need more Unit tests on this
    def fetchCandleStickData(self, instrument, granularity,startTime,endTime):
        
        if instrument in self.instruments:
        
            endpoint = self.baseURL + f"/v3/instruments/{instrument}/candles"

            payload = { 
                'granularity': granularity,
                'from': startTime,
                'to': endTime
                }
        
            session = requests.Session()
            
            message = session.get(endpoint, headers=self.header, 
                                  params=payload)
            session.close()
            response = message.json()

            return response,message
        else:
            return "Can not get data on this instrument"
    
    # Maybe need to add more situational fetches later. For right now,
    # this is good enough.
    
    def getTradableInstruments(self) -> dict:
        
        id = self.getAccountID()
        endpoint = self.baseURL + f"/v3/accounts/{id}/instruments"

        session = requests.Session()
        message = session.get(endpoint, headers=self.header)
        session.close()

        response = message.json()
        
        for instrument in response['instruments']:
            data = [instrument['pipLocation'],instrument['displayPrecision']]
            self.instruments[instrument['name']] = data
            
        self.instruments = dict(sorted(self.instruments.items()))
        return response, message


    



if __name__ == "__main__":
    practice_obj = OANDA_API(ACCESS_KEY,0)
    live_obj = OANDA_API(LIVE_ACCESS_KEY,1)
    

    
    
    


         

        
    
        
