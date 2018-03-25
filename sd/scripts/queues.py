def sleep(secs):
    yield int(secs * 1000)


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
    """Exception raised by get_nowait()."""

class QueueFull(Exception):
    """Exception raised by put_nowait()."""

class Queue:
    """A queue, useful for coordinating producer and consumer coroutines.

    If maxsize is less than or equal to zero, the queue size is infinite. If it
    is an integer greater than 0, then "yield from put()" will block when the
    queue reaches maxsize, until an item is removed by get().

    Unlike the standard library Queue, you can reliably know this Queue's size
    with qsize(), since your single-threaded uasyncio application won't be
    interrupted between calling qsize() and doing an operation on the Queue.
    """
    _attempt_delay = 0.1

    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self._queue = deque()

    def _get(self):
        return self._queue.popleft()

    def get(self):
        """Returns generator, which can be used for getting (and removing)
        an item from a queue.

        Usage::

            item = yield from queue.get()
        """
        while not self._queue:
            yield from sleep(self._attempt_delay)
        return self._get()

    def get_nowait(self):
        """Remove and return an item from the queue.

        Return an item if one is immediately available, else raise QueueEmpty.
        """
        if not self._queue:
            raise QueueEmpty()
        return self._get()

    def _put(self, val):
        self._queue.append(val)

    def put(self, val):
        """Returns generator which can be used for putting item in a queue.

        Usage::

            yield from queue.put(item)
        """
        while self.qsize() >= self.maxsize and self.maxsize:
            yield from sleep(self._attempt_delay)
        self._put(val)

    def put_nowait(self, val):
        """Put an item into the queue without blocking.

        If no free slot is immediately available, raise QueueFull.
        """
        if self.qsize() >= self.maxsize and self.maxsize:
            raise QueueFull()
        self._put(val)

    def qsize(self):
        """Number of items in the queue."""
        return len(self._queue)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return not self._queue

    def full(self):
        """Return True if there are maxsize items in the queue.

        Note: if the Queue was initialized with maxsize=0 (the default),
        then full() is never True.
        """
        if self.maxsize <= 0:
            return False
        else:
            return self.qsize() >= self.maxsize