
def check_fd(fd):
    """ Validate that a fd parameter looks like a file descriptor.

    Raises an exception if the parameter is invalid.

    :param fd: File descriptor to check.
    """

    if not isinstance(fd, int):
        raise TypeError('fd must be an integer, but was {}'.format(fd.__class__.__name__))
    if fd < 0:
        raise ValueError('fd cannot be negative')
