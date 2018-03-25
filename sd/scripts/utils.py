## utils.py
import gc
import uos
import time
import struct
import ssl
import socket


def https_test(host):
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(addr)
    try:
        s = ssl.wrap_socket(s)
        s.close()
        return True
    except OSError as error:
        print("OSError: {}".format(error))
        s.close()
        return False


def ntp_gettime(host='pool.ntp.org'):
    NTP_DELTA = 3155673600
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

def ntp_settime(rtc):
    t = ntp_gettime()
    tm = time.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc.init(tm)


def mv_file(source, dest):
    success = uos.rename(source, dest)
    if success:
        uos.listdir(dest)
    else:
        return success


def free_ram():
    gc.collect()
    print('Free RAM: %.2f kB' % (gc.mem_free()/1024))
    gc.collect()


def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)
    return _partial


def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value


# EOF