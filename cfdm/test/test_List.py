import datetime
import os
import unittest

import cfdm


class ListTest(unittest.TestCase):
    def setUp(self):
        # Disable log messages to silence expected warnings
        cfdm.log_level('DISABLE')
        # Note: to enable all messages for given methods, lines or
        # calls (those without a 'verbose' option to do the same)
        # e.g. to debug them, wrap them (for methods, start-to-end
        # internally) as follows:
        #
        # cfdm.LOG_LEVEL('DEBUG')
        # < ... test code ... >
        # cfdm.log_level('DISABLE')

        self.gathered = 'gathered.nc'

    def test_List__repr__str__dump(self):
        f = cfdm.read(self.gathered)[0]

        l = f.data.get_list()

        _ = repr(l)
        _ = str(l)
        _ = l.dump(display=False)

#--- End: class


if __name__ == '__main__':
    print('Run date:', datetime.datetime.utcnow())
    cfdm.environment()
    print()
    unittest.main(verbosity=2)
