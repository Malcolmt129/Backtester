from client import IBClient
from dbmanagement import DBManager
from dbento import DataBento
import logging

from charter import Charter 


#log = logging.getLogger(__name__)
#logging.basicConfig(level=loggin.DEBUG)

def main():
    
    dbman = DBManager() 
    dbentoClient = DataBento() 
    chart = Charter()

    data = dbentoClient.requestDailyFutureData("ES", "20250101", "20250930")
    

    adjData = dbentoClient.backAdjustData(data)

    chart.showBackAdjVUnadj(data, adjData)

    #dbman.addDailyCandleData("ES", data)

    #dbman.getDailyCandleDataFromDB("20250101", "20250131")


if __name__ == "__main__":

    main()
