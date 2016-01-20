__author__ = 'No3x'

from socketIO_client import SocketIO, LoggingNamespace
# import logging
# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)
import math
import collections


class VirtualBlinkStick:
    currentColors = collections.OrderedDict()

    # Round values
    def __round(self, colors):
        roundedColors = []
        for k, v in colors:
            (R, G, B) = v
            R = math.floor(R)
            G = math.floor(G)
            B = math.floor(B)
            v = (R, G, B)
            roundedColors.append(v)
        return roundedColors

    def setCurrentColors(self, currentColors):
        self.currentColors = self.__round(currentColors)

    def connect(self):
        return True

    def run(self):
        with SocketIO('localhost', 7076, LoggingNamespace) as socketIO:
            socketIO.emit('setColors', {'colors': self.currentColors})
            socketIO.wait_for_callbacks(seconds=2)
