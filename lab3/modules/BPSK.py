import numpy as np

class BPSK:
    """
    Class for BPSK modulation and demodulation.
    """
    def decode(self, received_symbols):
        """
        Estima os símbolos BPSK originais (-1 ou 1) a partir dos símbolos recebidos após transmissão pelo canal AWGN.
        Args:
            received_symbols (np.ndarray): Sinais recebidos do canal (valores reais).
        Returns:
            np.ndarray: Símbolos estimados (-1 ou 1).
        """
        return np.where(received_symbols >= 0, 1, -1)
