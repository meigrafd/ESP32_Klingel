import sh1106
import settings
import network
import machine


class OLED:
    def __init__(self, freq=400000):
        # ValueError: Pins 16&17 cannot be used if SPIRAM is used
        RST = machine.Pin(0)
        SDA = machine.Pin(settings.SDA)
        SCL = machine.Pin(settings.SCL)
        self.i2c = machine.I2C(scl=SCL, sda=SDA, freq=freq)
        if 60 in set(self.i2c.scan()):
            self.display = sh1106.SH1106_I2C(settings.oledtype[0], settings.oledtype[1], self.i2c, RST, 0x3c)
            self.display.sleep(False)
            self.display.fill(0)
            self.display.rotate(True)
    
    def on(self):
        self.display.poweron()
    
    def off(self):
        self.display.poweroff()
    
    def oprint(self, x, y):
        self.display.pixel(x, y, 1)
        self.display.show()
    
    def text(self, text, indent, line):
        self.display.text(text, indent, line)
        self.display.show()
    
    def clear(self):
        self.display.fill(0)
        self.display.show()
    
    def welcome(self):
        self.clear()
        self.text('----------------', 0, 0)
        self.text('e-Bell', 30, 13)
        self.text('----------------', 0, 28)
    
    def scroll(self, indent, line):
        self.display.scroll(indent, line)
        self.display.show()

# EOF
