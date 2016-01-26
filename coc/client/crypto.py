from nacl.public import PublicKey
from coc.crypto import CoCCrypto, CoCNonce


class CoCClientCrypto(CoCCrypto):

    def __init__(self, factory):
        self._factory = factory
        self.keypair()
        self._serverkey = PublicKey(bytes.fromhex("01c98c143a840d92ee656996dad5af41de5d1b8ebb289081368b5cfda9bd4a30"))
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
        if messageid in {20100, 20103}:
            if messageid == 20100:
                self.session_key = self.server.session_key = packet[-24:]
            return messageid, unknown, payload
        elif messageid == 20104:
            nonce = CoCNonce(nonce=self.encrypt_nonce, clientkey=self.clientkey, serverkey=self.serverkey)
            ciphertext = payload
            try:
                message = self.decrypt(ciphertext, bytes(nonce))
            except ValueError:
                print("Failed to decrypt the message (client, {}).".format(messageid))
                self.server.loseConnection()
                return False
            else:
                self.decrypt_nonce = self.server.encrypt_nonce = message[:24]
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
