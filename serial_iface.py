import serial
import config
import time
import sys
import traceback

STATE_IDLE = 0
STATE_READY = 1
STATE_PRINTING = 2

EVT_NONE = 0
EVT_PRINT = 1
EVT_RESET = 2

m_state = STATE_IDLE
m_evt = EVT_NONE

def set_state(st):
    global m_state
    m_state = st

def get_pressed():
    global m_evt
    _evt = m_evt
    m_evt = EVT_NONE
    return _evt

def serial_loop():
    global m_state, m_evt

    if config.SERIAL_PORT is None:
        while True: m_evt = EVT_PRINT

    """
        Software -> Button: sends state every 0.2s
        Button -> Software: sends event when triggered
    """
    try:
        with serial.Serial(config.SERIAL_PORT, 115200, timeout=0) as ser:
            while True:
                time.sleep(0.2)
                ser.write(str(m_state).encode())
                ser.flush()

                dat = ser.read(9999).decode()
                for c in dat:
                    if c == "1": m_evt = EVT_PRINT
                    if c == "2": m_evt = EVT_RESET

                if not ser.is_open:
                    break
    except:
        print("Serial Error")
        traceback.print_exc()

    # If serial fails, kill the whole app
    sys.exit(1)

