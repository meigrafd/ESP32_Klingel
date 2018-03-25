## /sd/scripts/main.py
import gc
import sys
import uos
import utime
import machine
import network
#import micropython

# custom
import oled
import queues
import settings
from wlan_manager import wifi
from utils import *


## https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/tree/master/MicroPython_BUILD/components/micropython/esp32/modules
## https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md#71-why-scheduling
## https://github.com/micropython/micropython/tree/master/ports/esp32/modules


def printD(message, end='\n'):
    if settings.DEBUG:
        print(message, end=end)

# turn off GPIO2 (blue onboard led)
#blue_led = machine.Pin(2, machine.Pin.OUT)
#blue_led.value(0)


# ----- OLED
oled.init()
oled.owelcome()


wlan = wifi(settings.WLAN_SSID, settings.WLAN_PASSWD, settings.DEBUG)
# go for fixed IP settings (IP, Subnet, Gateway, DNS)
#wlan.sta.ifconfig(('192.168.0.111', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
wlan.static_network(ip='192.168.0.111', gateway='192.168.0.1')

if not wlan.do_connect():
    printD("Could not initialize the network connection.")
    oled.oclear()
    oled.otext("Could not initialize network.", 0, 5)
    wlan.access_point(password=settings.WLAN_AP_PASS, authmode=3)

oled.oclear()
oled.otext("WLAN IP", 0, 5)
oled.otext(str(wlan.ipadd), 0, 15)

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/blob/master/MicroPython_BUILD/components/micropython/docs/zones.csv
rtc_timeout=10
rtc = machine.RTC()
rtc.ntp_sync(server=settings.ntpserver, tz=settings.tz)
while not rtc.synced():
    utime.sleep(1)
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


def interrupt_event(q, r, channel):
    q.put((r.now(), channel))

queue = queues.Queue()
pin_isr = machine.Pin(settings.isr, machine.Pin.IN, machine.Pin.PULL_UP)
pin_isr.irq(trigger=machine.Pin.IRQ_RISING, handler=partial(interrupt_event, queue, rtc))


# webserver

# for test purpose....
sys.exit(0)


import telegram
telegram_bot = telegram.bot(settings.TOKEN, settings.CHAT_ID)
telegram_bot.send("Ding Dong!")

cleared=False
while True:
    utime.sleep(0.1)
    # reduce power consumption
    machine.idle()
    if not cleared:
        oled.oclear()
        cleared=True
    if not queue.empty():
        start_time, pin = queue.get()
        printD('pin change {}'.format(pin))
        oled.otext('pin change {}'.format(pin), 15, 35)
        cleared=False
        #telegram_bot.send("Ding Dong!")
        #blue_led.toggle()
        utime.sleep(2)
        #blue_led.toggle()


# EOF
