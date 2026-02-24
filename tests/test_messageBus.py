
# tests/test_message_bus.py

import threading
import time
from dataclasses import dataclass
import pytest

from src.messageBus import MessageBus


@dataclass(frozen=True)
class BarEvent:
    symbol: str
    ts_epoch: int
    close: float


@dataclass(frozen=True)
class OrderEvent:
    symbol: str
    qty: int


@pytest.fixture
def bus():
    return MessageBus()


def test_publish_then_get_returns_same_event(bus: MessageBus):
    e = BarEvent("ES", 10001, 101.0)
    bus.publish(e)

    got = bus.get(timeout=0.1)
    assert got == e


def test_get_timeout_returns_none_when_queue_empty(bus: MessageBus):
    got = bus.get(timeout=0.05)
    assert got is None


def test_subscribe_and_dispatch_calls_handler_once(bus: MessageBus):
    calls = []

    def handler(e: BarEvent):
        calls.append(e)

    bus.subscribe(BarEvent, handler)

    e = BarEvent("NQ", 20002, 22222.25)
    bus.publish(e)

    # using the internal dispatcher loop manually (fast + deterministic)
    got = bus.get(timeout=0.1)
    assert got == e

    bus._dispatch(got)
    assert calls == [e]


def test_multiple_handlers_for_same_event_type_are_all_called(bus: MessageBus):
    called_a = []
    called_b = []

    def handler_a(e: BarEvent):
        called_a.append(e)

    def handler_b(e: BarEvent):
        called_b.append(e)

    bus.subscribe(BarEvent, handler_a)
    bus.subscribe(BarEvent, handler_b)

    e = BarEvent("ES", 123, 99.5)
    bus._dispatch(e)

    assert called_a == [e]
    assert called_b == [e]


def test_no_handlers_for_event_type_does_not_raise(bus: MessageBus):
    # No one subscribed to OrderEvent; should be a no-op.
    e = OrderEvent("ES", 1)
    bus._dispatch(e)  # should not throw


def test_subscribe_is_type_specific(bus: MessageBus):
    bar_calls = []
    order_calls = []

    def on_bar(e: BarEvent):
        bar_calls.append(e)

    def on_order(e: OrderEvent):
        order_calls.append(e)

    bus.subscribe(BarEvent, on_bar)
    bus.subscribe(OrderEvent, on_order)

    bar = BarEvent("ES", 1, 101.0)
    order = OrderEvent("ES", 2)

    bus._dispatch(bar)
    bus._dispatch(order)

    assert bar_calls == [bar]
    assert order_calls == [order]


def test_run_processes_published_event_and_calls_handler(bus: MessageBus):
    calls = []

    def handler(e: BarEvent):
        calls.append(e)

    bus.subscribe(BarEvent, handler)

    event = BarEvent("ES", 999, 123.45)
    bus.publish(event)

    # Engine-style loop behavior
    received = bus.get(timeout=0.1)
    assert received == event

    bus._dispatch(received)

    assert calls == [event]


def test_returns_none_when_no_events(bus: MessageBus):

    result = bus.get(timeout=0.05)
    assert result is None

def test_events_are_processed_in_fifo_order(bus: MessageBus):
    received = []

    def handler(e: BarEvent):
        received.append(e)

    bus.subscribe(BarEvent, handler)

    e1 = BarEvent("ES", 1, 10.0)
    e2 = BarEvent("ES", 2, 20.0)
    e3 = BarEvent("ES", 3, 30.0)

    bus.publish(e1)
    bus.publish(e2)
    bus.publish(e3)

    # Simulate engine loop: pop then dispatch in sequence
    for _ in range(3):
        event = bus.get(timeout=0.1)
        assert event is not None
        bus._dispatch(event)

    assert received == [e1, e2, e3]

