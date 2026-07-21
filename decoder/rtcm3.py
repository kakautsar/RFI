"""
RTCM3 Frame Reader

Author : OpenAI + Muhammad Al Kautsar
Project : GNSS RFI Monitoring
"""

from .crc24q import verify

PREAMBLE = 0xD3


class RTCMStream:
    """
    Read RTCM3 frames from socket/file.

    Example
    -------
    stream = RTCMStream(sock)

    for frame in stream:
        print(frame)
    """

    def __init__(self, source):

        self.source = source

    ###############################################################

    def _read_exact(self, n):

        data = b""

        while len(data) < n:

            chunk = self.source.recv(n - len(data))

            if not chunk:
                raise EOFError("Connection closed")

            data += chunk

        return data

    ###############################################################

    def __iter__(self):

        return self

    ###############################################################

    def __next__(self):

        while True:

            b = self._read_exact(1)

            if b[0] == PREAMBLE:
                break

        ###########################################################

        header = self._read_exact(2)

        length = ((header[0] & 0x03) << 8) | header[1]

        ###########################################################

        payload = self._read_exact(length)

        ###########################################################

        crc = self._read_exact(3)

        ###########################################################

        frame = (
            bytes([PREAMBLE])
            + header
            + payload
            + crc
        )

        if not verify(frame):

            raise ValueError("CRC24Q failed")

        return frame

    ###############################################################

    def read_frame(self):

        return next(self)
