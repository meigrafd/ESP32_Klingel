from micropython import const

# Imported: Turn off (False) if your Project is ready.
# Adding logs not just takes up a lot of memory, but also wastes time sending data out over UART.
DEBUG = True

# D13 is GPIO13, D14 is GPIO14 and so on...

# OLED (i2c):
SDA = const(5) # GPIO21, pin11, Data -> D1 pin OLED Display
SCL = const(4) # GPIO22, pin14, Clock -> D0 pin OLED Display
oledtype = (128, 64)

#SDA = const(21) # GPIO21, pin11, Data -> D1 pin OLED Display
#SCL = const(22) # GPIO22, pin14, Clock -> D0 pin OLED Display
#oledtype = (64, 48) # D1-mini 64x48.  Regular "0.96inch" 128x64
#oledtype = (128, 64)

#RST = const(17)    # GPIO17, pin7 -> RST pin OLED Display ... use any free digital GPIO

# spi
#CS = const(5)      # GPIO5, pin8 - SPI_CS0 -> CS / SS pin OLED Display
#DC = const(19)     # GPIO16, pin6 -> DC pin OLED Display ... use any free digital GPIO
#SCLK = const(18)   # D18, pin9 - SPI_CLK -> D0 pin OLED Display
#MOSI = const(23)   # GPIO23, pin15 - SPI_MOSI -> D1 pin OLED Display
#MISO = None # not needed

# SD (spi mode)
CS = const(13)
SCK = const(14)
MOSI = const(15)
MISO = const(2)

# Doorbell Interrupt pin
isr = const(25)  # D25, GPIO25, pin8


# TIME:
tz = "CET-1CEST,M3.5.0,M10.5.0/3"
ntpserver = "de.pool.ntp.org"
ntpserver2 = "3.de.pool.ntp.org"

# WiFi
#known_networks = {
#    '<net>': {'pwd': '<password>'},
#    '<net>': {'pwd': '<password>', 'wlan_config':  ('10.0.0.114', '255.255.0.0', '10.0.0.1', '10.0.0.1')}, # (ip, subnet_mask, gateway, DNS_server)
#}# https://docs.pycom.io/chapter/tutorials/all/wlan.html
WLAN_SSID = "t0p"
WLAN_PASSWD = "s3cr3t"
WLAN_AP_PASS = "ESP-*"

# Telegram
TOKEN = '502745623:..top..'
CHAT_ID = '..secret..'

# FTP Server & Telnet Server
FTP_LOGIN = 'micro'
FTP_PASSWD = 'python'


