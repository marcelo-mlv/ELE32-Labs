from modules.Channel import AWGNChannel
from modules.LDPC_LLR import LDPC_LLR

import numpy as np
import matplotlib.pyplot as plt


channel = AWGNChannel()

dv = 3
dc = 7
N = 994 #98, 994, 1001
decode_max_iter = 20
graph = LDPC_LLR(dv, dc, N)
graph.export_to_csv('ldpc_graph.csv')

snr_values_dB = np.arange(-2, 5.5, 0.5) 
snr_values = 10 ** (snr_values_dB/10)               
pb_values = np.zeros(len(snr_values))

s_symbols = np.full(N, 1, dtype=int)

for k in range(len(snr_values)):

    Nzero = 1 / snr_values[k]
    r_symbols = channel.transmit(s_symbols, Nzero)

    decoded_symbols = graph.decode(r_symbols, Nzero, decode_max_iter)

    num_of_flipped_symbols = 0
    for s in decoded_symbols:
        if s == -1:
            num_of_flipped_symbols += 1
    pb_values[k] = num_of_flipped_symbols / N

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Iteration no. {k+1}")
    # print(f"r: {r_symbols}")
    # print(f"decoded: {decoded_symbols}")
    print(f"snr: {snr_values_dB[k]} dB")
    print(f"pb: {pb_values[k]}")

"""
Plots the bit error probability as a function of the signal-to-noise ratio (dB).
    x axis: snr_values, in logarithmic scale
    y axis: pb_values, in logarithmic scale
"""
plt.figure()
plt.plot(snr_values_dB, pb_values)
# plt.xscale('log')
plt.yscale('log')
plt.xlabel('snr (dB)')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x relação sinal-ruído")
plt.grid(True)
# plt.legend()
# plt.gca().invert_xaxis()
plt.savefig("plot.png", format="png")
plt.show()