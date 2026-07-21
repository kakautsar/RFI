"""
RTCM3 Bit Reader

Author : OpenAI + Muhammad Al Kautsar
Project : GNSS RFI Monitoring
"""

from typing import Union


class BitReader:
    """
    Read arbitrary bits from bytes.

    Example
    -------
    br = BitReader(data)

    value = br.read(12)

    """

    def __init__(self, data: Union[bytes, bytearray]):

        self.data = data
        self.bitpos = 0
        self.length = len(data) * 8

    ###############################################################

    def remaining(self):

        return self.length - self.bitpos

    ###############################################################

    def seek(self, bit):

        if bit < 0:
            raise ValueError("negative seek")

        if bit > self.length:
            raise ValueError("seek beyond end")

        self.bitpos = bit

    ###############################################################

    def tell(self):

        return self.bitpos

    ###############################################################

    def align_byte(self):

        r = self.bitpos % 8

        if r != 0:
            self.bitpos += (8-r)

    ###############################################################

    def skip(self, n):

        self.seek(self.bitpos+n)

    ###############################################################

    def read(self, n):

        """
        Read unsigned integer
        """

        if n <= 0:
            return 0

        if self.bitpos+n > self.length:

            raise EOFError(
                "Attempt to read beyond buffer."
            )

        value = 0

        for _ in range(n):

            byte = self.bitpos//8

            bit = 7-(self.bitpos % 8)

            value <<= 1

            value |= (
                self.data[byte] >> bit
            ) & 1

            self.bitpos += 1

        return value

    ###############################################################

    def read_signed(self, n):

        """
        Two's complement signed integer
        """

        value = self.read(n)

        sign = 1 << (n-1)

        if value & sign:

            value -= (1 << n)

        return value

    ###############################################################

    def read_bool(self):

        return bool(self.read(1))

    ###############################################################

    def peek(self, n):

        p = self.bitpos

        value = self.read(n)

        self.bitpos = p

        return value

    ###############################################################

    def eof(self):

        return self.bitpos >= self.length
