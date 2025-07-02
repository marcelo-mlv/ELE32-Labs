from modules.Channel import AWGNChannel, BinarySymmetricChannel
from modules.LDPC_BP import LDPC_BP
from modules.LDPC_BF import LDPC_BF
from modules.BPSK import BPSK
from modules.Hamming import Hamming

import numpy as np
import math

### CONSTANTS ###
Q = lambda x: 0.5 * np.exp(- (x ** 2) / 2)

### PARAMETERS ###
rate = 4/7

# LDPC #
N = 1001
N_2 = 1000
decode_max_iter = 20

# simulation #
num_samples = 10
Et_N0_values_sem_cod = np.arange(0, 10.5, 0.5)
Et_N0_values = Et_N0_values_sem_cod - 3

### CHANNEL ###
awgnc = AWGNChannel()
bsc = BinarySymmetricChannel()

### LDPC-BP ###
ldpc_bp = LDPC_BP.from_csv('graph_3_7.csv', dv=3, dc=7)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-BP GRAPH BUILT\n")

ldpc_bp_2 = LDPC_BP.from_csv('graph_4_8.csv', dv=4, dc=8)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-BP-2 GRAPH BUILT\n")

## LDPC-BF ###
ldpc_bf = LDPC_BF.from_csv('ldpc_graph.csv', dv=3, dc=7)
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"LDPC-BF GRAPH BUILT\n")

### BPSK ###
bpsk = BPSK()

### HAMMING ###
hamming = Hamming()

### Channel input ###
s_symbols = np.full(N, 1, dtype=int)
s_bits = np.full(N, 0, dtype=int)
