
import dearpygui.dearpygui as dpg
from backtester.interfaces.viewInterface import IView
from backtester.tradingEngine import TradingEngine
import datetime, math, random


class DataRetrievalView(IView):


    def __init__(self, engine: TradingEngine) -> None:
        self.name = "DataRetrievalView"
        self.tag = "DataRetrievalView"
        self.engine = engine


    def build(self):
        with dpg.child_window(tag=self.tag, show=False):
            with dpg.group(tag="Paramters", horizontal=False):
                #start text box
                dpg.add_input_text(label="start_box", default_value="dd/mm/yyyy") 
                #end text box
                dpg.add_input_text(label="end_box", default_value="dd/mm/yyyy") 
                #symbol

                dpg.add_input_text(label="symbol_box", default_value="e.g. ES") 
                #timeframe

                    



