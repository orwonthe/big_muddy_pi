import time


def wide_client_connector_test(big_muddy):
    print('Wide connector test: Use single leaf on console loop')
    client_names = ["D8", "D7", "C6", "C5", "B4", "B3", "A2", "A1"]
    bit_names = ["Z1 (Green)", "Z0 (green/white)"]
    while True:
        for client_index in range(8):
            bits_found = [[False, False], [False,False]]
            for cycles in range(8):
                for out_bit_index in range(8):
                    bit_to_send = 1 if out_bit_index == client_index else 0
                    big_muddy.set_data_pins(bit_to_send)
                    big_muddy.shifting.pulse()
                for out_bit_index in range(16):
                    big_muddy.shifting.pulse()
                big_muddy.loading.pulse()

                big_muddy.set_data_pins(0)
                for out_bit_index in range(24):
                    big_muddy.shifting.pulse()
                big_muddy.loading.pulse()

                for in_client_index in range(8):
                    for in_bit_index in range(2):
                        bit_read = big_muddy.consoles.read()
                        big_muddy.shifting.pulse()
                        if in_client_index == client_index:
                            bits_found[in_bit_index][bit_read] = True
                for out_bit_index in range(8):
                    big_muddy.shifting.pulse()

            for in_bit_index in range(2):
                have_zeroes, have_ones = bits_found[in_bit_index]
                if have_ones and have_zeroes:
                    print(client_names[client_index] + ' has bit ' + str(in_bit_index))
        print()
