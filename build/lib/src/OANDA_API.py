from utils.defs import *
import requests


class OANDA_API:

    def __init__(self, api_key, mode) -> None:
        
        self.api_key = api_key
        
        if (mode == 0):
            self.baseURL = "https://api-fxpractice.oanda.com"
        elif (mode == 1):
            self.baseURL = "https://api-fxtrade.oanda.com"

    
    def getAccountID(self) -> str:

        endpoint = self.baseURL + "/v3/accounts"
        header = SECURE_HEADER
        session = requests.Session()

        response = session.get(endpoint, headers=header)
        session.close()

        response = response['accounts'][0] #Select the field we need

        return response #should be a string



if __name__ == "__main__":
    obj = OANDA_API(ACCESS_KEY,0)

    print(obj.getAccountID())


         

        
    
        
