from __future__ import print_function
import ctypes
import fcntl
import sys
import unittest

import ioctl

try:
    import unittest.mock as mock
except ImportError:
    import mock

def _ioctl_get_generator(retval):
    def _ioctl_handler(fd, op, arg=0, mutate_flag=True):
        if isinstance(retval, ctypes._SimpleCData):
            ret_size = ctypes.sizeof(retval)
            retval_ptr = ctypes.byref(retval)
        else:
            ret_size = len(retval)
            retval_ptr = (ctypes.c_ubyte * ret_size).from_buffer_copy(retval)

        arg_size = ctypes.sizeof(arg)
        if arg_size != ret_size:
            raise Exception('fcntl.ioctl called with a {arg_size} byte buffer, but should have received a {ret_size} byte buffer.'.format(arg_size=arg_size, ret_size=ret_size))

        ctypes.memmove(ctypes.byref(arg), retval_ptr, ret_size)

    return _ioctl_handler

class TestMain(unittest.TestCase):

    @mock.patch('fcntl.ioctl', new=_ioctl_get_generator(retval=ctypes.c_size_t(123)))
    def test_ioctl_size_t(self):
        ret = ioctl.ioctl_size_t(5, 7)
        self.assertEquals(ret, 123)

    @mock.patch('fcntl.ioctl', new=_ioctl_get_generator(retval=ctypes.c_int(123)))
    def test_ioctl_int(self):
        ret = ioctl.ioctl_int(5, 7)
        self.assertEquals(ret, 123)

if __name__ == '__main__':
    unittest.main()
