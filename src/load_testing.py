def load_testing(big_muddy):
    print('Load testing.')
    while True:
        big_muddy.set_data_pins(0)
        big_muddy.loading.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.loading.pulse()
