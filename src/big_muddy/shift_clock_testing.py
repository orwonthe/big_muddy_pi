import time

from big_muddy_io import BigMuddyIO


def shift_clock_testing():
    big_muddy_io = BigMuddyIO.system()
    print('Shift clock testing: endless shift clocking')
    while True:
        big_muddy_io.shifting.pulse()

def shift_clock_tracing():
    big_muddy_io = BigMuddyIO.system()
    print('Shift clock tracing: endless shift clocking')
    while True:
        big_muddy_io.shifting.output.write(1)
        time.sleep(0.01)
        big_muddy_io.shifting.output.write(0)
        time.sleep(0.01)
