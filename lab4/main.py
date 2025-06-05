from modules.Channel import AWGNChannel, BinarySymmetricChannel
from modules.LDPC_BP import LDPC_BP
from modules.LDPC_BF import LDPC_BF
from modules.BPSK import BPSK
from modules.Hamming import Hamming

import math
import numpy as np
import matplotlib.pyplot as plt
from modules.run_simulation import run_bpsk, run_ldpc_bp, run_ldpc_bf, run_hamming

### PARAMETERS ###

rate = 4/7

# LDPC #
dv = 3
dc = 7
N = 1001
decode_max_iter = 20

# plot #
num_samples = 1
snr_values = np.arange(0, 5.5, 0.5)

print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"dv        = {dv}\n")
print(f"dc        = {dc}\n")
print(f"N         = {N}\n")
print(f"samples   = {num_samples}\n")

### CHANNEL ###
awgnc = AWGNChannel()
bsc = BinarySymmetricChannel()

### LDPC-BP ###
ldpc_bp = LDPC_BP.from_csv('ldpc_graph.csv', dv, dc)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-BP GRAPH BUILT\n")

## LDPC-BF ###
ldpc_bf = LDPC_BF.from_csv('ldpc_graph.csv', dv, dc)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-BF GRAPH BUILT\n")

### BPSK ###
bpsk = BPSK()

### HAMMING ###
hamming = Hamming()

s_symbols = np.full(N, 1, dtype=int)
s_bits = np.full(N, 0, dtype=int)

### Simulation ###              
pb_bpsk = run_bpsk(snr_values)
pb_ldpc_bp = run_ldpc_bp(s_symbols, awgnc, ldpc_bp, snr_values, decode_max_iter, rate, num_samples)
pb_ldpc_bf = run_ldpc_bf(s_bits, bsc, ldpc_bf, snr_values, decode_max_iter, num_samples)
pb_hamming = run_hamming(s_bits, bsc, hamming, snr_values, num_samples)

### OUTPUT - POINTS.TXT ###
with open("output/points.txt", "w") as file:
    for k in range(len(snr_values)):
        file.write(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
        file.write(f"point no. {k+1}\n")
        file.write(f"snr: {snr_values[k]}\n")
        file.write(f"pb  BPSK não codificado: {pb_bpsk[k]}\n")
        file.write(f"pb  LDPC-BF: {pb_ldpc_bf[k]}\n")
        file.write(f"pb  Hamming: {pb_hamming[k]}\n")
        file.write(f"pb  LDPC-BP: {pb_ldpc_bp[k]}\n")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"points.txt [OK]\n")

### OUTPUT - PLOT.PNG ###
plt.figure()
plt.plot(snr_values, pb_bpsk, label='BPSK não codificado', color='green')
plt.plot(snr_values, pb_ldpc_bf, label='LDPC-BF', color='orange')
plt.plot(snr_values, pb_hamming, label='Hamming', color='red')
plt.plot(snr_values, pb_ldpc_bp, label='LDPC-BP', color='blue')
plt.yscale('log')
plt.xlabel('snr (dB)')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x relação sinal-ruído")
plt.grid(True, which='both', linestyle='--')
plt.legend(title="Curvas", loc="upper right")
plt.savefig("output/plot.png", format="png")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"plot.png [OK]\n")
plt.show()