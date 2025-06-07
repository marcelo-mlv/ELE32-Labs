import matplotlib.pyplot as plt

def out_txt(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp):
    with open("output/points.txt", "w") as file:
        for k in range(len(snr_values)):
            file.write(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
            file.write(f"point no. {k+1}\n")
            file.write(f"snr: {snr_values[k]}\n")
            file.write(f"pb  BPSK não codificado: {pb_bpsk[k]}\n")
            file.write(f"pb  LDPC-BF: {pb_ldpc_bf[k]}\n")
            file.write(f"pb  Hamming: {pb_hamming[k]}\n")
            file.write(f"pb  LDPC-BP: {pb_ldpc_bp[k]}\n")
    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"points.txt [OK]\n")

def out_plot(snr_values, pb_bpsk, pb_ldpc_bf, pb_hamming, pb_ldpc_bp, show):
    plt.figure()
    plt.plot(snr_values, pb_bpsk, label='BPSK não codificado', color='green')
    plt.plot(snr_values, pb_ldpc_bf, label='LDPC-BF', color='orange')
    plt.plot(snr_values, pb_hamming, label='Hamming', color='red')
    plt.plot(snr_values, pb_ldpc_bp, label='LDPC-BP', color='blue')
    plt.yscale('log')
    plt.xlabel('snr (dB)')
    plt.ylabel('Pb')
    plt.title("Prob. inversão de bit pós decodificação x relação sinal-ruído")
    plt.grid(True, which='both', linestyle='--')
    plt.legend(title="Curvas", loc="upper right")
    plt.savefig("output/plot.png", format="png")
    print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    print(f"plot.png [OK]\n")
    
    if show:
        plt.show()
    else:
        plt.close()
