from output import out_plot, out_txt
from modules.run_simulation import run_bpsk, run_ldpc_bp, run_ldpc_bf, run_hamming
from params import rate, decode_max_iter, num_samples, snr_values, \
awgnc, bsc, ldpc_bp, ldpc_bf, hamming, s_bits, s_symbols, Q

import math
import numpy as np

pb_bpsk = []
pb_ldpc_bp = []
pb_ldpc_bf = []
pb_hamming = []

### Simulation ###
for idx, snr_db in enumerate(snr_values):
    snr = 10 ** (snr_db / 10)
    p_bsc = Q(math.sqrt(3*snr))
    N0 = 1/(rate*snr)

    bp_flipped_symbols = 0
    bf_flipped_symbols = 0
    hm_flipped_symbols = 0

    for _ in range(num_samples):
        bp_flipped_symbols += np.sum(run_ldpc_bp(s_symbols, awgnc, ldpc_bp, N0, decode_max_iter) == -1)
        bf_flipped_symbols += np.sum(run_ldpc_bf(s_bits, bsc, ldpc_bf, p_bsc, decode_max_iter) == 1)
        hm_flipped_symbols += np.sum(run_hamming(s_bits, bsc, hamming, p_bsc) == 1)

    pb_bpsk.append(run_bpsk(snr))
    pb_ldpc_bp.append(bp_flipped_symbols / (num_samples * len(s_symbols)))
    pb_ldpc_bf.append(bf_flipped_symbols / (num_samples * len(s_bits)))
    pb_hamming.append(hm_flipped_symbols / (num_samples * len(s_bits)))

    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"Simulation completed for SNR = {[snr for snr in snr_values[0:idx+1]]}\n")
    print(f"SNR values left: {[snr for snr in snr_values[idx+1:]]}\n")
    print(f"Simulation {int(100*(idx+1)/len(snr_values))}% complete\n")

### Output ###
out_txt(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp)
out_plot(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, show=True)
