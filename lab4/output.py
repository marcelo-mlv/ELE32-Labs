import matplotlib.pyplot as plt
import numpy as np

def out_txt(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, pb_ldpc_bp_2):
    with open("output/points.txt", "w") as file:
        for k in range(len(snr_values)):
            file.write(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
            file.write(f"point no. {k+1}\n")
            file.write(f"snr: {snr_values[k]}\n")
            file.write(f"pb  BPSK não codificado: {pb_bpsk[k]}\n")
            file.write(f"pb  LDPC-BF: {pb_ldpc_bf[k]}\n")
            file.write(f"pb  Hamming: {pb_hamming[k]}\n")
            file.write(f"pb  LDPC-BP: {pb_ldpc_bp[k]}\n")
            file.write(f"pb  LDPC-BP-2: {pb_ldpc_bp_2[k]}\n")
    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"points.txt [OK]\n")

def out_plot(Et_N0_values, pb_sem_cod, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, pb_ldpc_bp_2, show):
    plt.figure()
    plt.plot(Et_N0_values + 3, pb_sem_cod, label='BPSK não codificado', color='green')
    plt.plot(Et_N0_values - 10*np.log10(4/7), pb_hamming, label='Hamming (4/7)', color='red')
    plt.plot(Et_N0_values - 10*np.log10(4/7), pb_ldpc_bf, label='LDPC-BF (4/7)', color='orange')
    plt.plot(Et_N0_values - 10*np.log10(4/7), pb_ldpc_bp, label='LDPC-BP (4/7)', color='blue')
    plt.plot(Et_N0_values - 10*np.log10(1/2), pb_ldpc_bp_2, label='LDPC-BP (1/2)')
    plt.yscale('log')
    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('Pb')
    plt.title("Probabilidade de Erro de Bit de Informação x Eb/N0")
    plt.grid(True, which='both', linestyle='--')
    plt.legend(title="Curvas", loc="upper right")
    plt.savefig("output/plot.png", format="png")
    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"plot.png [OK]\n")
    
    if show:
        plt.show()
    else:
        plt.close()
