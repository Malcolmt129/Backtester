import dearpygui.dearpygui as dpg

from backtester.interfaces.viewInterface import IView
from backtester.tradingEngine import TradingEngine

class BacktestView(IView):

    def __init__(self, engine: TradingEngine) -> None:
        self.name = "BacktestView"
        self.tag = "BacktestView" 
        self.engine = engine


    def build(self)  -> None:

        with dpg.child_window(tag=self.tag, show=False):

            with dpg.plot(tag="tag_chart", width=-1, height=-170, crosshairs=True):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Date", time=True, tag="tag_x_axis")

