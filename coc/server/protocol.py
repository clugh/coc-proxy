from twisted.internet import reactor
from coc.protocol import CoCProtocol
from coc.server.crypt import CoCServerCrypt
from coc.client.factory import CoCClientFactory


class CoCServerProtocol(CoCServerCrypt, CoCProtocol):

    def __init__(self, factory):
        super(CoCServerProtocol, self).__init__(factory)
        self.factory.server = self

    def connectionMade(self):
        super(CoCServerProtocol, self).connectionMade()
        print("connection from {}:{} ...".format(self.peer.host, self.peer.port))
        self.factory.client_endpoint.connect(CoCClientFactory(self))

    def packetDecrypted(self, messageid, unknown, payload):
        if not self.client:
            reactor.callLater(0.25, self.packetDecrypted, messageid, unknown, payload)
            return
        print(messageid, (messageid.to_bytes(2, byteorder="big") + len(payload).to_bytes(3, byteorder="big") + unknown.to_bytes(2, byteorder="big") + payload).hex())
        self.client.sendPacket(messageid, unknown, payload)

    def connectionLost(self, reason):
        print("connection from {}:{} closed ...".format(self.peer.host, self.peer.port))
        if self.client:
            self.client.transport.loseConnection()
