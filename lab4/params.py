from modules.Channel import AWGNChannel, BinarySymmetricChannel
from modules.LDPC_BP import LDPC_BP
from modules.LDPC_BF import LDPC_BF
from modules.BPSK import BPSK
from modules.Hamming import Hamming

import numpy as np

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

### Channel input ###
s_symbols = np.full(N, 1, dtype=int)
s_bits = np.full(N, 0, dtype=int)
