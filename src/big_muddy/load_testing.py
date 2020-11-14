from big_muddy.big_muddy_io import BigMuddyIO


def load_testing():
    big_muddy_io = BigMuddyIO.system()
    print('Load testing.')
    while True:
        big_muddy_io.set_data_pins(0)
        big_muddy_io.loading.pulse()
        big_muddy_io.set_data_pins(1)
        big_muddy_io.loading.pulse()
