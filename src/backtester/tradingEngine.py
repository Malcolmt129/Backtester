from backtester.interfaces.databaseInterface import IDatabase
from backtester.messageBus import MessageBus


class TradingEngine:
    def __init__(self, bus: MessageBus, store:IDatabase):
        self.bus = bus
        self.store = store 
        self.strategies = []
        self._stop = False

    def request_stop(self):
        self._stop = True

    def run(self):
        #self.feed.start()
        #self.broker.start()

        
        #Each of the strategies have to have a stop and a start function
        #Remember
        for s in self.strategies:
            s.start()

        while not self._stop:
            event = self.bus.get(timeout=1.0)   # blocks

            if event is None:
                continue
            self._dispatch(event)
            print("Finished loop")

        self._shutdown()

    def _dispatch(self, event):
        for s in self.strategies:
            s.on_event(event)

    def _shutdown(self):
        for s in self.strategies:
            s.stop()
        #self.broker.stop()
        #self.feed.stop()
