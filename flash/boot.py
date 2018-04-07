## /flash/boot.py
# This file is executed on every boot (including wake-boot from deepsleep)
from micropython import const
import machine
import uos
import sys


sys.path[1] = '/sd/lib'
sys.path.append('/sd')
sys.path.append('/flash/lib')

CS = machine.Pin(const(13))
SCK = machine.Pin(const(14))
MOSI = machine.Pin(const(15))
MISO = machine.Pin(const(2))

uos.sdconfig(uos.SDMODE_SPI, SCK, MOSI, MISO, CS)
uos.mountsd()

if 'main.py' in uos.listdir('/sd/scripts'):
    exec(open('/sd/scripts/main.py').read(), globals())
