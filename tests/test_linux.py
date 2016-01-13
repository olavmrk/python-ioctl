import ctypes
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import ioctl.linux

arch_values = {
    'i386': {
        'sizeof_int': 4,
        'sizeof_ff_effect': 44,
        'EVIOCSFF': 0x402c4580,
        'BLKRRPART': 0x0000125f,
        'RNDGETENTCNT': 0x80045200,
        'RNDADDTOENTCNT': 0x40045201,
        'FIFREEZE': 0xc0045877,
    },
}

class TestLinux(unittest.TestCase):

    def _test_values(self, values):
        EVIOCSFF = ioctl.linux.IOC('w', 'E', 0x80, values['sizeof_ff_effect'])
        self.assertEqual(EVIOCSFF, values['EVIOCSFF'])

        BLKRRPART = ioctl.linux.IO(0x12, 95)
        self.assertEqual(BLKRRPART, values['BLKRRPART'])

        RNDGETENTCNT = ioctl.linux.IOR('R', 0x00, values['sizeof_int'])
        self.assertEqual(RNDGETENTCNT, values['RNDGETENTCNT'])

        RNDADDTOENTCNT = ioctl.linux.IOW('R', 0x01, values['sizeof_int'])
        self.assertEqual(RNDADDTOENTCNT, values['RNDADDTOENTCNT'])

        FIFREEZE = ioctl.linux.IOWR('X', 119, values['sizeof_int'])
        self.assertEqual(FIFREEZE, values['FIFREEZE'])

    def test_i386(self):
        with mock.patch('platform.machine', return_value='i386'):
            self._test_values(arch_values['i386'])
