import time

from big_muddy_io import BigMuddyIO


def data_probe(big_muddy=None):
    print("data probe: loop servo and console with no leaves")
    if big_muddy is None:
        big_muddy = BigMuddyIO.system()
    error_count = 0
    for data_signal in big_muddy.signals:
        for index in range(10):
            for value in [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]:
                data_signal.write(value)
                time.sleep(0.001)
                read_value = data_signal.read()
                if read_value != value:
                    print('ERROR!')
                    error_count += 1
                print(data_signal.signal_name, index, value, read_value)
    print('errors = ', error_count)
