#
# (c) 02.2018 by meigrafd
#
import utime
import network

##
## https://github.com/tayfunulu/WiFiManager
## https://github.com/BLavery/psuite-upython/tree/master/lib
##


class wifi:
    def __init__(self, ssid=None, password=None, debug=True, timeout=12):
        self.ssid = ssid
        self.password = password
        self.debug = debug
        self.timeout = timeout #sec
        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self.ap_active = self.ap.active(False)
        self.AUTHMODE = {0: 'open', 1: 'WEP', 2: 'WPA-PSK', 3: 'WPA2-PSK', 4: 'WPA/WPA2-PSK'}
    
    def printD(self, message, end='\n'):
        if self.debug:
            print(message, end=end)
    
    def scan(self, ssid=None, password=None):
        if ssid is not None: self.ssid = ssid
        if password is not None: self.password = password
        self.sta.active(True)
        self.networks = self.sta.scan()
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(self.networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            self.printD('ssid: %s chan: %d rssi: %d authmode: %s' % (ssid, channel, rssi, self.AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid == self.ssid:
                    self.connected = self.do_connect(self.ssid, self.password)
                else:
                    self.printD('skipping unknown encrypted network.')
            else:  # open
                self.connected = self.do_connect(ssid, None)
            if self.connected:
                break
        if self.sta.isconnected():
            return True
        return False
    
    def connect(self):
        return self.scan()
    
    def disconnect(self):
        return self.sta.disconnect()
    
    def do_connect(self, ssid=None, password=None, check=True):
        if check and self.sta.isconnected():
            self.printD('Already connected!')
            return True
        timeout = self.timeout
        if not self.sta.active(): self.sta.active(True)
        self.printD('WLAN: Connecting.', end='')
        self.sta.connect(ssid, password)
        while not self.sta.isconnected() and timeout > 0:
            self.printD('.', end='')
            timeout -= 1
            utime.sleep_ms(1000)
        if self.sta.isconnected():
            self.ipadd = self.sta.ifconfig()[0]
            self.printD(' client connection as {}'.format(self.ipadd))
            return True
        else:
            self.sta.disconnect()
            self.sta.active(False)
            self.printD(' failed!')
        return False
    
    def static_network(self, ip, subnet='255.255.255.0', gateway='192.168.0.1', dns='208.67.220.220'):
        self.sta.ifconfig((ip, subnet, gateway, dns))
    
    def access_point(self, ssid=None, password=None, authmode=0):
        if self.sta.active(): self.sta.active(False)
        self.ap.active(True)
        if not ssid:
            ssid = 'ESP-'+str(self.ap.config('mac')[4])+str(self.ap.config('mac')[5])
        self.ssid = ssid
        self.ap.config(essid=ssid, password=password, authmode=authmode)
        print('Own WLAN-AP: "{0}" pw: "{1}"' . format(self.ap.config('essid'), password))
        self.ap_active = True
        self.ipadd = '0.0.0.0'


# EOF