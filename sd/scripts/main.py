## /sd/scripts/main.py
import gc
import sys
import uos
import utime
import machine
import network

#for debugging interrupt service routines:
import micropython
micropython.alloc_emergency_exception_buf(100)

# custom
import settings
import telegram
from oled import OLED
from queue import Queue, QueueEmpty, QueueFull
from irq_debounce import DebouncedSwitch
from wlan_manager import wifi
from utils import *


## https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/tree/master/MicroPython_BUILD/components/micropython/esp32/modules
## https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md#71-why-scheduling
## https://github.com/peterhinch/Micropython-scheduler
## https://github.com/micropython/micropython/tree/master/ports/esp32/modules


def printD(message, end='\n'):
    if settings.DEBUG:
        print(message, end=end)

# turn off GPIO2 (blue onboard led)
#blue_led = machine.Pin(2, machine.Pin.OUT)
#blue_led.value(0)


# ----- OLED
oled = OLED()
oled.welcome()


wlan = wifi(settings.WLAN_SSID, settings.WLAN_PASSWD, settings.DEBUG)
# go for fixed IP settings (IP, Subnet, Gateway, DNS)
#wlan.sta.ifconfig(('192.168.0.111', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
wlan.static_network(ip='192.168.0.111', gateway='192.168.0.1')

if not wlan.do_connect():
    printD("Could not initialize the network connection.")
    oled.clear()
    oled.text("Could not initialize network.", 0, 5)
    wlan.access_point(password=settings.WLAN_AP_PASS, authmode=3)

oled.clear()
oled.text("WLAN IP", 0, 5)
oled.text(str(wlan.ipadd), 0, 15)

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/blob/master/MicroPython_BUILD/components/micropython/docs/zones.csv
rtc_timeout=10
rtc = machine.RTC()
rtc.ntp_sync(server=settings.ntpserver, tz=settings.tz)
while not rtc.synced():
    utime.sleep_ms(1000)
    rtc_timeout -= 1
    if rtc_timeout == 5:
        rtc.ntp_sync(server=settings.ntpserver2, tz="UTC-1")
    if rtc_timeout == 0:
        ntp_settime(rtc)
        break
print("Time set:", utime.strftime("%c", utime.localtime()))


# mDNS ... https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/mdns
mdns = network.mDNS()
_ = mdns.start("mPy", "MicroPython with mDNS")
_ = mdns.addService('_ftp', '_tcp', 21, "MicroPython", {"board": "ESP32", "service": "mPy FTP File transfer", "passive": "True"})
_ = mdns.addService('_telnet', '_tcp', 23, "MicroPython", {"board": "ESP32", "service": "mPy Telnet REPL"})
_ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "mPy Web server"})


# FTP & Telnet Server
network.ftp.start(user=settings.FTP_LOGIN, password=settings.FTP_PASSWD, buffsize=1024, timeout=300)
network.telnet.start(user=settings.FTP_LOGIN, password=settings.FTP_PASSWD, timeout=300)


def interrupt_event(arg):
    q, r, pin = arg
    q.put((r.now(), pin))
    print('{} pin change {}'.format(utime.strftime("%M:%S", r.now()), pin))

queue = Queue()
interrupt_pin = machine.Pin(settings.isr, machine.Pin.IN, machine.Pin.PULL_UP)
doorbellbutton = DebouncedSwitch(sw=interrupt_pin, cb=interrupt_event, arg=(queue, rtc, settings.isr), delay=500)


# webserver

# for test purpose....
#sys.exit(0)


telegram_bot = telegram.bot(settings.TOKEN, settings.CHAT_ID)
#telegram_bot.send("Ding Dong!")


def loop():
    while True:
        _time, pin = queue.get()  # block till entry
        print("debug: {}".format(queue.qsize()))
        print('{0} pin change {1}'.format(utime.strftime("%H:%M:%S", _time), pin))


def loop2():
    cleared=False
    while True:
        gc.collect()
        utime.sleep_ms(100)
        # reduce power consumption
        machine.idle()
        if not cleared:
            oled.clear()
            cleared=True
        if not queue.empty():
            print("debug: {}".format(queue.qsize()))
            _time, pin = queue.get()
            print('{0} pin change {1}'.format(utime.strftime("%H:%M:%S", _time), pin))
            oled.text('{0} pin change'.format(utime.strftime("%H:%M:%S", _time)), 0, 35)
            cleared=False
            #telegram_bot.send("Ding Dong!")
            #blue_led.toggle()
            #utime.sleep(2)
            #blue_led.toggle()


# EOF
