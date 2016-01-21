from twisted.internet.protocol import Factory
from coc.server.protocol import CoCServerProtocol


class CoCServerFactory(Factory):

    def __init__(self, client_endpoint):
        self.client_endpoint = client_endpoint

    def buildProtocol(self, endpoint):
        return CoCServerProtocol(self)
