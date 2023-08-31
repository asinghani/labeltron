from render import *
from config import *
import time

def print_label(text, last=True):
    image = render_label(text, border=False, for_print=True)
    pbm = render_pbm(image)
    bs = prepare_bitstream(pbm, (image.height, image.width), last=last)

    log_line = f"Send to printer text={repr(text)} len={len(bs)}"
    print(log_line)

    with open("log.txt", "a+") as f:
        f.write(log_line+"\n")

    with open(PRINTER_DEV, "ab+") as f:
        f.write(bs)

    time.sleep(10) # estimated printing time
    print("Done printing")

# Prepare the raw data stream to send to the printer
# last=False is for chain-printing and won't cut
# immediately after the print, but will still
# cut immediately before the next print
def prepare_bitstream(pbm, dims, last=True):
    exp_header = f"P4\n{dims[1]} {dims[0]}\n".encode()
    if pbm[0:len(exp_header)] != exp_header:
        print("INVALID PBM HEADER")
        print("EXPECTED", exp_header)
        print("GOT", pbm[0:len(exp_header)])

    pbm = pbm[len(exp_header):]

    bs = b""
    bs += b"\x00"*100 # Send zeros to clear state
    bs += b"\x1B@"    # Initialize
    bs += b"\x1BiM\x40" # Auto cut

    # Half cut mode
    if last: bs += b"\x1BiK\x08"
    else:    bs += b"\x1BiK\x00"

    bs += b"M\x02" # Compression

    # Encode the image
    width_bytes = dims[1] // 8
    assert width_bytes in [8, 16]
    for i in range(dims[0]):
        offs = i*width_bytes

        pad = (16 - width_bytes)//2

        bs += b"G\x11\x00\x0F" # line start
        bs += b"\x00"*pad # left padding
        bs += bytes([_reverse_bits(x) for x in pbm[offs:offs+width_bytes][::-1]])
        bs += b"\x00"*pad # right padding

    bs += b"\x1A"

    return bs

def _reverse_bits(x):
    return int('{:08b}'.format(x)[::-1], 2)

# Test case
if __name__ == "__main__":
    print_label("Hello")
