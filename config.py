import os

"""
How long an API key should remain fresh
"""
APIKEY_EXPIRY = 12*60*60

"""
Printer device path
"""
PRINTER_DEV = "/dev/usb/lp0"

"""
HTTP basic authentication for use on public networks
"""
AUTHENTICATION = None

if os.path.exists("creds.txt"):
    with open("creds.txt") as f:
        creds = f.readlines()
        assert len(creds) >= 2
        AUTHENTICATION = (creds[0].strip(), creds[1].strip())

"""
Serial port to require manual button-press to print
"""
SERIAL_PORT = None
# SERIAL_PORT = "/dev/ttyUSB0"
