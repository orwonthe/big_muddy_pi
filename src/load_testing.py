from big_muddy_io import BigMuddyIO


def load_testing(big_muddy=None):
    print('Load testing.')
    if big_muddy is None:
        big_muddy = BigMuddyIO.system()
    while True:
        big_muddy.set_data_pins(0)
        big_muddy.loading.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.loading.pulse()

