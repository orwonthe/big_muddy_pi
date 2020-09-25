import time


def client_connector_test(big_muddy, sleep_time=0.25):
    print('Client connector test: Use single leaf on servo loop')
    client_signals = [signal << 4 for signal in [1, 3, 5, 7]]
    bits_read = [[0, 0], [0, 0], [0, 0], [0, 0]]
    bits_expected = [[0, 0], [0, 0], [0, 0], [0, 0]]
    client_names = ["D", "C", "B", "A"]
    bit_names = ["SW1 (Green)", "SW0 (green/white)"]
    while True:
        bits_connected = [[True, True], [True, True], [True, True], [True, True]]
        for cycle_index in range(5):
            for shift_index in range(8):
                time.sleep(sleep_time)
                for client_index in range(4):
                    for bit_index in range(2):
                        bits_read[client_index][bit_index] = big_muddy.servos.read()
                        big_muddy.shifting.pulse()
                for client_index in range(4):
                    client_signal = client_signals[client_index]
                    bits = client_signal >> shift_index
                    for bit_index in range(4):
                        send_bit = bits & 1
                        if bit_index < 2:
                            bits_expected[client_index][bit_index] = send_bit
                        big_muddy.set_data_pins(send_bit)
                        bits = bits >> 1
                        big_muddy.shifting.pulse()
                big_muddy.loading.pulse()
                if cycle_index > 1:
                    for client_index in range(4):
                        for bit_index in range(2):
                            matching = bits_expected[client_index][bit_index] == bits_read[client_index][bit_index]
                            if not matching and bits_connected[client_index][bit_index]:
                                bits_connected[client_index][bit_index] = False
        for client_index in reversed(range(4)):
            if bits_connected[client_index][0] and bits_connected[client_index][1]:
                print("client " + client_names[client_index] + " appears to be okay")
            elif not bits_connected[client_index][0] and not bits_connected[client_index][1]:
                print("client " + client_names[client_index] + " is not connected")
            else:
                for bit_index in range(2):
                    if not bits_connected[client_index][bit_index]:
                        print("client " + client_names[client_index] + " is not connected at bit " + bit_names[
                            bit_index])
        print()
