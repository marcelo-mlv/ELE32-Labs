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
# plot #
samples = 100
snr_values = np.arange(0, 5.5, 0.5)

### CHANNEL ###
awgnc = AWGNChannel()
bsc = BinarySymmetricChannel()

### LDPC ###
ldpc_llr = LDPC_LLR.from_csv('ldpc_graph.csv', dv, dc)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-LLR GRAPH BUILT\n")

### BPSK ###
bpsk = BPSK()

### HAMMING ###
hamming = Hamming()

### PLOT ###              
pb_ldpc_llr = np.zeros(len(snr_values))
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
    
        r_symbols = awgnc.transmit(s_symbols, Nzero)
        r_bits = bsc.transmit(s_bits, bsc_p)

        llr_decoded_symbols = ldpc_llr.decode(r_symbols, Nzero, decode_max_iter)
        bpsk_decoded_symbols = bpsk.decode(r_symbols)

        # decoded_symbols = ldpc_bf.decode(r_bits, bf_max_iter) -- BSC -- qual a relação de p (do BSC) com Eb/N0 (snr)
        # decoded_symbols = hamming.decode(r_bits, ...) -- BSC

        for s in llr_decoded_symbols:
            if s == -1:
                llr_num_of_flipped_symbols += 1

        for s in bpsk_decoded_symbols:
            if s == -1:
                bpsk_num_of_flipped_symbols += 1
        
        
    pb_ldpc_llr[k] = llr_num_of_flipped_symbols / (N*samples)
    pb_bpsk[k] = bpsk_num_of_flipped_symbols / (N*samples)
    # add
    # add
    # add
        

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"point no. {k+1} / {len(snr_values)}\n")

### OUTPUT - POINTS.TXT ###
with open("output/points.txt", "w") as file:
    for k in range(len(snr_values)):
        file.write(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
        file.write(f"point no. {k+1}\n")
        file.write(f"snr: {snr_values[k]}\n")
        file.write(f"pb LDPC-LLR: {pb_ldpc_llr[k]}\n")
        file.write(f"pb LDPC-BF: {pb_ldpc_bf[k]}\n")
        # add
        # add
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"points.txt [OK]\n")

### OUTPUT - POINTS.TXT ###
plt.figure()
plt.plot(snr_values, pb_ldpc_llr)
# plt.plot(snr_values, pb_ldpc_bf)
# add
# add
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