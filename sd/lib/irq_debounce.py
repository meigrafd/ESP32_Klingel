#
# modified for irq/isr, by meigrafd (26.03.2018)
# 
# http://www.ganssle.com/debouncing.htm
# https://www.allaboutcircuits.com/technical-articles/switch-bounce-how-to-deal-with-it/
#
# https://gist.github.com/SpotlightKid/0a0aac56606286a80f860b116423c94f
#
# inspired by: https://forum.micropython.org/viewtopic.php?t=1938#p10931
#
import micropython

from machine import Timer
timer_init = lambda t, p, cb: t.init(period=p, callback=cb)

# uncomment when debugging callback problems
#micropython.alloc_emergency_exception_buf(100)


class DebouncedSwitch:
    def __init__(self, sw, cb, arg=None, delay=200, edge='RISING', tid=1):
        self.sw = sw
        # Create references to bound methods beforehand
        # http://docs.micropython.org/en/latest/pyboard/library/micropython.html#micropython.schedule
        self._sw_cb = self.sw_cb
        self._tim_cb = self.tim_cb
        self._set_cb = getattr(self.sw, 'callback', None) or self.sw.irq
        self.delay = delay
        # IRQ_RISING = 1 , IRQ_FALLING = 2 , IRQ_ANYEDGE = 3
        if edge == 'RISING':
            self.edge = self.sw.IRQ_RISING
        elif edge == 'FALLING':
            self.edge = self.sw.IRQ_FALLING
        else:
            self.edge = self.sw.IRQ_ANYEDGE
        self.tim = Timer(tid)
        self.callback(cb, arg)

    def sw_cb(self, pin=None):
        self._set_cb(None)
        timer_init(self.tim, self.delay, self._tim_cb)

    def tim_cb(self, tim):
        tim.deinit()
        if self.sw():
            micropython.schedule(self.cb, self.arg)
        self._set_cb(self._sw_cb if self.cb else None, trigger=self.edge)

    def callback(self, cb, arg=None):
        self.tim.deinit()
        self.cb = cb
        self.arg = arg
        self._set_cb(self._sw_cb if cb else None, trigger=self.edge)

