def set_and_shift_values(big_muddy_io, values):
    for value in values:
        set_and_shift_single(big_muddy_io, value)


def set_and_shift_single(big_muddy_io, value):
    big_muddy_io.set_data_pins(value)
    big_muddy_io.shifting.pulse()