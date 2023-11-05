from datetime import datetime
from dateutil import tz
import pytz

# This is used in the backtester
def localizeAndISOtime(date):
    newDate = datetime.strptime(date, '%Y-%m-%d')
    newDate = newDate.astimezone(tz.gettz("America/New_York"))
    newDate = datetime.timestamp(newDate)
    
    return newDate


# The format that they come in is 2023-01-31T13:30:00-04:00
def localizeAndISOtimeHMS(date):
    newDate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    newDate = newDate.astimezone(tz.gettz("America/New_York"))
    newDate = datetime.timestamp(newDate)
    
    return newDate



# Could be used in other places later

def localizeAndISOtimeHM(date):

    #The format that date should come in is 2023-01-31T13:30-04:00
    newDate = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    newDate = newDate.astimezone(tz.gettz("America/New_York"))
    newDate = datetime.timestamp(newDate)
    
    return newDate

def localizeTimeFromOANDA(date):
    
    newDate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f000Z')
    newDate = newDate.astimezone(tz.gettz("America/New_York"))
    newDate = datetime.timestamp(newDate)
    
    return newDate

if __name__ == "__main__":
    pass