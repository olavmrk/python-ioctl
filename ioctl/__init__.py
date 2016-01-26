import ctypes
import ctypes.util
import fcntl
import os
import sys

from ._paramcheck import (
    check_ctypes_datatype,
    check_fd,
    check_request,
)

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

def _init_ioctl():
    libc_name = ctypes.util.find_library('c')
    if not libc_name:
        raise Exception('Unable to find c library')
    libc = ctypes.CDLL(libc_name, use_errno=True)
    return libc.ioctl

ioctl_fn = None
def ioctl(fd, request, *args):
    """ Call the C library ioctl()-function directly.

    This function invokes ioctl() through ctypes. This gives
    greater control over the parameters passed to ioctl().

    :param fd: File descriptor to operate on.
    :param request: The ioctl request to call.
    :param args: parameter to pass to ioctl.
    :return: The return value of the ioctl-call.
    """

    check_fd(fd)
    check_request(request)
    ioctl_args = [ ctypes.c_int(fd), ctypes.c_ulong(request)] + list(args)

    global ioctl_fn
    if ioctl_fn is None:
        try:
            ioctl_fn = _init_ioctl()
        except Exception as e:
            raise NotImplementedError('Unable to get ioctl()-function from C library: {err}'.format(err=str(e)))

    res = ioctl_fn(*ioctl_args)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))
    return res

def ioctl_fn_ptr_r(request, datatype, return_python=None):
    """ Create a helper function for invoking a ioctl() read call.

    This function creates a helper function for creating a ioctl() read function.
    It will call the ioctl() function with a pointer to data, and return the contents
    of the data after the call.

    If the datatype is a integer type (int, long, etc), it will be returned as a python int or long.

    :param request: The ioctl request to call.
    :param datatype: The data type of the data returned by the ioctl() call.
    :param return_python: Whether we should attempt to convert the return data to a Python value. Defaults to True for fundamental ctypes data types.
    :return: A function for invoking the specified ioctl().

    :Example:
      ::

          import os
          import ioctl
          import ioctl.linux
          RNDGETENTCNT = ioctl.linux.IOR('R', 0x00, ctypes.c_int)
          rndgetentcnt = ioctl.ioctl_fn_ptr_r(RNDGETENTCNT, ctypes.c_int)
          fd = os.open('/dev/random', os.O_RDONLY)
          entropy_avail = rndgetentcnt(fd)
    """

    check_request(request)
    check_ctypes_datatype(datatype)
    if return_python is not None and not isinstance(return_python, bool):
        raise TypeError('return_python must be None or a boolean, but was {}'.format(return_python.__class__.__name__))


    if return_python is None:
        return_python = issubclass(datatype, ctypes._SimpleCData)

    def fn(fd):
        check_fd(fd)
        value = datatype()
        ioctl(fd, request, ctypes.byref(value))
        if return_python:
            return value.value
        else:
            return value
    return fn

def ioctl_ptr_int(fd, request, value=0):
    """Call ioctl() with an ``int *`` argument.

    :param fd: File descriptor to operate on.
    :param request: The ioctl request to call.
    :param value: Optional value to pass to the ioctl() operation. Defaults to 0.
    :return: Tuple of ``(ioctl_return, updated_value)``.
            ``ioctl_return`` is the return value of the ioctl()-call, while
            ``updated_value`` is the value of the integer argument after the
            ioctl()-call.
    """
    check_fd(fd)
    check_request(request)
    res = ctypes.c_int(value)
    ioctl_return = fcntl.ioctl(fd, request, res)
    return (ioctl_return, res.value)

def ioctl_ptr_size_t(fd, request, value=0):
    """Call ioctl() with a ``size_t *`` argument.

    :param fd: File descriptor to operate on.
    :param request: ioctl request to call.
    :param value: Optional value to pass to the ioctl() operation. Defaults to 0.
    :return: Tuple of ``(ioctl_return, updated_value)``.
             ``ioctl_return`` is the return value of the ioctl()-call, while
             ``updated_value`` is the value of the size_t argument after the
             ioctl()-call.
    """
    check_fd(fd)
    check_request(request)
    res = ctypes.c_size_t(value)
    ioctl_return = fcntl.ioctl(fd, request, res)
    return (ioctl_return, res.value)

def ioctl_ptr_buffer(fd, request, value=None, length=None):
    """Call ioctl() with a ``void *`` argument.

    You must specify either the ``value`` parameter or the ``length`` parameter.
    If the ``length`` parameter is specified, this function will allocate a byte
    buffer of the specified length to pass to ioctl().

    :param fd: File descriptor to operate on.
    :param request: ioctl request to call.
    :param value: Optional contents of the byte buffer at the start of the call.
    :param length: Optional length of the byte buffer.
    :return: Tuple of ``(ioctl_return, updated_value)``.
             ``ioctl_return`` is the return value of the ioctl()-call, while
             ``updated_value`` is the contents of the buffer after the ioctl()-call.
    """
    check_fd(fd)
    check_request(request)
    if value is None and length is None:
        raise ValueError('Must specify either `value` or `length`')
    if value is not None and length is not None:
        raise ValueError('Cannot specify both `value` and `length`')
    if value is None:
        value = [0] * length
    data = _to_bytearray(value)
    ioctl_return = fcntl.ioctl(fd, request, data)
    data = _from_bytearray(data)
    return (ioctl_return, data)
