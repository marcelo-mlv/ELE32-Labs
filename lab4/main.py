from output import out_plot, out_txt
from modules.run_simulation import run_bpsk, run_ldpc_bp, run_ldpc_bf, run_hamming, find_operational_ebn0, theoretical_ebn0_min
from params import rate, decode_max_iter, num_samples, Et_N0_values_sem_cod, Et_N0_values, \
awgnc, bsc, ldpc_bp, ldpc_bp_2, ldpc_bf, hamming, s_bits, s_symbols, Q

import math
import numpy as np

pb_sem_cod = []
pb_ldpc_bp = []
pb_ldpc_bp_2 = []
pb_ldpc_bf = []
pb_hamming = []

### Simulation ###
for idx, Et_N0_db in enumerate(Et_N0_values):
    Et_N0 = 10 ** (Et_N0_db / 10)
    p_bsc = Q(math.sqrt(2*Et_N0))
    N0 = 1/Et_N0

    bp_flipped_symbols = 0
    bp_2_flipped_symbols = 0
    bf_flipped_symbols = 0
    hm_flipped_symbols = 0

    for _ in range(num_samples):
        bp_flipped_symbols += np.sum(run_ldpc_bp(s_symbols, awgnc, ldpc_bp, N0, decode_max_iter) == -1)
        bp_2_flipped_symbols += np.sum(run_ldpc_bp(s_symbols[:-1], awgnc, ldpc_bp_2, N0, decode_max_iter) == -1)
        bf_flipped_symbols += np.sum(run_ldpc_bf(s_bits, bsc, ldpc_bf, p_bsc, decode_max_iter) == 1)
        hm_flipped_symbols += np.sum(run_hamming(s_bits, bsc, hamming, p_bsc) == 1)

    pb_ldpc_bp.append(bp_flipped_symbols / (num_samples * len(s_symbols)))
    pb_ldpc_bp_2.append(bp_flipped_symbols / (num_samples * (len(s_symbols) - 1)))
    pb_ldpc_bf.append(bf_flipped_symbols / (num_samples * len(s_bits)))
    pb_hamming.append(hm_flipped_symbols / (num_samples * len(s_bits)))

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"Simulation completed for SNR = {[snr for snr in Et_N0_values[0:idx+1]]}\n")
    print(f"SNR values left: {[snr for snr in Et_N0_values[idx+1:]]}\n")
    print(f"Simulation {int(100*(idx+1)/len(Et_N0_values))}% complete\n")

### SEM CODIFICAÇÃO ###
pb_sem_cod = np.zeros(len(Et_N0_values_sem_cod))
for k in range(len(Et_N0_values_sem_cod)):
    Et_N0 = 10 ** (Et_N0_values_sem_cod[k]/10)
    pb_sem_cod[k] = Q(np.sqrt(2*Et_N0))

### Output ###
out_txt(Et_N0_values, pb_sem_cod, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, pb_ldpc_bp_2)
out_plot(Et_N0_values, pb_sem_cod, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, pb_ldpc_bp_2 , show=True)

# Operatoinal Eb/N0
op_sem_cod = find_operational_ebn0(Et_N0_values + 3, pb_sem_cod)
op_ldpc_bp = find_operational_ebn0(Et_N0_values - 10*np.log10(4/7), pb_ldpc_bp)
op_ldpc_bp_2 = find_operational_ebn0(Et_N0_values - 10*np.log10(1/2), pb_ldpc_bp_2) 
op_ldpc_bf = find_operational_ebn0(Et_N0_values - 10*np.log10(4/7), pb_ldpc_bf) 
op_hamming = find_operational_ebn0(Et_N0_values - 10*np.log10(4/7), pb_hamming) 

print("\n=========== Operational Eb/N0 for Pb <= 1e-4 (dB) ===========")
print(f"BPSK theoretical:  {op_sem_cod if op_sem_cod is not None else 'Not reached target'} dB")
print(f"LDPC-BP (LLR):     {op_ldpc_bp if op_ldpc_bp is not None else 'Not reached target'} dB")
print(f"LDPC-BP-2 (LLR):   {op_ldpc_bp_2 if op_ldpc_bp_2 is not None else 'Not reached target'} dB")
print(f"LDPC-BF:           {op_ldpc_bf if op_ldpc_bf is not None else 'Not reached target'} dB")
print(f"Hamming:           {op_hamming if op_hamming is not None else 'Not reached target'} dB")
print("============================================================\n")

# Theoretical minimum Eb/N0
minimum_ebn0 = theoretical_ebn0_min(rate)

print("\n====================== Min Eb/N0 (dB) ======================")
print(f"Theoretical minimum Eb/N0:  {minimum_ebn0 if minimum_ebn0 is not None else 'Not reached target'} dB")
print("(It's the same for all cases)")
print("============================================================\n")

# Gap Between operational and theoretical min Eb/N0

print("\n==== Gap Between operational and theoretical min Eb/N0 =====")
print(f"BPSK theoretical:  {op_sem_cod - minimum_ebn0 if op_sem_cod or minimum_ebn0 is not None else 'Not reached target'} dB")
print(f"LDPC-BP (LLR):     {op_ldpc_bp - minimum_ebn0 if op_ldpc_bp or minimum_ebn0 is not None else 'Not reached target'} dB")
print(f"LDPC-BP-2 (LLR):     {op_ldpc_bp_2 - minimum_ebn0 if op_ldpc_bp_2 or minimum_ebn0 is not None else 'Not reached target'} dB")
print(f"LDPC-BF:           {op_ldpc_bf - minimum_ebn0 if op_ldpc_bf or minimum_ebn0 is not None else 'Not reached target'} dB")
print(f"Hamming:           {op_hamming - minimum_ebn0 if op_hamming or minimum_ebn0 is not None else 'Not reached target'} dB")
print("============================================================\n")
