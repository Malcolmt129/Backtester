import dearpygui.dearpygui as dpg

TAG = "view_backtest"


def build():
    with dpg.child_window(tag=TAG, show=False):
        dpg.add_text("Backtest")
        dpg.add_separator()
        dpg.add_text("Strategy selection, date range, and live bar feed will appear here.")
