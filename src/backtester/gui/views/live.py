import dearpygui.dearpygui as dpg

TAG = "view_live"


def build():
    with dpg.child_window(tag=TAG, show=False):
        dpg.add_text("Live Trading")
        dpg.add_separator()
        dpg.add_text("Active strategies, positions, and real-time P&L will appear here.")
