from dataclasses import dataclass
from backtester.messageBus import MessageBus
from backtester.tradingEngine import TradingEngine
from backtester.sqliteManager import SQLiteManager


@dataclass
class App:

    engine: TradingEngine


def build_app() -> App:

    bus = MessageBus()
    store = SQLiteManager(bus)

    #The engine should not have to initiate with stategies already active. 
    #I should be able to add them at a later time. Lets say raise an event 
    #where I can add one on the fly
    engine = TradingEngine(
            bus=bus,
            store=store
            )

    return App(engine=engine)

