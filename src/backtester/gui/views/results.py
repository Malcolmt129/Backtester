import dearpygui.dearpygui as dpg

TAG = "view_results"


def build():
    with dpg.child_window(tag=TAG, show=False):
        dpg.add_text("Results")
        dpg.add_separator()
        dpg.add_text("Past backtest runs and trade history will appear here.")
