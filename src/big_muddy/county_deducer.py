# Copyright 2022 WillyMillsLLC

def county_deducer(daisy_units_actual):
    for burliegh in range(4):
        for morton in range(4):
            daisy_units_expected = burliegh * 3 + morton * 4
            if daisy_units_expected == daisy_units_actual:
                return burliegh, morton
    return None
