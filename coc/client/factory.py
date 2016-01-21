from twisted.internet.protocol import ClientFactory
from coc.client.protocol import CoCClientProtocol


class CoCClientFactory(ClientFactory):

    def __init__(self, server):
        self.server = server

    def buildProtocol(self, addr):
        return CoCClientProtocol(self)
