import sh1106
import settings
import network
import machine


def init():
    global display
    # ValueError: Pins 16&17 cannot be used if SPIRAM is used
    RST = machine.Pin(0)
    SDA = machine.Pin(settings.SDA)
    SCL = machine.Pin(settings.SCL)
    i2c = machine.I2C(scl=SCL, sda=SDA, freq=400000)
    if 60 in set(i2c.scan()):
        display = sh1106.SH1106_I2C(settings.oledtype[0], settings.oledtype[1], i2c, RST, 0x3c)
        display.sleep(False)
        display.fill(0)
        display.rotate(True)


def oprint(x, y):
    display.pixel(x, y, 1)
    display.show()


def otext(text, indent, line):
    display.text(text, indent, line)
    display.show()


def oclear():
    display.fill(0)
    display.show()


def owelcome():
    oclear()
    otext('----------------', 0, 0)
    otext('e-Bell', 25, 13)
    otext('----------------', 0, 28)

# EOF