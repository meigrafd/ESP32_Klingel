# https://github.com/python/cpython/blob/master/Lib/queue.py
#
# own creation (25.03.2018 by meigrafd)
#
# Example Usage:
#
# from queue import Queue, QueueEmpty, QueueFull
# queue = Queue()
# try:
#   queue.get(timeout=20)
# except QueueEmpty:
#   pass
#
from utime import time, sleep_ms


class deque:
    def __init__(self, iterable=None):
        if iterable is None:
            self.q = []
        else:
            self.q = list(iterable)
    
    def popleft(self):
        return self.q.pop(0)
    
    def popright(self):
        return self.q.pop()
    
    def pop(self):
        return self.q.pop()
    
    def append(self, a):
        self.q.append(a)
    
    def appendleft(self, a):
        self.q.insert(0, a)
    
    def extend(self, a):
        self.q.extend(a)
    
    def __len__(self):
        return len(self.q)
    
    def __bool__(self):
        return bool(self.q)
    
    def __iter__(self):
        yield from self.q
    
    def __str__(self):
        return 'deque({})'.format(self.q)


class QueueEmpty(Exception):
    'Exception raised by Queue.get(block=0)/get_nowait().'
    pass

class QueueFull(Exception):
    'Exception raised by Queue.put(block=0)/put_nowait().'
    pass

class Queue:
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self.queue = deque()
    
    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return not self.qsize()
    
    def full(self):
        return 0 < self.maxsize <= self.qsize()
    
    def _put(self, item):
        self.queue.append(item)
    
    def put(self, item, block=True, timeout=None):
        if self.maxsize > 0:
            if not block:
                if self.qsize() >= self.maxsize:
                    raise QueueFull
            elif timeout is None:
                while self.qsize() >= self.maxsize:
                    sleep_ms(100)
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while self.qsize() >= self.maxsize:
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise QueueFull
                    sleep_ms(100)
        self._put(item)
    
    def _get(self):
        return self.queue.popleft()
    
    def get(self, block=True, timeout=None):
        if not block:
            if not self.qsize():
                raise QueueEmpty
        elif timeout is None:
            while not self.qsize():
                sleep_ms(100)
        elif timeout < 0:
            raise ValueError("'timeout' must be a non-negative number")
        else:
            endtime = time() + timeout
            while not self.qsize():
                remaining = endtime - time()
                if remaining <= 0.0:
                    raise QueueEmpty
                sleep_ms(100)
        return self._get()
    
    def get_nowait(self):
        return self._get() if self.qsize() else None
    
    def qsize(self):
        """Number of items in the queue."""
        return len(self.queue)

    def __len__(self):
        return len(self.queue)


# EOF