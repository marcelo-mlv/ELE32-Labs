import numpy as np
from Channel import BinarySymmetricChannel
from LDPCgraph import LDPCgraph
from LDPCdecoder import bit_flipping_decoder

N = 70
dv = 3
dc = 7
ldpc_graph = LDPCgraph(N, dv, dc)

input_bits = np.zeros(N, dtype=int)

channel = BinarySymmetricChannel()
channel_bits = channel.transmit(input_bits, 0.1)
print(channel_bits)

decoded_bits = bit_flipping_decoder(ldpc_graph, channel_bits, 50)
print(decoded_bits)