from districts import normalize_cube_dictionary_list

"""
Describe the console blocks for the two counties
"""

MORTON_COUNTY_TURNOUTS = normalize_cube_dictionary_list("Morton", "turnout", [
    {
        "direction": "left",
        "name": "rejoin yard",
        "color": "purple",
        "row": 0,
        "column": 7,
        "console_socket": 4,
        "servo_socket": 4
    },
    {
        "direction": "left",
        "name": "rejoin main",
        "color": "purple+green",
        "row": 0,
        "column": 5,
        "console_socket": 13,
        "servo_socket": 13,
    },
    {
        "direction": "left",
        "name": "staging",
        "color": "gray+black",
        "row": 0,
        "column": 0,
        "console_socket": 8,
        "servo_socket": 8,
    },
    {
        "direction": "left",
        "name": "fore to main",
        "color": "orange+green",
        "row": 5,
        "column": 2,
        "console_socket": 14,
        "servo_socket": 14,
    },
    {
        "direction": "left",
        "name": "yard to depot",
        "color": "pink+yellow",
        "row": 5,
        "column": 3,
        "console_socket": 15,
        "servo_socket": 15,
    },
    {
        "direction": "right",
        "name": "depot to siding",
        "color": "yellow",
        "row": 3,
        "column": 3,
        "console_socket": 12,
        "servo_socket": 12,
    },
    {
        "direction": "left",
        "name": "depot merge",
        "color": "purple+yellow",
        "row": 2,
        "column": 4,
        "console_socket": 10,
        "servo_socket": 10,
    },
    {
        "direction": "left",
        "name": "yard A rejoin",
        "color": "purple+pink",
        "row": 2,
        "column": 5,
        "console_socket": 6,
        "servo_socket": 6,
    },
    {
        "direction": "left",
        "name": "yard B rejoin",
        "color": "purple+pink",
        "row": 2,
        "column": 6,
        "console_socket": 2,
        "servo_socket": 2,
    },
    {
        "direction": "right",
        "name": "yard C rejoin",
        "color": "pink+purple",
        "row": 2,
        "column": 7,
        "console_socket": 5,
        "servo_socket": 5,
    },
    {
        "direction": "left",
        "name": "yard A",
        "color": "pink",
        "row": 5,
        "column": 5,
        "console_socket": 1,
        "servo_socket": 1,
    },
    {
        "direction": "left",
        "name": "yard B",
        "color": "pink",
        "row": 5,
        "column": 6,
        "console_socket": 3,
        "servo_socket": 3,
    },
    {
        "direction": "left",
        "name": "yard C",
        "color": "pink",
        "row": 5,
        "column": 7,
        "console_socket": 0,
        "servo_socket": 0,
    },
    {
        "direction": "left",
        "name": "main to refinery",
        "color": "blue+green",
        "row": 1,
        "column": 3,
        "console_socket": 11,
        "servo_socket": 11,
    },
    {
        "direction": "left",
        "name": "refinery split",
        "color": "blue",
        "row": 1,
        "column": 1,
        "console_socket": 9,
        "servo_socket": 9,
    },
])
BURLEIGH_COUNTY_TURNOUTS = normalize_cube_dictionary_list("Burleigh", "turnout", [
    {
        # Correctly detects state
        # Can divert
        # ALIGN MAIN FAILS WEAK
        "direction": "right",
        "name": "rejoin main",
        "color": "purple",
        "row": 0,
        "column": 2,
        "console_socket": 0,
        "servo_socket": 0,
        "servo_half": 1,
    },
    {
        # Correctly detected
        # Direction is controlled.
        "direction": "right",
        "name": "depot west",
        "color": "green+orange",
        "inverted": 1,
        "row": 0,
        "column": 3,
        "console_socket": 1,
        "servo_socket": 0,
        "servo_half": 0,
    },
    {
        # Correctly detected
        # CONTROL TOO WEAK
        "direction": "left",
        "name": "depot east",
        "color": "green+orange",
        "row": 0,
        "column": 6,
        "console_socket": 2,
        "servo_socket": 3,
        "servo_half": 0,
    },
    { # No detection
        "direction": "right",
        "name": "depot to yard",
        "color": "orange",
        "row": 1,
        "column": 4,
        "console_socket": 3,
        "servo_socket": 1,
        "servo_half": 0,
    },
    { # No detection
        "direction": "right",
        "name": "yard to commerce",
        "color": "orange+yellow",
        "row": 2,
        "column": 5,
        "console_socket": 4,
        "servo_socket": 1,
        "servo_half": 1,
    },
    { # No detection
        "direction": "right",
        "name": "yard to siding",
        "color": "orange",
        "row": 2,
        "column": 6,
        "console_socket": 5,
        "servo_socket": 2,
        "servo_half": 0,
    },
    { # Correctly detected
        "direction": "right",
        "name": "back yard",
        "color": "yellow",
        "inverted": 1,
        "row": 4,
        "column": 6,
        "console_socket": 6,
        "servo_socket": 3,
        "servo_half": 1,
    },
    { # Intermittent detection
        "direction": "right",
        "name": "main to flat",
        "color": "blue+gray",
        "row": 5,
        "column": 5,
        "console_socket": 7,
        "servo_socket": 2,
        "servo_half": 1,
    },
])

MORTON_COUNTY_BLOCKS = normalize_cube_dictionary_list("Morton", "block", [
    {
        "name": "rejoin",
        "color": "purple",
        "row": 0,
        "column": 6,
        "console_socket": 3,
        "servo_socket": 3,
    },
    {
        "name": "main",
        "color": "gray",
        "row": 0,
        "column": 3,
        "console_socket": 5,
        "servo_socket": 5,
    },
    {
        "name": "loop",
        "color": "black",
        "row": 3,
        "column": 0,
        "console_socket": 4,
        "servo_socket": 4,
    },
    {
        "name": "fore",
        "color": "orange",
        "row": 5,
        "column": 1,
        "console_socket": 7,
        "servo_socket": 7,
    },
    {
        "name": "through",
        "color": "green",
        "row": 1,
        "column": 4,
        "console_socket": 2,
        "servo_socket": 2,
    },
    {
        "name": "refinery",
        "color": "blue",
        "row": 1,
        "column": 2,
        "console_socket": 6,
        "servo_socket": 6,
    },
    {
        "name": "depot",
        "color": "yellow",
        "row": 4,
        "column": 3,
        "console_socket": 0,
        "servo_socket": 0,
    },
    {
        "name": "yard",
        "color": "pink",
        "row": 5,
        "column": 4,
        "console_socket": 1,
        "servo_socket": 1,
    },
])
BURLEIGH_COUNTY_BLOCKS = normalize_cube_dictionary_list("Burleigh", "block", [
    {
        "name": "bridge",
        "color": "brown",
        "row": 4,
        "column": 0,
        "console_socket": 1,
        "servo_socket": 1,
    },
    {
        "name": "rejoin",
        "color": "purple",
        "row": 0,
        "column": 1,
        "console_socket": 7,
        "servo_socket": 7,
    },
    {
        "name": "main",
        "color": "green",
        "row": 0,
        "column": 7,
        "console_socket": 6,
        "servo_socket": 6,
    },
    {
        "name": "loop",
        "color": "black",
        "row": 3,
        "column": 8,
        "console_socket": 4,
        "servo_socket": 4,
    },
    {
        "name": "flats",
        "color": "blue",
        "row": 5,
        "column": 4,
        "console_socket": 0,
        "servo_socket": 0,
    },
    {
        "name": "crossing",
        "color": "gray",
        "row": 4,
        "column": 5,
        "console_socket": 3,
        "servo_socket": 3,
    },
    {
        "name": "depot",
        "color": "orange",
        "row": 1,
        "column": 5,
        "console_socket": 5,
        "servo_socket": 5,
    },
    {
        "name": "commerce",
        "color": "yellow",
        "row": 1,
        "column": 5,
        "console_socket": 2,
        "servo_socket": 2,
    },
])

MORTON_COUNTY_CUBE_RECIPES = MORTON_COUNTY_TURNOUTS + MORTON_COUNTY_BLOCKS
BURLEIGH_COUNTY_CUBE_RECIPES = BURLEIGH_COUNTY_TURNOUTS + BURLEIGH_COUNTY_BLOCKS
BIG_MUDDY_CUBE_RECIPES = MORTON_COUNTY_CUBE_RECIPES + BURLEIGH_COUNTY_CUBE_RECIPES
