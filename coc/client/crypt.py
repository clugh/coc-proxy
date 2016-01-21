from nacl.public import PublicKey
from coc.crypt import CoCCrypt, CoCNonce


class CoCClientCrypt(CoCCrypt):

    factory = None
    server = None

    def __init__(self, factory):
        self._factory = factory
        self.keypair()
        self._serverkey = PublicKey(bytes.fromhex("47d1416f3cf982d2b510cab32ecc4f1a04971345446cb1af326f304f63da6264"))
        self.beforenm(self.serverkey)

    @property
    def serverkey(self):
        return bytes(self._serverkey)

    @property
    def clientkey(self):
        return bytes(self._pk)

    def decryptPacket(self, packet):
        messageid = int.from_bytes(packet[:2], byteorder="big")
        unknown = int.from_bytes(packet[5:7], byteorder="big")
        payload = packet[7:]
        if messageid == 20100:
            self.session_key = packet[-24:]
            self.server.session_key = self.session_key
            return messageid, unknown, payload
        elif messageid == 20104:
            nonce = CoCNonce(nonce=self.encrypt_nonce, clientkey=self.clientkey, serverkey=self.serverkey)
            ciphertext = payload
            try:
                message = self.decrypt(ciphertext, bytes(nonce))
            except ValueError:
                print("Failed to decrypt the message (client, {}).".format(messageid))
                self.factory.server.loseConnection()
                return False
            else:
                self.decrypt_nonce = message[:24]
                self.server.encrypt_nonce = self.decrypt_nonce
                self.k = message[24:56]
                return messageid, unknown, message[56:]
        else:
            ciphertext = payload
            message = self.decrypt(ciphertext)
            return messageid, unknown, message

    def encryptPacket(self, messageid, unknown, payload):
        if messageid == 10100:
            return messageid, unknown, payload
        elif messageid == 10101:
            nonce = CoCNonce(clientkey=self.clientkey, serverkey=self.serverkey)
            message = self.session_key + self.encrypt_nonce + payload
            ciphertext = self.encrypt(message, nonce)
            return messageid, unknown, self.clientkey + ciphertext
        else:
            message = payload
            return messageid, unknown, self.encrypt(message)
