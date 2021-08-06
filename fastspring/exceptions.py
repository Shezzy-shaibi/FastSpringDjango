from __future__ import absolute_import, print_function, unicode_literals


class FsprgException(Exception):

    attrs = ('httpStatusCode', 'errorCode')

    def __init__(self, *args, **kwargs):
        for attr in self.attrs:
            setattr(self, attr, kwargs.pop(attr, None))

        super(FsprgException, self).__init__(*args, **kwargs)
