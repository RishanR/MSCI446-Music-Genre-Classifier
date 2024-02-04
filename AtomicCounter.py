import threading


class AtomicCounter:
    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()

    def increment(self, num=1):
        with self._lock:
            self.value += num
            return self.value

# Example Usage:
#
# counter = AtomicCounter(0)
#
# counter.increment()
# print(counter.value) - should be 1
#
# counter.increment(4)
# print(counter.value) - should be 5
