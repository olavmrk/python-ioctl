import ctypes
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import ioctl.linux


class TestLinux(unittest.TestCase):

    @mock.patch('platform.machine', return_value='i386')
    def test_i386(self, _mock):

        sizeof_ff_effect = 44
        EVIOCSFF = ioctl.linux.IOC('w', 'E', 0x80, sizeof_ff_effect)
        self.assertEqual(EVIOCSFF, 0x402c4580)

        BLKRRPART = ioctl.linux.IO(0x12, 95)
        self.assertEqual(BLKRRPART, 0x0000125f)

        RNDGETENTCNT = ioctl.linux.IOR('R', 0x00, ctypes.c_int)
        self.assertEqual(RNDGETENTCNT, 0x80045200)

        RNDGETENTCNT = ioctl.linux.IOR('R', 0x00, 4)

        RNDADDTOENTCNT = ioctl.linux.IOW('R', 0x01, ctypes.c_int)
        self.assertEqual(RNDADDTOENTCNT, 0x40045201)

        FIFREEZE = ioctl.linux.IOWR('X', 119, ctypes.c_int)
        self.assertEqual(FIFREEZE, 0xc0045877)
