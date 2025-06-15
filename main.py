from client import IBClient
import time
def main():
    
    #context management to make sure the disconnect() is ran when done
    with  IBClient("127.0.0.1", 7497, 5) as client:
        nvda = client.get_stock_contract("NVDA") 
        data = client.requestHistoricalData(99, nvda)
        

        nq = client.get_futures_contract("NQ", expiry="202506")
        data_nq = client.requestHistoricalData(98, nq)

    print(data)
    print(data_nq)


main()
