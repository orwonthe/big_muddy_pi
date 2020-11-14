from big_muddy.big_muddy_io import BigMuddyIO


def flow_testing():
    print('Flow testing.')
    big_muddy_io = BigMuddyIO.system()
    while True:
        big_muddy_io.set_data_pins(0)
        big_muddy_io.shifting.pulse()
        big_muddy_io.set_data_pins(0)
        big_muddy_io.shifting.pulse()
        big_muddy_io.set_data_pins(0)
        big_muddy_io.shifting.pulse()
        big_muddy_io.set_data_pins(1)
        big_muddy_io.shifting.pulse()
        big_muddy_io.set_data_pins(1)
        big_muddy_io.shifting.pulse()
