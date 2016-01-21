from twisted.internet.endpoints import TCP4ServerEndpoint


class CoCServerEndpoint(TCP4ServerEndpoint):

    @property
    def interface(self):
        if not self._interface:
            return "0.0.0.0"
        else:
            return self._interface

    @property
    def port(self):
        return self._port
