class Channel:
    def transmit(self, *args, **kwargs):
        pass

class Encoder:
    def encode(self, *args, **kwargs):
        pass

class Decoder:
    def decode(self, *args, **kwargs):
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
