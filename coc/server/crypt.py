from nacl.public import PrivateKey, PublicKey
from nacl.exceptions import CryptoError
from coc.crypt import CoCCrypt, CoCNonce


class CoCServerCrypt(CoCCrypt):

    def __init__(self, factory):
        self._factory = factory
        self._sk = PrivateKey(bytes.fromhex("1891d401fadb51d25d3a9174d472a9f691a45b974285d47729c45c6538070d85"))
        self._pk = self._sk.public_key
        self._clientkey = None

    @property
    def serverkey(self):
        return bytes(self._pk)

    @property
    def clientkey(self):
        return bytes(self._clientkey)

    @clientkey.setter
    def clientkey(self, pk):
        self._clientkey = PublicKey(pk)

    def decryptPacket(self, packet):
        messageid = int.from_bytes(packet[:2], byteorder="big")
        unknown = int.from_bytes(packet[5:7], byteorder="big")
        payload = packet[7:]
        if messageid == 10100:
            return messageid, unknown, payload
        elif messageid == 10101:
            self.clientkey = self.client.clientkey = payload[:32]
            nonce = CoCNonce(clientkey=self.clientkey, serverkey=self.serverkey)
            ciphertext = payload[32:]
            try:
                message = self.decrypt(ciphertext, nonce)
            except CryptoError:
                print("Failed to decrypt the message (server, {}).".format(messageid))
                self.transport.loseConnection()
                return False
            else:
                self.decrypt_nonce = self.client.encrypt_nonce = message[24:48]
                return messageid, unknown, message[48:]
        else:
            ciphertext = payload
            message = self.decrypt(ciphertext)
            return messageid, unknown, message

    def encryptPacket(self, messageid, unknown, payload):
        if messageid == 20100:
            return messageid, unknown, payload
        elif messageid == 20104:
            nonce = CoCNonce(nonce=self.decrypt_nonce, clientkey=self.clientkey, serverkey=self.serverkey)
            message = self.encrypt_nonce + self.client.k + payload
            ciphertext = self.encrypt(message, nonce)
            self.k = self.client.k
            return messageid, unknown, ciphertext
        else:
            message = payload
            return messageid, unknown, self.encrypt(message)
