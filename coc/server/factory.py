from twisted.internet.protocol import Factory
from coc.server.protocol import CoCServerProtocol


class CoCServerFactory(Factory):

    def __init__(self, client_endpoint, decoder):
        self.client_endpoint = client_endpoint
        self.decoder = decoder

    def buildProtocol(self, endpoint):
        return CoCServerProtocol(self)
