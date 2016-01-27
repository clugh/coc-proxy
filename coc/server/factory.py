from twisted.internet.protocol import Factory
from coc.server.protocol import CoCServerProtocol
from coc.message.encoder import CoCMessageEncoder
from coc.message.decoder import CoCMessageDecoder


class CoCServerFactory(Factory):

    def __init__(self, client_endpoint, definitions):
        self.client_endpoint = client_endpoint
        self.encoder = CoCMessageEncoder(definitions)
        self.decoder = CoCMessageDecoder(definitions)

    def buildProtocol(self, endpoint):
        return CoCServerProtocol(self)
