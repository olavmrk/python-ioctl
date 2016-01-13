import ctypes
import os
import subprocess
import tempfile
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

def _native_values():
    source_file = os.path.join(os.path.dirname(__file__), 'linux_ioctls.c')
    exec_file_fd, exec_file = tempfile.mkstemp()
    os.close(exec_file_fd)
    try:
        subprocess.check_output(['gcc', '-std=c99', '-Wall', '-o', exec_file, source_file], stderr=subprocess.STDOUT)
        values = subprocess.check_output([exec_file])
    finally:
        os.unlink(exec_file)
    values = eval(values)
    return values

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

    def test_native(self):
        try:
            native_values = _native_values()
        except:
            # For some reason unable to compile & run the ioctl-printing program.
            # Could be missing the GCC compiler or the linux headers.
            raise
            raise unittest.SkipTest('Unable to build & run native program for dumping ioctl values.')
        self._test_values(native_values)
