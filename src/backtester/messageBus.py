from queue import Queue, Empty
from collections import defaultdict
from typing import Callable, Type
from backtester.interfaces.btEvents import Event

class MessageBus:
    def __init__(self):
        self._queue = Queue()
        self._handlers = defaultdict(list)
        self._running = False
        
    # ---- Publish ----

    '''
        An event is basically just a dataclass of some sort. Its just pure data,
        that represents what happened and the data that needs to be reported to 
        subscribers. 
    '''
    def publish(self, event: Event):
        self._queue.put(event)

    # ---- Subscribe ----
    def subscribe(self, event_type: Type, handler: Callable):
        self._handlers[event_type].append(handler)
    
    def get(self, timeout=None):
        try:
            return self._queue.get(timeout=timeout) #timeout is a queue parameter
        except Empty:
            return None
   

   # ---- Event Loop ----
    def run(self):
        self._running = True
        while self._running:
            try:
                event = self._queue.get(timeout=1.0)
            except Empty:
                continue

            self._dispatch(event)

    def stop(self):
        self._running = False

    def _dispatch(self, event: Event):
        handlers = self._handlers[type(event)]
        for handler in handlers:
            handler(event)
