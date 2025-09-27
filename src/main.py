from client import IBClient
from dbmanagement import DBManager
import logging 


#log = logging.getLogger(__name__)
#logging.basicConfig(level=loggin.DEBUG)

def main():
    
    dbman = DBManager() 
    #context management to make sure the disconnect() is ran when done
    with  IBClient("127.0.0.1", 7497, 1, dbman) as client:
        client.dbconn.init_db() 
        es_data = client.dailyDataRequest("ES", 2) 
        
        dbman.addDailyCandleData("ES", client.data) 



if __name__ == "__main__":

    main()
