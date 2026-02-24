from dataclasses import dataclass
from src.messageBus import MessageBus
from src.tradingEngine import TradingEngine
from src.sqliteManager import SQLiteManager


@dataclass
class App:

    engine: TradingEngine


def build_app() -> App:

    bus = MessageBus()
    store = SQLiteManager(bus)
    strategies = []

    strategies = ["EMA_CrossOver"]
    
    #You will need to add on to this later when you get other components up
    # and running
    engine = TradingEngine(
            bus=bus,
            store=store,
            strategies=strategies,
            )

    return App(engine=engine)

