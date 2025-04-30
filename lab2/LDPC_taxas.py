from modules.Channel import BinarySymmetricChannel
from modules.LDPCgraph import LDPCgraph
from modules.LDPCdecoder import bit_flipping_decoder

import numpy as np
import matplotlib.pyplot as plt

bsc = BinarySymmetricChannel()

bit_flipping_max_iter = 50 

n_iterations = 20
p_values = np.logspace(-2, np.log10(0.5), n_iterations)       # Probability of a bit being flipped during transmission          
LDPC_pb_values = np.zeros((4, p_values.size))                # System bit error probability (LDPC)

for k in range(p_values.size):
    
    flipped_bits = np.zeros(4)
    dv = [2, 3, 2, 2]
    dc= [6, 7, 4, 3]
    N = [996, 994, 1000, 999]
   
    for i in range(4):
        input_bits = np.zeros(N[i], dtype=int)
        channel_bits = bsc.transmit(input_bits, p_values[k])
        decoded_bits = bit_flipping_decoder(LDPCgraph(N[i],dv[i],dc[i]), channel_bits, bit_flipping_max_iter)
        for bit in decoded_bits:
            if bit == 1:
                flipped_bits[i] += 1
        LDPC_pb_values[i][k] = flipped_bits[i] / N[i]
       

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Iteration no. {k+1}")
    print(f"p: {p_values[k]}")
    print(f"\tLDPC 2/3, N~1000:   pb = {LDPC_pb_values[0][k]:.7f}")
    print(f"\tLDPC 4/7, N~1000:   pb = {LDPC_pb_values[1][k]:.7f}")
    print(f"\tLDPC 1/2, N~1000:   pb = {LDPC_pb_values[2][k]:.7f}")
    print(f"\tLDPC 1/3, N~1000:   pb = {LDPC_pb_values[3][k]:.7f}")

"""
Plots the bit error probability as a function of the probability of a bit being flipped during transmission.
    x axis: p_values (list), reversed, in logarithmic scale
    y axis: pb_values (list), in logarithmic scale
"""
plt.figure()
plt.plot(p_values, LDPC_pb_values[0], label='LDPC 2/3 N~1000')
plt.plot(p_values, LDPC_pb_values[1], label='LDPC 4/7 N~1000')
plt.plot(p_values, LDPC_pb_values[2], label='LDPC 1/2 N~1000')
plt.plot(p_values, LDPC_pb_values[3], label='LDPC 1/3 N~1000')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('P')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x prob. inversão de bit no canal")
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()

# Save the plot as a PNG file
plt.savefig("plot_taxas.png", format="png")

plt.show()