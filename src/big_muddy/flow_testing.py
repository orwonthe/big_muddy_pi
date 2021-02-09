from big_muddy_io import BigMuddyIO
from big_muddy_util import set_and_shift_values


def flow_testing():
    print('Flow testing.')
    big_muddy_io = BigMuddyIO.system()
    while True:
        set_and_shift_values([0, 0, 0, 1, 1])


