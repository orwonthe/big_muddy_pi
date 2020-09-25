def duration_testing(big_muddy):
    print("Duration testing")
    big_muddy.determine_durations()
    for data_signal in big_muddy.data_signals:
        print(data_signal.signal_name, data_signal.duration, " / 24 = ", data_signal.duration / 24)
    print(big_muddy.duration)


def duration_check(big_muddy=None):
    if big_muddy is None:
        durations = [
            {
                'name': 'this',
                'bits': 48,
                'daisy': 2
            },
            {
                'name': 'that',
                'bits': 72,
                'daisy': 3
            },
        ]
    else:
        big_muddy.determine_durations()
        durations = [
            {
                'name':data_signal.signal_name,
                'bits': data_signal.duration,
                'daisy': data_signal.duration // 24
            }
            for data_signal in big_muddy.data_signals
        ] + [
            {
                'name': "Max",
                'bits': big_muddy.max_duration,
                'daisy': big_muddy.max_duration // 24
            }
        ]
    return durations
