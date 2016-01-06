from __future__ import print_function
import array
import ctypes
import fcntl
import sys
import unittest

import ioctl

try:
    import unittest.mock as mock
except ImportError:
    import mock

def _ctype_to_ptr(value):
    ptr = ctypes.byref(value)
    ptr_type = ctypes.POINTER(ctypes.c_ubyte)
    return ctypes.cast(ptr, ptr_type)

def _ctype_to_bytes(value):
    value_length = ctypes.sizeof(value)
    value_ptr = _ctype_to_ptr(value)
    return bytes(bytearray(value_ptr[0:value_length]))

class IoctlMock(mock.MagicMock):

    def __init__(self, *args, **kwargs):
        set_value = kwargs.pop('set_value', None)
        if set_value is not None:
            if isinstance(set_value, bytes):
                pass # Nothing to convert here
            elif isinstance(set_value, ctypes._SimpleCData):
                set_value = _ctype_to_bytes(set_value)
            else:
                raise TypeError('`set_value` must be a `bytes` object or a ctypes type')
        self.__dict__['_set_value'] = set_value
        super(IoctlMock, self).__init__(*args, **kwargs)

    @staticmethod
    def _arg_to_bytes(arg):
        if isinstance(arg, bytearray):
            return bytes(arg)
        elif isinstance(arg, array.array):
            return arg.tostring()
        elif isinstance(arg, int):
            return _ctype_to_bytes(ctypes.c_int(arg))
        elif isinstance(arg, ctypes._SimpleCData):
            return _ctype_to_bytes(arg)
        else:
            raise TypeError('Unhandled type of arg-parameter for ioctl: {argtype}'.format(argtype=str(type(arg))))

    def _set_arg_return(self, arg):
        set_value = self.__dict__['_set_value']
        if set_value is None:
            return # Nothing to set

        if isinstance(arg, bytearray) or isinstance(arg, array.array):
            arg_array = arg
            arg_size = len(arg)
        elif isinstance(arg, ctypes._SimpleCData):
            arg_array = _ctype_to_ptr(arg)
            arg_size = ctypes.sizeof(arg)
        else:
            raise TypeError('Unhandled type of arg-parameter for ioctl return: {argtype}'.format(argtype=str(type(arg))))

        ret_size = len(set_value)
        if arg_size != ret_size:
            raise Exception('fcntl.ioctl called with a {arg_size} byte buffer, but should have received a {ret_size} byte buffer.'.format(arg_size=arg_size, ret_size=ret_size))

        for i, v in enumerate(bytearray(set_value)):
            arg_array[i] = v

    def __call__(self, fd, op, arg=0, mutate_flag=True):
        wrapped_arg = IoctlMock._arg_to_bytes(arg)
        ret = super(IoctlMock, self).__call__(fd=fd, op=op, arg=wrapped_arg, mutate_flag=mutate_flag)
        self._set_arg_return(arg)
        return ret


class TestMain(unittest.TestCase):

    def test_ioctl_size_t(self):
        with mock.patch('fcntl.ioctl', new=IoctlMock(set_value=ctypes.c_size_t(123))) as ioctl_mock:
            ret = ioctl.ioctl_size_t(5, 7)
            self.assertEqual(ret, 123)
            kwargs = ioctl_mock.call_args[1]
            self.assertEqual(kwargs['fd'], 5)
            self.assertEqual(kwargs['op'], 7)
            self.assertEqual(len(kwargs['arg']), ctypes.sizeof(ctypes.c_size_t))
            self.assertEqual(kwargs['mutate_flag'], True)


    def test_ioctl_int(self):
        with mock.patch('fcntl.ioctl', new=IoctlMock(set_value=ctypes.c_int(123))) as ioctl_mock:
            ret = ioctl.ioctl_int(5, 7)
            self.assertEqual(ret, 123)
            kwargs = ioctl_mock.call_args[1]
            self.assertEqual(kwargs['fd'], 5)
            self.assertEqual(kwargs['op'], 7)
            self.assertEqual(len(kwargs['arg']), ctypes.sizeof(ctypes.c_int))
            self.assertEqual(kwargs['mutate_flag'], True)

if __name__ == '__main__':
    unittest.main()
