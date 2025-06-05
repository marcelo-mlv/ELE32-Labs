import numpy as np
import math

Q = lambda x: 0.5 * (1 - math.erf(x / np.sqrt(2)))

def run_bpsk(snr_values):
    pb_bpsk = np.zeros(len(snr_values))
    for k, snr_db in enumerate(snr_values):
        snr = 10 ** (snr_db/10)
        pb_bpsk[k] = Q(np.sqrt(3*snr))
    return pb_bpsk

def run_ldpc_bp(s_symbols, channel, ldpc_bp, snr_values, decode_max_iter, rate, num_samples):
    N = len(s_symbols)
    pb_ldpc_bp = np.zeros(len(snr_values))
    for k, snr_db in enumerate(snr_values):
        snr = 10 ** (snr_db/10)
        Eb = 1 / rate
        Nzero = Eb / snr
        num_errors = 0
        for _ in range(num_samples):
            r_symbols = channel.transmit(s_symbols, Nzero)
            bp_decoded_symbols = ldpc_bp.decode(r_symbols, Nzero, decode_max_iter)
            num_errors += np.sum(bp_decoded_symbols == -1)
        pb_ldpc_bp[k] = num_errors / (N * num_samples)
    return pb_ldpc_bp

def run_ldpc_bf(s_bits, channel, ldpc_bf, snr_values, decode_max_iter, num_samples):
    N = len(s_bits)
    pb_ldpc_bf = np.zeros(len(snr_values))
    for k, snr_db in enumerate(snr_values):
        snr = 10 ** (snr_db/10)
        p = Q(np.sqrt(3*snr))
        num_errors = 0
        for _ in range(num_samples):
            r_bits = channel.transmit(s_bits, p)
            bf_decoded_bits = ldpc_bf.decode(r_bits, decode_max_iter)
            num_errors += np.sum(bf_decoded_bits == 1)
        pb_ldpc_bf[k] = num_errors / (N * num_samples)
    return pb_ldpc_bf

def run_hamming(s_bits, channel, hamming, snr_values, num_samples):
    N = len(s_bits)
    pb_hamming = np.zeros(len(snr_values))
    for k, snr_db in enumerate(snr_values):
        snr = 10 ** (snr_db/10)
        p = Q(np.sqrt(3*snr))
        num_errors = 0
        for _ in range(num_samples):
            r_bits = channel.transmit(s_bits, p)
            for i in range(0, len(r_bits), 7):
                chunk = r_bits[i:i+7]
                chunk_decoded_bits = hamming.decode(chunk)
                num_errors += np.sum(chunk_decoded_bits == 1)
        pb_hamming[k] = num_errors / (N * num_samples)
    return pb_hamming
