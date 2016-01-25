from pyblake2 import blake2b
import nacl.utils
from nacl.public import Box, PrivateKey, PublicKey


class CoCCrypto:
    _sk = None
    _pk = None
    _k = None
    _encrypt_nonce = None
    _decrypt_nonce = None

    session_key = None

    @property
    def pk(self):
        return bytes(self._pk)

    @property
    def k(self):
        return bytes(self._k)

    @k.setter
    def k(self, k):
        self._k = Box.decode(k)

    @property
    def encrypt_nonce(self):
        return bytes(self._encrypt_nonce)

    @encrypt_nonce.setter
    def encrypt_nonce(self, encrypt_nonce):
        self._encrypt_nonce = CoCNonce(nonce=encrypt_nonce)

    @property
    def decrypt_nonce(self):
        return bytes(self._decrypt_nonce)

    @decrypt_nonce.setter
    def decrypt_nonce(self, decrypt_nonce):
        self._decrypt_nonce = CoCNonce(nonce=decrypt_nonce)

    def keypair(self):
        self._sk = PrivateKey.generate()
        self._pk = self._sk.public_key

    def beforenm(self, pk):
        pk = PublicKey(bytes(pk))
        self._k = Box(self._sk, pk)

    def encrypt(self, message, nonce=None):
        if not nonce:
            self._encrypt_nonce.increment()
            nonce = self.encrypt_nonce
        return self._k.encrypt(message, bytes(nonce))[24:]

    def decrypt(self, ciphertext, nonce=None):
        if not nonce:
            self._decrypt_nonce.increment()
            nonce = self.decrypt_nonce
        return self._k.decrypt(ciphertext, bytes(nonce))

    def encryptPacket(self, messageid, unknown, payload):
        raise NotImplementedError

    def decryptPacket(self, packet):
        raise NotImplementedError


class CoCNonce:

    def __init__(self, nonce=None, clientkey=None, serverkey=None):
        if not clientkey:
            if nonce:
                self._nonce = nonce
            else:
                self._nonce = nacl.utils.random(Box.NONCE_SIZE)
        else:
            b2 = blake2b(digest_size=24)
            if nonce:
                b2.update(bytes(nonce))
            b2.update(bytes(clientkey))
            b2.update(bytes(serverkey))
            self._nonce = b2.digest()

    def __bytes__(self):
        return self._nonce

    def __len__(self):
        return len(self._nonce)

    def increment(self):
        self._nonce = (int.from_bytes(self._nonce, byteorder="little") + 2).to_bytes(Box.NONCE_SIZE, byteorder="little")
