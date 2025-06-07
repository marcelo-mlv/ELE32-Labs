import numpy as np
import math

Q = lambda x: 0.5 * (1 - math.erf(x / np.sqrt(2)))

def run_bpsk(snr):
    return Q(math.sqrt(3*snr))

def run_ldpc_bp(s_symbols, channel, ldpc_bp, Nzero, decode_max_iter):
    r_symbols = channel.transmit(s_symbols, Nzero)
    bp_decoded_symbols = ldpc_bp.decode(r_symbols, Nzero, decode_max_iter)
    return bp_decoded_symbols

def run_ldpc_bf(s_bits, channel, ldpc_bf, p, decode_max_iter):
    r_bits = channel.transmit(s_bits, p)
    bf_decoded_bits = ldpc_bf.decode(r_bits, decode_max_iter)
    return bf_decoded_bits

def run_hamming(s_bits, channel, hamming, p):
    r_bits = channel.transmit(s_bits, p)
    hamming_decoded_bits = np.array([], dtype=int)
    for i in range(0, len(r_bits), 7):
        chunk = r_bits[i:i+7]
        chunk_decoded_bits = hamming.decode(chunk)
        hamming_decoded_bits = np.concatenate((hamming_decoded_bits, chunk_decoded_bits))
    return hamming_decoded_bits
