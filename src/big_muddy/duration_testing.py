def duration_testing(big_muddy_io):
    print("Duration testing")
    big_muddy_io.determine_durations()
    for data_signal in big_muddy_io.data_signals:
        print(data_signal.signal_name, data_signal.duration, " / 24 = ", data_signal.duration / 24)
    print(big_muddy_io.duration)


