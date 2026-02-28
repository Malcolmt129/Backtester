from abc import ABC, abstractmethod

class IDatabase(ABC):
    
    @abstractmethod
    def __init__(self, db_name:str):
        pass

    @abstractmethod
    def __exit__(self):
        pass

    @abstractmethod
    def init_db(self):
        pass
    
    @abstractmethod
    def execQuery(self, query, params):
        pass
   
   
    #This will be to populate the schema to be used for queries
    @abstractmethod
    def _getSchema():
        pass
    
