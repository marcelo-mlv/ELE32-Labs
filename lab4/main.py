from output import out_plot, out_txt
from modules.run_simulation import run_bpsk, run_ldpc_bp, run_ldpc_bf, run_hamming
from params import rate, decode_max_iter, num_samples, snr_values, \
awgnc, bsc, ldpc_bp, ldpc_bf, hamming, s_bits, s_symbols

### Simulation ###
pb_bpsk = run_bpsk(snr_values)
pb_ldpc_bp = run_ldpc_bp(s_symbols, awgnc, ldpc_bp, snr_values, decode_max_iter, rate, num_samples)
pb_ldpc_bf = run_ldpc_bf(s_bits, bsc, ldpc_bf, snr_values, decode_max_iter, num_samples)
pb_hamming = run_hamming(s_bits, bsc, hamming, snr_values, num_samples)

### Output ###
out_txt(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp)
out_plot(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, show=True)
