import numpy as np

from modules.System import Encoder

class HammingEncoder(Encoder):
    """
    Receives an information, encodes it, transmits it through a channel and decodes it in an attempt to retrieve the original information.

    It also uses a generator matrix G and a parity-check matrix H to encode and decode the information.

    Typical usage example:

    encoder = Encoder()
    encoded_data = encoder.encode(raw_data)
    transmitted_data = channel.transmit(encoded_data)
    encoded_data_hat = encoder.decode(transmitted_data)
    raw_data = encoded_data_hat[:4]
    """

    def __init__(self):
        """
        Initializes the Encoder with generator matrix G based on Hamming(7, 4) code
        """
        self.G = np.array([
            [1, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 1]
        ])

    def encode(self, u, *args, **kwargs):
        """
        Encodes an input message using the generator matrix.

        Params:
            u (list): List of bits to be encoded.

        Returns:
            v (list): Encoded list of bits.
        """
        v = np.dot(u, self.G) % 2
        return v
