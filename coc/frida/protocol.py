from nacl.public import Box, PrivateKey
from coc.protocol import CoCProtocol
import frida
import os


class CoCFridaProtocol(CoCProtocol):

    session = None
    scripts = {}

    def __init__(self, factory):
        super(CoCFridaProtocol, self).__init__(factory)

    def connectionMade(self):
        self.session = frida.get_usb_device(30).attach("com.supercell.clashofclans")
        for module in self.session.enumerate_modules():
            if module.name == "libg.so":
                for export in module.enumerate_exports():
                    if export.name in {
                        "crypto_box_curve25519xsalsa20poly1305_tweet_keypair",
                        # "crypto_box_curve25519xsalsa20poly1305_tweet_afternm",
                        # "crypto_box_curve25519xsalsa20poly1305_tweet_open_afternm",
                        # "blake2b_update"
                    }:
                        name = export.name.replace("curve25519xsalsa20poly1305_tweet_", "")
                        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "js/{}.js".format(name)), "r") as fh:
                            js = fh.read()
                            self.scripts[name] = self.session.create_script(js.replace("ptr(addr)", "ptr({})".format(module.base_address + export.relative_address)))
                            self.scripts[name].on("message", self.recv)
                            self.scripts[name].load()

    def recv(self, message, data=None):
        if data:
            if message["payload"] == "sk":
                sk = PrivateKey(data)
                k = Box(sk, self.factory.server._serverkey)
                self.factory.server._sk = sk
                self.factory.server._k = k
                self.factory.server.client._sk = sk
                self.factory.server.client._k = k
                self.scripts["crypto_box_keypair"].post_message({"type": "keypair"})
            else:
                print(message["payload"], data.hex())

    def encryptPacket(self, messageid, unknown, payload):
        raise NotImplementedError

    def decryptPacket(self, packet):
        raise NotImplementedError

    def packetDecrypted(self, messageid, unknown, payload):
        raise NotImplementedError
