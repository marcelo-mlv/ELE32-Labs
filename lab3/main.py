from modules.Channel import AWGNChannel
from modules.LDPC_LLR import LDPC_LLR

import numpy as np
import matplotlib.pyplot as plt

### CHANNEL ###
channel = AWGNChannel()

### LDPC ###
# rate = 4/7 #
dv = 3
dc = 7
N = 994 #98, 994, 1001
decode_max_iter = 50
graph = LDPC_LLR(dv, dc, N)
# EXPORT #
graph.export_to_csv('ldpc_graph.csv')

### PLOT ###
snr_values_dB = np.arange(0, 5.5, 0.5) 
snr_values = 10 ** (snr_values_dB/10)               
pb_values = np.zeros(len(snr_values))
samples = 5
# INPUT #
s_symbols = np.full(N, 1, dtype=int)

for k in range(len(snr_values)):

    Nzero = 1 / snr_values[k]

    ### SAMPLES ###
    num_of_flipped_symbols = 0
    for _ in range(samples):
    
        r_symbols = channel.transmit(s_symbols, Nzero)

        decoded_symbols = graph.decode(r_symbols, Nzero, decode_max_iter)

        for s in decoded_symbols:
            if s == -1:
                num_of_flipped_symbols += 1

    pb_values[k] = num_of_flipped_symbols / (N*samples)

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Point no. {k+1}")
    print(f"snr: {snr_values_dB[k]} dB")
    print(f"pb: {pb_values[k]}")

"""
Plots the bit error probability as a function of the signal-to-noise ratio (dB).
    y axis: pb_values, in logarithmic scale
    x axis: snr_values_dB
"""
plt.figure()
plt.plot(snr_values_dB, pb_values)
plt.yscale('log')
plt.xlabel('snr (dB)')
plt.ylabel('Pb')
plt.title("AWGN channel / LDPC code, using LLR, rate = 4/7, N = 994")
plt.grid(True)
plt.savefig("plot.png", format="png")
plt.show()