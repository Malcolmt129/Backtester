import dearpygui.dearpygui as dpg

TAG = "view_dashboard"


def build():
    with dpg.child_window(tag=TAG, show=True):
        dpg.add_text("Dashboard")
        dpg.add_separator()
        dpg.add_text("Engine status and live event feed will appear here.")
