import ctypes
import fcntl

def ioctl_int_get(fd, op):
    res = ctypes.c_int()
    fcntl.ioctl(fd, op, res)
    return res.value

def ioctl_size_t_get(fd, op):
    res = ctypes.c_size_t()
    fcntl.ioctl(fd, op, res)
    return res.value
