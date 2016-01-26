from twisted.internet import reactor
from coc.protocol import CoCProtocol
from coc.server.crypto import CoCServerCrypto
from coc.client.factory import CoCClientFactory


class CoCServerProtocol(CoCServerCrypto, CoCProtocol):

    client = None

    def __init__(self, factory):
        super(CoCServerProtocol, self).__init__(factory)
        self.factory.server = self
        self.decoder = self.factory.decoder

    def connectionMade(self):
        super(CoCServerProtocol, self).connectionMade()
        print("connection from {}:{} ...".format(self.peer.host, self.peer.port))
        self.factory.client_endpoint.connect(CoCClientFactory(self))

    def packetDecrypted(self, messageid, unknown, payload):
        if not self.client:
            reactor.callLater(0.25, self.packetDecrypted, messageid, unknown, payload)
            return
        self.decodePacket(messageid, unknown, payload)
        self.client.sendPacket(messageid, unknown, payload)

    def connectionLost(self, reason):
        print("connection from {}:{} closed ...".format(self.peer.host, self.peer.port))
        if self.client:
            self.client.transport.loseConnection()
