def flow_testing(big_muddy):
    print('Flow testing.')
    while True:
        big_muddy.set_data_pins(0)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(0)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(0)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.shifting.pulse()
