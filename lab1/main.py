from modules.HammingEncoder import HammingEncoder
from modules.HammingDecoder import HammingDecoder
from modules.BinarySymmetricChannel import BinarySymmetricChannel
from modules.System import System

import random
import numpy as np
import matplotlib.pyplot as plt

encoder = HammingEncoder()
decoder = HammingDecoder()
bsc = BinarySymmetricChannel()

p_values = np.logspace(-5, np.log10(0.5), 20) # Probability of a bit being flipped during transmission
pb_values = p_values.copy() # Bit error probability

sample_size = 10000
random_bits = [random.randint(0, 1) for _ in range(sample_size)]

for k in range(p_values.size):
    """
    Simulates the transmission of random bits through a binary symmetric channel
    and calculates the bit error probability for different values of p.
    """
    flipped_bits = 0

    for i in range(0, len(random_bits), 4):
        u = random_bits[i:i+4]
        v = encoder.encode(u)
        r = bsc.transmit(v, p_values[k])
        v_hat = decoder.decode(r)
        u_hat = v_hat[:4]

        for j in range(4):
            if u[j] != u_hat[j]:
                flipped_bits += 1

    pb = flipped_bits / sample_size
    pb_values[k] = pb

"""
Plots the bit error probability as a function of the probability of a bit being flipped during transmission.
    x axis: p_values (list), reversed, in logarithmic scale
    y axis: pb_values (list), in logarithmic scale
"""
plt.figure()
plt.plot(p_values, pb_values, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('P')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x prob. inversão de bit no canal")
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
