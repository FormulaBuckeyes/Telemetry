import serial


# Adjust the scaling of the data
def scale(data, scaling):
    return float(data * scaling)


def package(data, index, map):
    map.update(keys[index], data)


def readInput(input):
    inputArray = bytearray()

    ends = bytearray([80, 81, 82])
    end_count = 0

    while end_count < 3:

        # c is of type bytes
        c = input.read(1)

        if c not in ends:
            inputArray.extend(c)

        else:
            end_count += 1

    return inputArray

input = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    bytesize=serial.EIGHTBITS)
input.flushInput()

telemetry = {
    "rpm":
        {"scaling": 1, "offset": 1, "location": 0, "value": None},

    "throttle_pos":
        {"scaling": 0.1, "offset": 1, "location": 2, "value": None},

    "Manifold_Pressure":
        {"scaling": 0.1, "offset": 1, "location": 4, "value": None},

    "Air_Temperature":
        {"scaling": 0.1, "offset": 1, "location": 6, "value": None},

    "Engine_Temperature":
        {"scaling": 0.1, "offset": 1, "location": 8, "value": None},

    "Lamda_1":
        {"scaling": 0.1, "offset": 1, "location": 10, "value": None},

    "Lamda_2":
        {"scaling": 0.001, "offset": 1, "location": 12, "value": None},

    "Exhaust_Manifold_Pressure":
        {"scaling": 0.1, "offset": 1, "location": 14, "value": None},

    "Mass_Air_Flow":
        {"scaling": 0.1, "offset": 1, "location": 16, "value": None}
}

while True:
    readInput(input)
    scale()
