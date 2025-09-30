from client import IBClient
from dbmanagement import DBManager
from dbento import DataBento
import logging 


#log = logging.getLogger(__name__)
#logging.basicConfig(level=loggin.DEBUG)

def main():
    
    dbman = DBManager() 
    dbentoClient = DataBento() 


    data = dbentoClient.requestDailyFutureData("ES.c.0", "20250101", "20250131")


    dbman.addDailyCandleData("ES.c.0", data)


if __name__ == "__main__":

    main()
