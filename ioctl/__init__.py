import ctypes
import ctypes.util
import os

from ._paramcheck import (
    check_ctypes_datatype,
    check_fd,
    check_request,
)

_ioctl_fn = None
def _get_ioctl_fn():
    global _ioctl_fn
    if _ioctl_fn is not None:
        return _ioctl_fn
    libc_name = ctypes.util.find_library('c')
    if not libc_name:
        raise Exception('Unable to find c library')
    libc = ctypes.CDLL(libc_name, use_errno=True)
    _ioctl_fn = libc.ioctl
    return _ioctl_fn

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

    try:
        ioctl_fn = _get_ioctl_fn()
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

          import ctypes
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

def ioctl_fn_ptr_w(request, datatype):
    """ Create a helper function for invoking a ioctl() write call.

    This function creates a helper function for creating a ioctl() write function that uses a pointer argument.
    E.g. if you have a ioctl() call like::

      int param = 42;
      ioctl(fd, RNDADDTOENTCNT, &param);

    :param request: The ioctl request to call.
    :param datatype: The data type of the data to be passed to the ioctl() call.
    :return: A function for invoking the specified ioctl().

    :Example:
      ::

          import ctypes
          import os
          import ioctl
          import ioctl.linux
          RNDADDTOENTCNT = ioctl.linux.IOW('R', 0x01, ctypes.c_int)
          rndaddtoentcnt = ioctl.ioctl_fn_ptr_w(RNDADDTOENTCNT, ctypes.c_int)
          fd = os.open('/dev/random', os.O_RDONLY)
          rndaddtoentcnt(fd, -100) # Decrease entropy by 100 bits.
    """

    check_request(request)
    check_ctypes_datatype(datatype)

    def fn(fd, value):
        check_fd(fd)
        value = datatype(value)
        ioctl(fd, request, ctypes.byref(value))
    return fn

def ioctl_fn_ptr_rw(request, datatype, return_python=None):
    """ Create a helper function for invoking a ioctl() read & write call.

    This function creates a helper function for a ioctl() operation that both reads and writes data.
    Typically the case is a ioctl() operation that receives a pointer to data, performs an operation and updates the data at the pointer.
    E.g. if you have a ioctl() call like::

      int timeout = 45;
      ioctl(fd, WDIOF_SETTIMEOUT, &timeout);
      printf("Actual timeout: %d\n", timeout);

    :param request: The ioctl request to call.
    :param datatype: The data type of the data to be passed to the ioctl() call.
    :param return_python: Whether we should attempt to convert the return data to a Python value. Defaults to True for fundamental ctypes data types.
    :return: A function for invoking the specified ioctl().

    :Example:
      ::

          import ctypes
          import os
          import ioctl
          WDIOF_SETTIMEOUT = 0x0080
          wdiof_settimeout = ioctl.ioctl_fn_ptr_w(WDIOF_SETTIMEOUT, ctypes.c_int)
          fd = os.open('/dev/watchdog', os.O_RDONLY)
          actual_timeout = wdiof_settimeout(fd, 60)
    """

    check_request(request)
    check_ctypes_datatype(datatype)
    if return_python is not None and not isinstance(return_python, bool):
        raise TypeError('return_python must be None or a boolean, but was {}'.format(return_python.__class__.__name__))

    if return_python is None:
        return_python = issubclass(datatype, ctypes._SimpleCData)

    def fn(fd, value):
        check_fd(fd)
        value = datatype(value)
        ioctl(fd, request, ctypes.byref(value))
        if return_python:
            return value.value
        else:
            return value
    return fn

def ioctl_fn_w(request, datatype):
    """ Create a helper function for invoking a ioctl() write call.

    This function creates a helper function for creating a ioctl() write function that directly passes a single argument.
    E.g. if you have a ioctl() call like::

      unsigned long fd = 3;
      ioctl(fd, LOOP_SET_FD, value);

    :param request: The ioctl request to call.
    :param datatype: The data type of the data to be passed to the ioctl() call.
    :return: A function for invoking the specified ioctl().

    :Example:
      ::

          import ctypes
          import os
          import ioctl
          LOOP_SET_FD = 0x4C00
          loop_set_fd = ioctl.ioctl_fn_w(LOOP_SET_FD, ctypes.c_ulong)
          loop_fd = os.open('/dev/loop0', os.O_RDONLY)
          file_fd = os.open('/tmp/data', os.O_RDWR)
          loop_set_fd(loop_fd, file_fd)
    """

    check_request(request)
    check_ctypes_datatype(datatype)

    def fn(fd, value):
        check_fd(fd)
        value = datatype(value)
        ioctl(fd, request, value)
    return fn
