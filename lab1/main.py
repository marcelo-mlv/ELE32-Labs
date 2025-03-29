from modules.Encoder import HammingEncoder, MyEncoder
from modules.Decoder import HammingDecoder, MyDecoder
from modules.Channel import BinarySymmetricChannel
from modules.System import System

import random
import numpy as np
import matplotlib.pyplot as plt

# System declaration

hamming_encoder = HammingEncoder()
hamming_decoder = HammingDecoder()
bsc = BinarySymmetricChannel()
my_encoder = MyEncoder()
my_decoder = MyDecoder()

channel_only = System(None, None, bsc)
hamming_system = System(hamming_encoder, hamming_decoder, bsc)
my_system = System(my_encoder, my_decoder, bsc)

n_iterations = 20

p_values = np.logspace(-5, np.log10(0.5), n_iterations) # Probability of a bit being flipped during transmission
hamming_pb_values = np.zeros(p_values.size) # System bit error probability (hamming)
co_pb_values = np.zeros(p_values.size) #      System bit error probability (channel only)
my_pb_values = np.zeros(p_values.size) #      System bit error probability (custom)

sample_size = np.logspace(4, 7, p_values.size, dtype=int)[::-1]

for k in range(p_values.size):
    """
    Simulates the transmission of random bits through 2 systems
    and calculates the bit error probability for different values of p.
        System 1: Channel Only
        System 2: Hamming Encoding and Decoding
        System 2: Custom Encoding and Decoding
    Both systems use BSC as channel.
    """
    
    random_bits = [random.randint(0, 1) for _ in range(sample_size[k] - sample_size[k]%20)]
    
    flipped_bits = {"System 1": 0, "System 2": 0, "System 3": 0}

    # System 1
    channel_bits = channel_only.process(random_bits.copy(), p_values[k])

    for j in range(len(random_bits)):
        if random_bits[j] != channel_bits[j]:
            flipped_bits["System 1"] += 1
    
    co_pb_values[k] = flipped_bits["System 1"] / len(random_bits)

    # System 2
    for i in range(0, len(random_bits), 4):

        u = random_bits[i:i+4]
    
        v_hat = hamming_system.process(u.copy(), p_values[k])
        u_hat = v_hat[:4]

        for j in range(len(u)):
            if u[j] != u_hat[j]:
                flipped_bits["System 2"] += 1

    hamming_pb_values[k] = flipped_bits["System 2"] / len(random_bits)

    # System 3
    for i in range(0, len(random_bits), 5):

        u = random_bits[i:i+5]
    
        v_hat = my_system.process(u.copy(), p_values[k])
        u_hat = v_hat[:5]

        for j in range(len(u)):
            if u[j] != u_hat[j]:
                flipped_bits["System 3"] += 1

    my_pb_values[k] = flipped_bits["System 3"] / len(random_bits)

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Iteration no. {k+1}")
    print(f"Sample size: {sample_size[k]}")
    print(f"p: {p_values[k]}")
    print(f"\tCHANNEL ONLY: pb = {co_pb_values[k]:.7f}")
    print(f"\tHAMMING:      pb = {hamming_pb_values[k]:.7f}")
    print(f"\tCUSTOM:       pb = {my_pb_values[k]:.7f}")

"""
Plots the bit error probability as a function of the probability of a bit being flipped during transmission.
    x axis: p_values (list), reversed, in logarithmic scale
    y axis: pb_values (list), in logarithmic scale
"""
plt.figure()
plt.plot(p_values, hamming_pb_values, marker='o', label='Hamming')
plt.plot(p_values, co_pb_values, marker='x', label='Somente Canal')
plt.plot(p_values, my_pb_values, marker='o', label='Canal Próprio')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('P')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x prob. inversão de bit no canal")
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()

# Save the plot as a PNG file
plt.savefig("plot.png", format="png")

plt.show()
