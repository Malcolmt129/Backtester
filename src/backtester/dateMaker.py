from datetime import datetime
import pytz

def formatFromString(input: str):
   pass


def isDateTimeObj(input):
    return isinstance(input, datetime)



def localizeTime(timeStamp: str):
    tz = pytz.timezone('America/New_York')
    # directly get a TZ-aware datetime in New York
    dt = tz.localize(datetime.fromtimestamp(int(timeStamp)))
    return dt

def localizeTime_Ymmdd(timeStamp: str):
    
    tz = pytz.timezone('America/New_York')
    dt = datetime.strptime(timeStamp, "%Y%m%d").replace(tzinfo=tz)
    epoch_time = dt.timestamp() 
    return epoch_time 

#def _createDateObjFromString(self, input: str):
    #return date.fromisoformat(input)

