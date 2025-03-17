class Channel:
    def transmit(self, data):
        pass

class Encoder:
    def encode(self, data):
        pass

class Decoder:
    def decode(self, data):
        pass

class BinarySymmetricChannel(Channel):
    def transmit(self, data, p):
        pass

class System:
    def __init__(self, encoder, decoder, channel):
        self.encoder = encoder
        self.decoder = decoder
        self.channel = channel

    def process(self, data):
        encoded_data = self.encoder.encode(data)
        transmitted_data = self.channel.transmit(encoded_data)
        decoded_data = self.decoder.decode(transmitted_data)
        return decoded_data
