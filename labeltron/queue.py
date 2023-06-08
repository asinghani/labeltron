from print import print_label
from serial_iface import *
import copy
import time
import threading

pq = []
lock = threading.Lock()

def queue_add(text):
    global pq
    with lock:
        pq.append(text)

def queue_get():
    with lock:
        return copy.deepcopy(pq)

def queue_reset():
    global pq
    with lock:
        pq = []

def queue_loop():
    global pq

    set_state(STATE_IDLE)

    hanging = False
    while True:
        evt = get_pressed()

        if len(pq):
            set_state(STATE_READY)

        if len(pq) and (evt == EVT_RESET):
            print("Reset Queue")
            queue_reset()
            set_state(STATE_IDLE)

        if len(pq) and (evt == EVT_PRINT):
            set_state(STATE_PRINTING)

            while len(pq):
                with lock:
                    if len(pq) == 0: continue
                    txt = pq[0]
                    pq = pq[1:]
                    is_last = (len(pq) == 0)

                hanging = not is_last
                print_label(txt, last=is_last)

            if hanging:
                hanging = False
                print_label(" ", last=False)

            set_state(STATE_IDLE)

        time.sleep(1)
