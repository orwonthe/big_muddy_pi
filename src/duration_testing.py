from big_muddy_io import BigMuddyIO


def duration_testing(big_muddy=None):
    print("Duration testing")
    if big_muddy is None:
        big_muddy = BigMuddyIO.system()
    big_muddy.determine_durations()
    for data_signal in big_muddy.data_signals:
        print(data_signal.signal_name, data_signal.duration)
    print(big_muddy.duration)
