import dearpygui.dearpygui as dpg
from backtester.gui.views.dr_view import DataRetrievalView
from backtester.gui.views.portfolio import PortfolioView
from backtester.tradingEngine import TradingEngine
from backtester.gui.views.bt_view import BacktestView



class MainDashboard:
    def __init__(self, engine: TradingEngine) -> None:
        self.tag = "Main"
        self.views = [BacktestView(engine), 
                      PortfolioView(engine),
                      DataRetrievalView(engine)]
        self.sidebarWidth = 160 
        self.active_view = None
        self.engine = engine #For when we pass bus to other parts of dash



    def _switch_view(self, sender, app_data, user_data):
        dpg.hide_item(self._placeholder_tag)
        if self.active_view is not None:
            dpg.hide_item(self.active_view)
        dpg.show_item(user_data)
        self.active_view = user_data


    def _build_sidebar(self):
        with dpg.child_window(width=self.sidebarWidth, border=True):
            dpg.add_text("Navigation")
            dpg.add_separator()
            for view in self.views:
                dpg.add_button(
                    label=view.tag,
                    width=-1,
                    user_data=view.tag,
                    callback=self._switch_view,
                    
                )

    def build(self):
        with dpg.window(tag="Main"):
            #Horizontal true means that child widgets will be placed side by side

            with dpg.group(horizontal=True):
                self._build_sidebar()
                with dpg.child_window(tag="content_area", border=False):
                    self._placeholder_tag = dpg.add_text("Click on any of the sidebar buttons to navigate app")
                    for view in self.views:
                        view.build()

        dpg.set_primary_window("Main", True)
