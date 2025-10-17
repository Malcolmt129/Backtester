import plotly.graph_objects as go 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


class Charter():

    def __init__(self):
        
        pass

    

    def showBackAdjVUnadj(self, unadj: pd.DataFrame, adj: pd.DataFrame): 
    
        plt.figure(figsize=(12, 6))
        
        # Unadjusted price series
        plt.plot(unadj["ts_event"], unadj["mid"], label="Unadjusted", alpha=0.6)
        
        # Adjusted price series
        plt.plot(adj["ts_event"], adj["mid"], label="Back-Adjusted", linewidth=2)

        plt.title("Futures Prices: Adjusted vs Unadjusted")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        



