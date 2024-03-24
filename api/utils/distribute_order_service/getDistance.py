DISTANCE_MATRIX = [
    [
        0,
        50226,
        20869,
        27562,
        9671,
        22410,
        25208,
        25695,
        27804,
        25370,
        19683,
        15950,
        31576,
        12040,
        28730,
        23181,
        22089,
    ],
    [
        27562,
        0,
        36646,
        38976,
        33100,
        23792,
        34437,
        26030,
        30335,
        29669,
        28513,
        14058,
        25783,
        16672,
        30010,
        24563,
        16274,
    ],
    [
        20723,
        41045,
        0,
        48598,
        35082,
        38035,
        46244,
        40914,
        45562,
        43913,
        40719,
        23342,
        43033,
        24254,
        44163,
        38806,
        33524,
    ],
    [
        30704,
        58250,
        49241,
        0,
        18082,
        15204,
        2568,
        11305,
        7391,
        6750,
        11762,
        31503,
        17294,
        27593,
        8317,
        13730,
        23320,
    ],
    [
        11002,
        52335,
        35798,
        18218,
        0,
        12496,
        15864,
        15770,
        18460,
        16026,
        10339,
        18059,
        20079,
        14149,
        19385,
        15418,
        20283,
    ],
    [
        23118,
        42866,
        38258,
        15146,
        12637,
        0,
        12776,
        5384,
        8648,
        8009,
        10390,
        15329,
        7934,
        17887,
        7603,
        2909,
        6204,
    ],
    [
        28524,
        58510,
        47061,
        2568,
        15901,
        12420,
        0,
        9312,
        5398,
        4757,
        9582,
        29322,
        17553,
        25412,
        6323,
        11737,
        23579,
    ],
    [
        26411,
        45368,
        41072,
        10779,
        15740,
        4776,
        11796,
        0,
        4500,
        5933,
        8861,
        18143,
        4495,
        18484,
        3624,
        2671,
        10438,
    ],
    [
        30978,
        49686,
        46521,
        8046,
        18356,
        8506,
        8194,
        4338,
        0,
        2195,
        8335,
        23592,
        8812,
        20981,
        1554,
        6764,
        14755,
    ],
    [
        28625,
        48189,
        43581,
        6547,
        16003,
        8058,
        6456,
        5885,
        2297,
        0,
        5940,
        20652,
        10973,
        19331,
        3011,
        7316,
        13376,
    ],
    [
        20044,
        48338,
        38581,
        12856,
        7430,
        10631,
        10502,
        9099,
        8227,
        5931,
        0,
        20843,
        13349,
        16933,
        7931,
        9890,
        15978,
    ],
    [
        18280,
        33773,
        23544,
        28258,
        20850,
        15243,
        32013,
        18122,
        22770,
        21121,
        17023,
        0,
        20241,
        4413,
        21371,
        16014,
        10732,
    ],
    [
        29211,
        44459,
        42538,
        17956,
        19838,
        7991,
        19898,
        4767,
        9072,
        11368,
        15538,
        19609,
        0,
        22167,
        8747,
        6054,
        9528,
    ],
    [
        11721,
        36536,
        25337,
        27807,
        14291,
        17726,
        25453,
        18211,
        20255,
        18606,
        19928,
        4446,
        22724,
        0,
        18855,
        18497,
        13215,
    ],
    [
        30454,
        49802,
        45195,
        8452,
        17831,
        7181,
        9284,
        3555,
        1378,
        3043,
        7768,
        22266,
        8650,
        19089,
        0,
        5818,
        14593,
    ],
    [
        23792,
        43539,
        38932,
        12805,
        15029,
        2635,
        13316,
        2077,
        6525,
        7287,
        10814,
        16003,
        5779,
        18561,
        5288,
        0,
        8563,
    ],
    [
        21167,
        34961,
        33039,
        23559,
        19163,
        6991,
        18400,
        10613,
        14918,
        13633,
        14575,
        10111,
        10366,
        12669,
        14593,
        7749,
        0,
    ],
]
CUSTOMER = [
    (25, 0),
    (14, 1),
    (7, 2),
    (17, 3),
    (9, 4),
    (8, 5),
    (21, 6),
    (16, 7),
    (20, 8),
    (24, 9),
    (15, 10),
    (18, 11),
    (13, 12),
    (23, 13),
    (19, 14),
    (10, 15),
    (22, 16),
]


def getDistance(a, b):
    matrixA = 0
    matrixB = 0
    for customer in CUSTOMER:
        if customer[0] == a:
            matrixA = customer[1]
        if customer[0] == b:
            matrixB = customer[1]
    return DISTANCE_MATRIX[matrixA][matrixB]


def getTotalDistance(lst):
    total = 0
    for idx in range(0, len(lst) - 1):
        total += getDistance(lst[idx], lst[idx + 1])
    return total


print(getTotalDistance([0, 23, 0]))
