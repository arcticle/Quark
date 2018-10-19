from future.builtins import super

class EventHandler(object):
    def __init__(self):
        self._handlers = []

    def add(self, handler):
        self._handlers.append(handler)
        return self

    def remove(self, handler):
        self._handlers.remove(handler)
        return self

    def fire(self, sender, **args):
        for handler in self._handlers:
            handler(sender, **args)
    
    __iadd__ = add
    __isub__ = remove
    __call__ = fire


class DelayedEventHandler(EventHandler):
    def __init__(self):
        super().__init__()
        self._events = []
    
    def add(self, handler):
        super().add(handler)

        while len(self._events) > 0:
            sender, args = self._events.pop(0)
            super().fire(sender, **args)
        
        return self

    def fire(self, sender, **args):
        if len(self._handlers) == 0:
            self._events.append((sender, args))
            return

        super().fire(sender, **args)

    __iadd__ = add
    __call__ = fire