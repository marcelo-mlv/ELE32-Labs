from modules.Channel import AWGNChannel, BinarySymmetricChannel
from modules.LDPC_BP import LDPC_BP
from modules.LDPC_BF import LDPC_BF
from modules.BPSK import BPSK
from modules.Hamming import Hamming

import math
import numpy as np
import matplotlib.pyplot as plt

### PARAMETERS ###
# LDPC #
dv = 3
dc = 7
N = 1001
decode_max_iter = 20

# plot #
num_samples = 1000
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

### PLOT ###              
pb_ldpc_bp = np.zeros(len(snr_values))
pb_ldpc_bf = np.zeros(len(snr_values))
pb_bpsk = np.zeros(len(snr_values))
pb_hamming = np.zeros(len(snr_values))

# INPUT #
s_symbols = np.full(N, 1, dtype=int)
s_bits = np.full(N, 0, dtype=int)

for k in range(len(snr_values)):

    snr = 10 ** (snr_values[k]/10)
    Nzero = 1 / snr

    # Não tem função Q em numpy
    Q = lambda x: 0.5 * (1 - math.erf(x / np.sqrt(2)))

    # p = Q(np.sqrt(3*snr)) para AWGN e BPSK (prob. erro simbolo)
    # Usamos o mesmo p para o BSC para comparação justa entre os 4 métodos
    bsc_p = Q(np.sqrt(3*snr))

    ### SAMPLES ###
    num_errors = {"BPSK": 0, "Hamming": 0, "BF": 0, "BP": 0}

    for _ in range(num_samples):
    
        ### TRANSMISSION ###
        r_symbols = awgnc.transmit(s_symbols, Nzero)
        r_bits = bsc.transmit(s_bits, bsc_p)

        ### LDPC-BP ###
        bp_decoded_symbols  = ldpc_bp.decode(r_symbols, Nzero, decode_max_iter)

        for s in bp_decoded_symbols:
            if s == -1:
                num_errors['BP'] += 1

        ### BPSK ###
        bpsk_decoded_symbols = bpsk.decode(r_symbols)

        for s in bpsk_decoded_symbols:
            if s == -1:
                num_errors['BPSK'] += 1

        ### LDPC-BF ###
        bf_decoded_bits = ldpc_bf.decode(r_bits, decode_max_iter)

        for bit in bf_decoded_bits:
            if bit == 1:
                num_errors['BF'] += 1

        ### Hamming ###
        for i in range(0, len(r_bits), 7):
            chunk = r_bits[i:i+7]
            chunk_decoded_bits = hamming.decode(chunk)
            for bit in chunk_decoded_bits:
                if bit == 1:
                    num_errors['Hamming'] += 1
        
    num_total_samples = N * num_samples
    pb_ldpc_bp[k] = num_errors['BP'] / num_total_samples
    pb_bpsk[k] = num_errors['BPSK'] / num_total_samples
    pb_ldpc_bf[k] = num_errors['BF'] / num_total_samples
    pb_hamming[k] = num_errors['Hamming'] / num_total_samples        

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"point no. {k+1} / {len(snr_values)}\n")

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
plt.grid(True, witch='both', linestyle='--')
plt.legend(title="Curvas", loc="upper right")
plt.savefig("output/plot.png", format="png")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"plot.png [OK]\n")
plt.show()