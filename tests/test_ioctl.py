import ctypes
import unittest

import ioctl

try:
    import unittest.mock as mock
except ImportError:
    import mock

class TestMain(unittest.TestCase):

    @mock.patch('ioctl._get_ioctl_fn')
    def test_ioctl(self, get_ioctl_fn_mock):
        ioctl_fn = mock.Mock()
        ioctl_fn.return_value = 42
        get_ioctl_fn_mock.return_value = ioctl_fn
        value_ptr = ctypes.byref(ctypes.c_int(13))
        ret = ioctl.ioctl(1, 2, value_ptr)
        assert ret == 42
        assert ioctl_fn.call_count == 1
        args = ioctl_fn.call_args[0]
        assert len(args) == 3
        assert type(args[0]) == type(ctypes.c_int(1))
        assert args[0].value == 1
        assert type(args[1]) == type(ctypes.c_ulong(2))
        assert args[1].value == 2
        assert args[2] == value_ptr

    @mock.patch('ioctl.ioctl')
    @mock.patch('ctypes.byref', new=ctypes.pointer) # Ensure that we can access the pointer.
    def test_ioctl_fn_ptr_r(self, ioctl_mock):
        def _handle_ioctl(fd, request, int_ptr):
            assert fd == 12
            assert request == 32
            assert type(int_ptr) == ctypes.POINTER(ctypes.c_int)
            int_ptr.contents.value = 42
            return mock.DEFAULT
        ioctl_mock.side_effect = _handle_ioctl

        fn = ioctl.ioctl_fn_ptr_r(32, ctypes.c_int)
        res = fn(12)
        assert res == 42

    @mock.patch('ioctl.ioctl')
    @mock.patch('ctypes.byref', new=ctypes.pointer) # Ensure that we can access the pointer.
    def test_ioctl_fn_ptr_w(self, ioctl_mock):
        def _handle_ioctl(fd, request, int_ptr):
            assert fd == 12
            assert request == 32
            assert type(int_ptr) == ctypes.POINTER(ctypes.c_int)
            assert int_ptr.contents.value == 42
            return mock.DEFAULT
        ioctl_mock.side_effect = _handle_ioctl

        fn = ioctl.ioctl_fn_ptr_w(32, ctypes.c_int)
        fn(12, 42)

    @mock.patch('ioctl.ioctl')
    @mock.patch('ctypes.byref', new=ctypes.pointer) # Ensure that we can access the pointer.
    def test_ioctl_fn_ptr_wr(self, ioctl_mock):
        def _handle_ioctl(fd, request, int_ptr):
            assert fd == 12
            assert request == 32
            assert type(int_ptr) == ctypes.POINTER(ctypes.c_int)
            assert int_ptr.contents.value == 24
            int_ptr.contents.value = 42
            return mock.DEFAULT
        ioctl_mock.side_effect = _handle_ioctl

        fn = ioctl.ioctl_fn_ptr_wr(32, ctypes.c_int)
        res = fn(12, 24)
        assert res == 42

    @mock.patch('ioctl.ioctl')
    def test_ioctl_fn_w(self, ioctl_mock):
        def _handle_ioctl(fd, request, int_val):
            assert fd == 12
            assert request == 32
            assert type(int_val) == ctypes.c_int
            assert int_val.value == 42
            return mock.DEFAULT
        ioctl_mock.side_effect = _handle_ioctl

        fn = ioctl.ioctl_fn_w(32, ctypes.c_int)
        fn(12, 42)

if __name__ == '__main__':
    unittest.main()
