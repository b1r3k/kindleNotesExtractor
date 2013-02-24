import unittest
import sys

if __name__ == "__main__":
    test_suite = unittest.defaultTestLoader.discover("tests", pattern='test*.py')

    unittest.TextTestRunner(verbosity=2).run(test_suite)
