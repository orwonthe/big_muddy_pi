def duration_testing(big_muddy):
    print("Duration testing")
    big_muddy.determine_durations()
    for data_signal in big_muddy.data_signals:
        print(data_signal.signal_name, data_signal.duration)
    print(big_muddy.duration)
