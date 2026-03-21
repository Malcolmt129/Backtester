import dearpygui.dearpygui as dpg
from backtester.interfaces.viewInterface import IView
from backtester.tradingEngine import TradingEngine
import datetime, math, random


class PortfolioView(IView):


    def __init__(self, engine: TradingEngine) -> None:
        self.name = "PortfolioView"
        self.tag = "PortfolioView"
        self.engine = engine


    def build(self):
        with dpg.child_window(tag=self.tag, show=False):
            with dpg.group(tag="Account and Positions", horizontal=True):
                self.make_accountTable() 
                self.make_positionTable()

            self.make_graph()
    

    def make_accountTable(self):
        
        # Need to cap the width of shit so that it doesn't take up all of the space 
        # This is also something that happens in CSS
        with dpg.table(tag="Account Banner", width=300) as table:

            #Remember: If there is no columns defined, the table wont render...
            dpg.add_table_column(label="Metric")
            dpg.add_table_column(label="Value")
            for label, value in [
                    ("Account Size",    f"${getAccountValue():,.2f}"),
                    ("Unrealized P&L",  f"${getUPL():,.2f}"),
                    ("Realized P&L",    f"${getRPL():,.2f}"),
                    ("Buying Power",    f"${getBuyingPower():,.2f}"),
                    ]:
                with dpg.table_row():
                    dpg.add_text(label)
                    dpg.add_text(value)
        return table
    

    def make_positionTable(self):

        with dpg.table(tag="Postions", 
                       borders_outerH=True, borders_outerV=True) as table:

            dpg.add_table_column(label="Symbol")
            dpg.add_table_column(label="Qty")
            dpg.add_table_column(label="Last")
            dpg.add_table_column(label="Mkt Value")
            dpg.add_table_column(label="Unr. P&L")
            dpg.add_table_column(label="Allocation")

        return table


    def make_graph(self):

        with dpg.plot(tag="Portfolio Performance", width=-1, height=-550, crosshairs=True) as plot:
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Date", time=True, tag="x_axis")
            with dpg.plot_axis(dpg.mvYAxis, label="Percent", tag="y_axis"):
                xs, ys = _fake_equity_curve()
                dpg.add_line_series(xs, ys, label="Portfolio", parent="y_axis")

        return plot

    def make_portfolioAllocationGraph(self):

       pass 

def _fake_equity_curve():
    """Generate ~1 year of daily percent-return data ending today."""
    random.seed(42)
    end = datetime.date(2026, 3, 18)
    start = end - datetime.timedelta(days=365)
    xs, ys = [], []
    pct = 0.0
    day = start
    while day <= end:
        if day.weekday() < 5:  # weekdays only
            pct += random.gauss(0.04, 0.8)  # slight upward drift
            xs.append(datetime.datetime(day.year, day.month, day.day).timestamp())
            ys.append(pct)
        day += datetime.timedelta(days=1)
    return xs, ys



def getAccountValue():

    return 1800000

def getUPL():
    return 24042.23

def getRPL():
    return 104072.46

def getBuyingPower():
    return 674124.69
