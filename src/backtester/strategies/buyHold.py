import logging
from backtester.interfaces.tradingStratInterface import ITradingStrategy
from backtester.interfaces.btEvents import BarEvent, BacktestCompleteEvent

log = logging.getLogger(__name__)


class BuyHold(ITradingStrategy):

    def __init__(self):
        self._entry_price = None
        self._last_price = None
        self._symbol = None
        self._reported = False

    def start(self):
        log.info("BuyHold strategy started")

    def stop(self):
        self._report()

    def on_event(self, event):
        if isinstance(event, BarEvent):
            if self._entry_price is None:
                self._entry_price = event.close
                self._symbol = event.symbol
                log.info(f"Bought {event.symbol} at {event.close}")
            self._last_price = event.close

        elif isinstance(event, BacktestCompleteEvent):
            self._report()

    def _report(self):
        if self._reported:
            return
        self._reported = True

        if self._entry_price and self._last_price:
            pnl = self._last_price - self._entry_price
            pct = (pnl / self._entry_price) * 100
            log.info(
                f"BuyHold result — {self._symbol}: "
                f"entry={self._entry_price:.2f}, "
                f"exit={self._last_price:.2f}, "
                f"PnL={pnl:.2f} ({pct:.2f}%)"
            )
