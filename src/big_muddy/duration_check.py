# Copyright 2022 WillyMillsLLC
from big_muddy_io import BigMuddyIO


def duration_check():
    big_muddy_io = BigMuddyIO.system()
    big_muddy_io.determine_durations()
    durations = [
                    {
                        'name': data_signal.signal_name,
                        'bits': data_signal.duration,
                        'daisy': data_signal.duration // 24
                    }
                    for data_signal in big_muddy_io.data_signals
                ] + [
                    {
                        'name': "Max",
                        'bits': big_muddy_io.max_duration,
                        'daisy': big_muddy_io.max_duration // 24
                    }
                ]
    return durations
