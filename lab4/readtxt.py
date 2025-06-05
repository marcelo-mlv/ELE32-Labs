import matplotlib.pyplot as plt

import re
import numpy as np

# Caminho do arquivo
points_path = './output/points.txt'

# Inicializa listas para armazenar os valores
snr_values = []
pb_ldpc_bp = []
pb_bpsk = []
pb_ldpc_bf = []
pb_hamming = []

with open(points_path, 'r') as f:
    for line in f:
        if line.startswith('snr:'):
            snr_values.append(float(line.split(':')[1].strip()))
        elif 'pb' in line:
            # Extrai o valor numérico da linha
            value = float(re.findall(r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", line)[-1])
            if 'BPSK' in line:
                pb_bpsk.append(value)
            elif 'LDPC-BF' in line:
                pb_ldpc_bf.append(value)
            elif 'Hamming' in line:
                pb_hamming.append(value)
            elif 'LDPC-BP' in line:
                pb_ldpc_bp.append(value)

# Converte para numpy arrays
snr_values = np.array(snr_values)
pb_ldpc_bp = np.array(pb_ldpc_bp)
pb_bpsk = np.array(pb_bpsk)
pb_ldpc_bf = np.array(pb_ldpc_bf)
pb_hamming = np.array(pb_hamming)

print('snr_values:', snr_values)
print('pb_bpsk:', pb_bpsk)
print('pb_ldpc_bf:', pb_ldpc_bf)
print('pb_hamming:', pb_hamming)
print('pb_ldpc_bp:', pb_ldpc_bp)
