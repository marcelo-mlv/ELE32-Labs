from modules.Channel import AWGNChannel, BinarySymmetricChannel
from modules.LDPC_LLR import LDPC_LLR
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
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"dv        = {dv}\n")
print(f"dc        = {dc}\n")
print(f"N         = {N}\n")
print(f"samples   = {N}\n")

# plot #
samples = 1000
snr_values = np.arange(0, 5.5, 0.5)

### CHANNEL ###
awgnc = AWGNChannel()
bsc = BinarySymmetricChannel()

### LDPC-BP ###
ldpc_bp = LDPC_LLR.from_csv('ldpc_graph.csv', dv, dc)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-LLR GRAPH BUILT\n")

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
    num_of_flipped_symbols = 0
    for _ in range(samples):
    
        ### TRANSMISSION ###
        r_symbols = awgnc.transmit(s_symbols, Nzero)
        r_bits = bsc.transmit(s_bits, bsc_p)

        ### LDPC-BP ###
        bp_decoded_symbols  = ldpc_llr.decode(r_symbols, Nzero, decode_max_iter)

        bp_num_of_flipped_symbols = 0
        for s in bp_decoded_symbols:
            if s == -1:
                bp_num_of_flipped_symbols += 1

        ### BPSK ###
        bpsk_decoded_symbols = bpsk.decode(r_symbols)

        bpsk_num_of_flipped_symbols = 0 
        for s in bpsk_decoded_symbols:
            if s == -1:
                bpsk_num_of_flipped_symbols += 1

        ### LDPC-BF ###
        bf_decoded_bits = ldpc_bf.decode(r_bits, decode_max_iter)

        bf_num_of_flipped_bits = 0 
        for s in bf_decoded_bits:
            if s == 1:
                bf_num_of_flipped_bits += 1

        ### Hamming ###
        hamming_num_of_flipped_bits = 0
        for i in range(0, len(r_bits), 7):
            chunk = r_bits[i:i+7]
            chunk_decoded_bits = hamming.decode(chunk)
            for bit in chunk_decoded_bits:
                if bit == 1:
                    hamming_num_of_flipped_bits += 1
        
        
    pb_ldpc_bp[k] = bp_num_of_flipped_symbols / (N*samples)
    pb_bpsk[k] = bpsk_num_of_flipped_symbols / (N*samples)
    pb_ldpc_bf[k] = bf_num_of_flipped_bits / (N*samples)
    pb_hamming[k] = hamming_num_of_flipped_bits / (N*samples)        

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"point no. {k+1} / {len(snr_values)}\n")

### OUTPUT - POINTS.TXT ###
with open("output/points.txt", "w") as file:
    for k in range(len(snr_values)):
        file.write(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
        file.write(f"point no. {k+1}\n")
        file.write(f"snr: {snr_values[k]}\n")
        file.write(f"pb  LDPC-BP: {pb_ldpc_bp[k]}\n")
        file.write(f"pb     BPSK: {pb_bpsk[k]}\n")
        file.write(f"pb  LDPC-BF: {pb_ldpc_bf[k]}\n")
        file.write(f"pb  Hamming: {pb_hamming[k]}\n")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"points.txt [OK]\n")

### OUTPUT - POINTS.TXT ###
plt.figure()
plt.plot(snr_values, pb_ldpc_bp, label='LDPC-BP', color='blue')
plt.plot(snr_values, pb_ldpc_bf, label='LDPC-BF', color='orange')
plt.plot(snr_values, pb_bpsk, label='BPSK', color='green')
plt.plot(snr_values, pb_hamming, label='Hamming', color='red')
plt.yscale('log')
plt.xlabel('snr (dB)')
plt.ylabel('Pb')
plt.title("Prob. inversão de bit pós decodificação x relação sinal-ruído")
plt.grid(True)
plt.legend(title="Curvas", loc="upper right")
plt.savefig("output/plot.png", format="png")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"plot.png [OK]\n")
plt.show()