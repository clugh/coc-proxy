from coc.protocol import CoCProtocol
from coc.client.crypt import CoCClientCrypt


class CoCClientProtocol(CoCClientCrypt, CoCProtocol):

    def __init__(self, factory):
        super(CoCClientProtocol, self).__init__(factory)
        self.factory.server.client = self
        self.server = self.factory.server

    def connectionMade(self):
        super(CoCClientProtocol, self).connectionMade()
        print("connected to {}:{} ...".format(self.peer.host, self.peer.port))

    def packetDecrypted(self, messageid, unknown, payload):
        print(messageid, (messageid.to_bytes(2, byteorder="big") + len(payload).to_bytes(3, byteorder="big") + unknown.to_bytes(2, byteorder="big") + payload).hex())
        self.server.sendPacket(messageid, unknown, payload)

    def connectionLost(self, reason):
        print("connection to {}:{} closed ...".format(self.peer.host, self.peer.port))
        self.server.transport.loseConnection()
