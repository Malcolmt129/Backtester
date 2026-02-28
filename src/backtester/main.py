import signal
from backtester import bootstrap

def main():
    app = bootstrap.build_app()  
    engine = app.engine

    engine.run()

    # graceful shutdown
    def _stop(*_):
        engine.request_stop()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    engine.run()                   # blocking call
if __name__ == "__main__":

    main()
