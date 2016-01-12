python-ioctl
============

This Python module contains some simple helper functions for calling `fcntl.ioctl()`_.

.. _`fcntl.ioctl()`: https://docs.python.org/3/library/fcntl.html#fcntl.ioctl

Example
-------

::

  import os
  import ioctl
  RNDGETENTCNT = 0x80045200
  fd = os.open('/dev/random', os.O_RDONLY)
  _, entropy_avail = ioctl.ioctl_ptr_size_t(fd, RNDGETENTCNT)
  print('entropy_avail:', entropy_avail)
