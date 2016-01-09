import ctypes
import fcntl
import sys

# In Python 2, the bytearray()-type does not support the buffer interface,
# and can therefore not be used in ioctl().
# This creates a couple of helper functions for converting to and from 
if sys.version_info < (3, 0):
    import array
    def _to_bytearray(value):
        return array.array('B', value)
    def _from_bytearray(value):
        return value.tostring()
else:
    def _to_bytearray(value):
        return bytearray(value)
    def _from_bytearray(value):
        return bytes(value)

def ioctl_ptr_int(fd, request, value=0):
    """Call ioctl() with an `int *` argument.

    :param fd: File descriptor to operate on.
    :param request: The ioctl request to call.
    :param value: Optional value to pass to the ioctl() operation. Defaults to 0.
    :return The contents of the value parameter after the call to ioctl().
    """
    res = ctypes.c_int(value)
    fcntl.ioctl(fd, request, res)
    return res.value

def ioctl_ptr_size_t(fd, request, value=0):
    """Call ioctl() with a `size_t *` argument.

    :param fd: File descriptor to operate on.
    :param request: ioctl request to call.
    :param value: Optional value to pass to the ioctl() operation. Defaults to 0.
    :return: The contents of the value parameter after the call to ioctl().
    """
    res = ctypes.c_size_t(value)
    fcntl.ioctl(fd, request, res)
    return res.value

def ioctl_ptr_buffer(fd, request, value=None, length=None):
    """Call ioctl() with a `void *` argument.

    You must specify either the `value` parameter or the `length` parameter.
    If the `length` parameter is specified, this function will allocate a byte
    buffer of the specified length to pass to ioctl().

    :param fd: File descriptor to operate on.
    :param request: ioctl request to call.
    :param value: Optional contents of the byte buffer at the start of the call.
    :param length: Optional length of the byte buffer.
    :return: The contents of the value parameter after the call to ioctl().
    """
    request = int(request)
    if value is None and length is None:
        raise ValueError('Must specify either `value` or `length`')
    if value is not None and length is not None:
        raise ValueError('Cannot specify both `value` and `length`')
    if value is None:
        value = [0] * length
    data = _to_bytearray(value)
    fcntl.ioctl(fd, request, data)
    data = _from_bytearray(data)
    return data
