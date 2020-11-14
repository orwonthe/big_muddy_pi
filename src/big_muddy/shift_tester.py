from big_muddy_io import BigMuddyIO


def shift_clock_testing():
    big_muddy_io = BigMuddyIO.system()
    print('Shift clock testing: endless shift clocking')
    while True:
        big_muddy_io.shifting.pulse()
