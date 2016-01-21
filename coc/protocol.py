from twisted.internet import protocol


class CoCPacketReceiver(protocol.Protocol):

    _buffer = b""
    _packet = b""

    def dataReceived(self, data):
        self._buffer += data
        while self._buffer:
            if self._packet:
                payload_length = int.from_bytes(self._packet[2:5], byteorder="big")
                if len(self._buffer) >= payload_length:
                    self._packet += self._buffer[:payload_length]
                    self.packetReceived(self._packet)
                    self._packet = b""
                    self._buffer = self._buffer[payload_length:]
                else:
                    break
            elif len(self._buffer) >= 7:
                self._packet = self._buffer[:7]
                self._buffer = self._buffer[7:]

    def packetReceived(self, packet):
        raise NotImplementedError


class CoCProtocol(CoCPacketReceiver):

    _peer = None

    session_key = None

    def __init__(self, factory):
        self._factory = factory
        self.factory.server = None
        self.factory.client = None

    @property
    def factory(self):
        return self._factory

    @property
    def peer(self):
        return self._peer

    def connectionMade(self):
        self._peer = self.transport.getPeer()

    def packetReceived(self, packet):
        decrypted = self.decryptPacket(packet)
        if decrypted:
            self.packetDecrypted(*decrypted)

    def decryptPacket(self, packet):
        raise NotImplementedError

    def packetDecrypted(self, messageid, unknown, payload):
        raise NotImplementedError

    def sendPacket(self, messageid, unknown, payload):
        (messageid, unknown, payload) = self.encryptPacket(messageid, unknown, payload)
        packet = (messageid.to_bytes(2, byteorder="big") + len(payload).to_bytes(3, byteorder="big") + unknown.to_bytes(2, byteorder="big") + payload)
        self.transport.write(packet)

    def encryptPacket(self, messageid, unknown, payload):
        raise NotImplementedError
