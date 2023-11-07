import pandas as pd



    
    
def convertCandleDataToDF(response) -> pd.DataFrame:
    # Data should be some json that we got from the OANDA_API class
    
    ohlc = ['o','h','l','c']
    
    data = []
    
    for candle in response[0]['candles']:
        if candle['complete'] == False:
            continue
        else:
            new_dict = {}
            new_dict['time'] = candle['time']
            new_dict['volume'] = int(candle['volume'])
            
            for period in ohlc:
                new_dict[f'{period}'] = float(candle['mid'][period])
                
            if new_dict['o'] < new_dict['c']:
                new_dict['green'] = 1
            else:
                new_dict['green'] = 0
            
        data.append(new_dict)
        
    return pd.DataFrame.from_dict(data)
        











if __name__ == "__main__":
    pass