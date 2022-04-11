import numpy as np

x_r = np.array([
    0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90,
    1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90,
    2.00, 2.10, 2.20, 2.30, 2.40, 2.50, 2.60, 2.70, 2.80, 2.90,
    3.00, 3.10, 3.20, 3.30, 3.40, 3.50, 3.60, 3.70, 3.80, 3.90,
    4.00, 4.10, 4.20, 4.30, 4.40, 4.50, 4.60, 4.70, 4.80, 4.90
])

y_g = np.array([
    1.0000, 2.2667, 3.5533, 4.8599, 6.1865, 7.5332, 8.8998, 10.2865, 11.6931, 13.1197,
    14.5664, 16.0330, 17.5196, 19.0263, 20.5529, 22.0996, 23.6662, 25.2528, 26.8595, 28.4861,
    30.1327, 31.7994, 33.4860, 35.1927, 36.9193, 38.6659, 40.4326, 42.2192, 44.0258, 45.8525,
    47.6991, 49.5657, 51.4524, 53.3590, 55.2857, 57.2323, 59.1989, 61.1856, 63.1922, 65.2188,
    67.2655, 69.3321, 71.4188, 73.5254, 75.6520, 77.7987, 79.9653, 82.1519, 84.3586, 86.5852
])


# returns double, int neurons, inputw, inputv, bias
def calc_neuron(neurons, input_weights, input_values, bias):
    suma = bias
    for i in range(0, neurons):
        suma += input_weights[i] * input_values[i]
    return suma


L1N = 4
L2N = 4

layer1 = np.ndarray(shape=(L1N, 1))
layer2 = np.ndarray(shape=(L2N, L1N))
layer3 = np.ndarray(shape=(1, L2N))

bias1 = np.empty(shape=L1N)
bias2 = np.empty(shape=L2N)
bias3 = np.empty(shape=1)

output0 = np.empty(shape=1)
output1 = np.empty(shape=L1N)
output2 = np.empty(shape=L2N)


def main(argv):
    y_r = y_g

    total_expected_args = 1 + L1N + L1N * L2N + L2N + L1N + L2N

    argc = len(argv)

    if argc != total_expected_args:
        print("Broj argumenata nije odgovarajuci")
        return -1

    ai = 0

    # layer1
    for i in range(0, L1N):
        layer1[i][0] = argv[ai]
        ai += 1

    # layer2
    for i in range(0, L2N):
        for j in range(0, L1N):
            layer2[i][j] = argv[ai]
            ai += 1

    # layer3
    for i in range(0, L2N):
        layer3[0][i] = argv[ai]

    # bias1
    for i in range(0, L1N):
        bias1[i] = argv[ai]
        ai += 1

    # bias2
    for i in range(0, L2N):
        bias2[i] = argv[ai]
        ai += 1

    # bias3
    bias3[0] = argv[ai]

    # idemo dalje!
    mse = 0

    for k in range(0, 50):
        # print("mse: " + str(mse))
        output0[0] = x_r[k]

        # layer1
        for i in range(0, L1N):
            output1[i] = calc_neuron(1, layer1[i], output0, bias1[i])

        # layer2
        for i in range(0, L2N):
            output2[i] = calc_neuron(L1N, layer2[i], output1, bias2[i])

        # layer3
        val = calc_neuron(L2N, layer3[0], output2, bias3[0])

        err = (y_r[k] - val) ** 2
        mse += err

    return mse / 50
