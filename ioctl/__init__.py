import ctypes
import fcntl

def ioctl_int(fd, op, value=0):
    res = ctypes.c_int(value)
    fcntl.ioctl(fd, op, res)
    return res.value

def ioctl_size_t(fd, op, value=0):
    res = ctypes.c_size_t(value)
    fcntl.ioctl(fd, op, res)
    return res.value
