from big_muddy.districts import normalize

MORTON_COUNTY_TURNOUTS = normalize("morton", "turnout", [
    {
        "direction": "left",
        "name": "rejoin yard",
        "color": "purple",
        "row": 0,
        "column": 7,
        "socket": 4
    },
    {
        "direction": "left",
        "name": "rejoin main",
        "color": "purple+green",
        "row": 0,
        "column": 5,
        "socket": 13
    },
    {
        "direction": "left",
        "name": "staging",
        "color": "gray+black",
        "row": 0,
        "column": 0,
        "socket": 8
    },
    {
        "direction": "left",
        "name": "fore to main",
        "color": "orange+green",
        "row": 5,
        "column": 2,
        "socket": 14
    },
    {
        "direction": "left",
        "name": "yard to depot",
        "color": "pink+yellow",
        "row": 5,
        "column": 3,
        "socket": 15
    },
    {
        "direction": "right",
        "name": "depot to siding",
        "color": "yellow",
        "row": 3,
        "column": 3,
        "socket": 12
    },
    {
        "direction": "left",
        "name": "depot merge",
        "color": "purple+yellow",
        "row": 2,
        "column": 4,
        "socket": 10
    },
    {
        "direction": "left",
        "name": "yard A rejoin",
        "color": "purple+pink",
        "row": 2,
        "column": 5,
        "socket": 6
    },
    {
        "direction": "left",
        "name": "yard B rejoin",
        "color": "purple+pink",
        "row": 2,
        "column": 6,
        "socket": 2
    },
    {
        "direction": "right",
        "name": "yard C rejoin",
        "color": "pink+purple",
        "row": 2,
        "column": 7,
        "socket": 5
    },
    {
        "direction": "left",
        "name": "yard A",
        "color": "pink",
        "row": 5,
        "column": 5,
        "socket": 1
    },
    {
        "direction": "left",
        "name": "yard B",
        "color": "pink",
        "row": 5,
        "column": 6,
        "socket": 3
    },
    {
        "direction": "left",
        "name": "yard C",
        "color": "pink",
        "row": 5,
        "column": 7,
        "socket": 0
    },
    {
        "direction": "left",
        "name": "main to refinery",
        "color": "blue+green",
        "row": 1,
        "column": 3,
        "socket": 11
    },
    {
        "direction": "left",
        "name": "refinery split",
        "color": "blue",
        "row": 1,
        "column": 1,
        "socket": 9
    },
])
BURLEIGH_COUNTY_TURNOUTS = normalize("burleigh", "turnout", [
    {
        "direction": "right",
        "name": "rejoin main",
        "color": "purple",
        "row": 0,
        "column": 2,
        "socket": 0
    },
    {
        "direction": "right",
        "name": "depot west",
        "color": "green+orange",
        "row": 0,
        "column": 3,
        "socket": 1
    },
    {
        "direction": "left",
        "name": "depot east",
        "color": "green+orange",
        "row": 0,
        "column": 6,
        "socket": 2
    },
    {
        "direction": "right",
        "name": "depot to yard",
        "color": "orange",
        "row": 1,
        "column": 4,
        "socket": 3
    },
    {
        "direction": "right",
        "name": "yard to commerce",
        "color": "orange+yellow",
        "row": 2,
        "column": 5,
        "socket": 4
    },
    {
        "direction": "right",
        "name": "yard to siding",
        "color": "orange",
        "row": 2,
        "column": 6,
        "socket": 5
    },
    {
        "direction": "right",
        "name": "back yard",
        "color": "yellow",
        "row": 4,
        "column": 6,
        "socket": 6
    },
    {
        "direction": "right",
        "name": "main to flat",
        "color": "blue+gray",
        "row": 5,
        "column": 5,
        "socket": 7
    },
])

MORTON_COUNTY_BLOCKS = normalize("morton", "block", [
    {
        "name": "rejoin",
        "color": "purple",
        "row": 0,
        "column": 6,
        "socket": 3
    },
    {
        "name": "main",
        "color": "gray",
        "row": 0,
        "column": 3,
        "socket": 5
    },
    {
        "name": "loop",
        "color": "black",
        "row": 3,
        "column": 0,
        "socket": 4
    },
    {
        "name": "fore",
        "color": "orange",
        "row": 5,
        "column": 1,
        "socket": 7
    },
    {
        "name": "through",
        "color": "green",
        "row": 1,
        "column": 4,
        "socket": 2
    },
    {
        "name": "refinery",
        "color": "blue",
        "row": 1,
        "column": 2,
        "socket": 6
    },
    {
        "name": "depot",
        "color": "yellow",
        "row": 4,
        "column": 3,
        "socket": 0
    },
    {
        "name": "yard",
        "color": "pink",
        "row": 5,
        "column": 4,
        "socket": 1
    },
])
BURLEIGH_COUNTY_BLOCKS = normalize("burleigh", "block", [
    {
        "name": "bridge",
        "color": "brown",
        "row": 4,
        "column": 0,
        "socket": 1
    },
    {
        "name": "rejoin",
        "color": "purple",
        "row": 0,
        "column": 1,
        "socket": 7
    },
    {
        "name": "main",
        "color": "green",
        "row": 0,
        "column": 7,
        "socket": 6
    },
    {
        "name": "loop",
        "color": "black",
        "row": 3,
        "column": 8,
        "socket": 4
    },
    {
        "name": "flats",
        "color": "blue",
        "row": 5,
        "column": 4,
        "socket": 0
    },
    {
        "name": "crossing",
        "color": "gray",
        "row": 4,
        "column": 5,
        "socket": 3
    },
    {
        "name": "depot",
        "color": "orange",
        "row": 1,
        "column": 5,
        "socket": 5
    },
    {
        "name": "commerce",
        "color": "yellow",
        "row": 1,
        "column": 5,
        "socket": 2
    },
])

MORTON_COUNTY_DISTRICTS = (MORTON_COUNTY_TURNOUTS, MORTON_COUNTY_BLOCKS)
BURLEIGH_COUNTY_DISTRICTS = (BURLEIGH_COUNTY_TURNOUTS, BURLEIGH_COUNTY_BLOCKS)
BIG_MUDDY_DISTRICTS = [MORTON_COUNTY_DISTRICTS, BURLEIGH_COUNTY_DISTRICTS]
