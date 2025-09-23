from client import IBClient
from dbmanagement import DBManager
import logging as log

#log.basicConfig(level=log.DEBUG)

def main():
    
    dbman = DBManager() 
    #context management to make sure the disconnect() is ran when done
    with  IBClient("127.0.0.1", 7497, 1, dbman) as client:
        client.dbconn.init_db() 
        es_data = client.dailydataRequest("ES") 
        
        dbman.addDailyCandleData("ES", client.data) 




if __name__ == "__main__":

    main()
