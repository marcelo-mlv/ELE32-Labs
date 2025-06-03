from modules.Channel import AWGNChannel
from modules.LDPC_LLR import LDPC_LLR

import numpy as np
import matplotlib.pyplot as plt


### PARAMETERS ###
# LDPC #
dv = 3      # rate = 4/7 #
dc = 7
N = 994     #98, 994, 1001
decode_max_iter = 50
# plot #
samples = 5
snr_values_dB = np.arange(0, 5.5, 0.5)


### CHANNEL ###
channel = AWGNChannel()

### LDPC ###
graph = LDPC_LLR(dv, dc, N)
# OUTPUT - .CSV #
graph.export_to_csv('ldpc_graph.csv')
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print("ldpc_graph.csv [OK]\n")

### PLOT ### 
snr_values = 10 ** (snr_values_dB/10)               
pb_values = np.zeros(len(snr_values))
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

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"Point no. {k+1} / {len(snr_values)}\n")

### OUTPUT - POINTS.TXT ###
with open("output/points.txt", "w") as file:
    for k in range(len(snr_values_dB)):
        file.write("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
        file.write(f"Point no. {k+1}\n")
        file.write(f"snr: {snr_values_dB[k]} dB\n")
        file.write(f"pb: {pb_values[k]}\n")
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print("points.txt [OK]\n")

### OUTPUT - PLOT.PNG ###
plt.figure()
plt.plot(snr_values_dB, pb_values)
plt.yscale('log')
plt.xlabel('snr (dB)')
plt.ylabel('Pb')
plt.title(f"AWGN channel / LDPC code, using LLR, rate = 4/7, N = {N}")
plt.grid(True)
plt.savefig("output/plot.png", format="png")
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print("plot.png [OK]\n")
plt.show()