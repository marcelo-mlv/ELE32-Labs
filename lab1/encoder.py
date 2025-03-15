import numpy as np

class Encoder:
    """Receives an information, encodes it, transmits it through a channel and decodes it in an attempt to retrieve the original information.

    It also uses a generator matrix G and a parity-check matrix H to encode and decode the information.

    Typical usage example:

    encoder = Encoder()
    encoded_data = encoder.encode(raw_data)
    transmitted_data = channel.transmit(encoded_data)
    encoded_data_hat = encoder.decode(transmitted_data)
    raw_data = encoded_data_hat[:4]
    """

    def __init__(self):
        self.G = np.array([
            [1, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 1]
        ])
        self.H = np.array([
            [1, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1]
        ])

    def encode(self, u):
        v = np.dot(u, self.G) % 2
        return v
    
    def getSyndrome(self, r):
        return np.dot(r, self.H.T) % 2

    def getError(self, r):
        s = self.getSyndrome(r)
        e = np.zeros(7)
        if np.all(s == 0):
            return e
        for i in range(0, len(self.H.T)):
            if np.all(s == self.H.T[i]):
                e[i] = 1 - e[i]
                return e

    def decode(self, r):
        e = self.getError(r)
        return r + e % 2
