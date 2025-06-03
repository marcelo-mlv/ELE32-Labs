from modules.Channel import AWGNChannel
from modules.LDPC_LLR import LDPC_LLR

import numpy as np
import matplotlib.pyplot as plt

### PARAMETERS ###
# LDPC #
dv = 3      # rate = 4/7 #
dc = 7
N = 1001   #98, 994, 1001
decode_max_iter = 20
# plot #
samples = 100
snr_values = np.arange(0, 5.5, 0.5)


### CHANNEL ###
channel = AWGNChannel()

### LDPC ###
graph = LDPC_LLR(dv, dc, N)
# OUTPUT - .CSV #
graph.export_to_csv('ldpc_graph.csv')
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"ldpc_graph.csv [OK]\n")

### PLOT ###              
pb_ldpc_llr = np.zeros(len(snr_values))
# INPUT #
s_symbols = np.full(N, 1, dtype=int)

for k in range(len(snr_values)):

    snr = 10 ** (snr_values[k]/10)
    Nzero = 1 / snr

    ### SAMPLES ###
    num_of_flipped_symbols = 0
    for _ in range(samples):
    
        r_symbols = channel.transmit(s_symbols, Nzero)

        decoded_symbols = graph.decode(r_symbols, Nzero, decode_max_iter)

        for s in decoded_symbols:
            if s == -1:
                num_of_flipped_symbols += 1

    pb_ldpc_llr[k] = num_of_flipped_symbols / (N*samples)

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"point no. {k+1} / {len(snr_values)}\n")

### OUTPUT - POINTS.TXT ###
with open("output/ldpc_llr.txt", "w") as file:
    for k in range(len(snr_values)):
        file.write(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
        file.write(f"point no. {k+1}\n")
        file.write(f"snr: {snr_values[k]}\n")
        file.write(f"pb LDPC-LLR: {pb_ldpc_llr[k]}\n")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"points.txt [OK]\n")

### OUTPUT - POINTS.TXT ###
plt.figure()
plt.plot(snr_values, pb_ldpc_llr)
plt.yscale('log')
plt.xlabel('snr (dB)')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x relação sinal-ruído")
plt.grid(True)
# plt.legend()
plt.savefig("output/plot.png", format="png")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"plot.png [OK]\n")
plt.show()