from BinarySymmetricChannel import BinarySymmetricChannel as BSC
from Encoder import Encoder
import matplotlib.pyplot as plt

import random
import numpy as np

encoder = Encoder()

p_values = np.logspace(-5, np.log10(0.5), 20)
pb_values = p_values.copy()

random_bits = [random.randint(0, 1) for _ in range(1000000)]

for k in range(p_values.size):

    number_of_errors = 0

    for i in range(0, len(random_bits), 4):

        u = random_bits[i:i+4]
            
        v = encoder.encode(u)

        r = BSC(v, p_values[k])

        v_hat = encoder.decode(r)

        u_hat = v_hat[:4]

        for j in range(4):
            if u[j] != u_hat[j]:
                number_of_errors += 1

    pb = number_of_errors / 1000000
    pb_values[k] = pb

plt.figure()
plt.plot(p_values, pb_values, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('P')
plt.ylabel('Pb')
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
