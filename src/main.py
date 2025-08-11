from .client import IBClient
from .dbmanagement import DBManager

def main():
    
    dbman = DBManager() 
    #context management to make sure the disconnect() is ran when done
    with  IBClient("127.0.0.1", 7497, 5, dbman) as client:
        client.dbconn.init_db() 



main()
