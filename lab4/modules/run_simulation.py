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

def find_operational_ebn0(snr_values, pb_vector, pb_target=1e-4):
    """
    Retorna o menor Eb/N0 (em dB) para o qual Pb <= pb_target.
    Se não encontrar, retorna None.
    """
    for snr_db, pb in zip(snr_values, pb_vector):
        if pb <= pb_target:
            return snr_db
    return None

def theoretical_ebn0_min(rate):
    """
    Calcula o limite teórico inferior de Eb/N0 (em dB) para um dado rate.
    Para rate -> 0, retorna -1.59 dB (limite de Shannon para canal AWGN).
    Para rate > 0, calcula Eb/N0 mínimo teórico para o código.
    """
    import numpy as np
    if rate <= 0:
        return None
    # Shannon: R < 0.5*log2(1 + 2*R*Eb/N0)
    # Para o limite, R = 0.5*log2(1 + 2*R*Eb/N0)
    # Inverter para Eb/N0:
    # 2^ (2R) = 1 + 2*R*Eb/N0
    # 2*R*Eb/N0 = 2^(2R) - 1
    # Eb/N0 = (2^(2R) - 1) / (2*R)
    ebn0_linear = (2**(2*rate) - 1) / (2*rate)
    ebn0_db = 10 * np.log10(ebn0_linear)
    return ebn0_db

def shannon_limit_db():
    """
    Limite teórico inferior universal para canal AWGN: Eb/N0 > 1/(2*log2(e)) ≈ -1.59 dB
    """
    import numpy as np
    return 10 * np.log10(1/(2*np.log2(np.e)))
