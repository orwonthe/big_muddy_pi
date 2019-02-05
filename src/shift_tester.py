from big_muddy_io import BigMuddyIO


def shift_clock_testing(big_muddy=None):
    print('Shift clock testing: endless shift clocking')
    if big_muddy is None:
        big_muddy = BigMuddyIO.system()
    while True:
        big_muddy.shifting.pulse()

