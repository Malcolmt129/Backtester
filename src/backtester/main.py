import signal
from backtester import bootstrap
import threading
import dearpygui.dearpygui as dpg

from backtester.gui.app import MainDashboard 

def main():
    app = bootstrap.build_app()  
    engine = app.engine
    gui = MainDashboard(engine) 
    engineThread = threading.Thread(target=engine.run)
    engineThread.start()
    
    # graceful shutdown
    def _stop(*_):
        engine.request_stop()


    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    dpg.create_context() 
    gui.build() 

    dpg.create_viewport(width=1200, height=800, title="Backtester GUI")
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    engine.request_stop()
    dpg.destroy_context()

if __name__ == "__main__":

    main()
