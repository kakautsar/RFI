"""
CRC24Q implementation for RTCM3

Polynomial : 0x1864CFB
Initial    : 0x000000

Reference:
RTCM Standard 10403.x
"""

CRC24Q_POLY = 0x1864CFB


def crc24q(data: bytes) -> int:
    """
    Calculate CRC24Q.

    Parameters
    ----------
    data : bytes
        RTCM frame without CRC

    Returns
    -------
    int
        24-bit CRC
    """

    crc = 0

    for byte in data:

        crc ^= byte << 16

        for _ in range(8):

            crc <<= 1

            if crc & 0x1000000:
                crc ^= CRC24Q_POLY

            crc &= 0xFFFFFF

    return crc


def verify(frame: bytes) -> bool:
    """
    Verify RTCM3 CRC.

    Parameters
    ----------
    frame : bytes
        Complete RTCM frame
        including CRC

    Returns
    -------
    bool
    """

    if len(frame) < 6:
        return False

    body = frame[:-3]

    crc_recv = (
        (frame[-3] << 16)
        | (frame[-2] << 8)
        | frame[-1]
    )

    crc_calc = crc24q(body)

    return crc_calc == crc_recv


def append_crc(frame: bytes) -> bytes:
    """
    Append CRC24Q to frame.

    Useful for testing.
    """

    crc = crc24q(frame)

    return frame + bytes([
        (crc >> 16) & 0xFF,
        (crc >> 8) & 0xFF,
        crc & 0xFF
    ])
