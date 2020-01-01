#!/usr/bin/env python

import sys

try:
    import django
    from django.conf import settings

    settings.configure(      
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "partitialajax",
        ])
    django.setup()
    import unittest
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements.txt")


def run_tests(*test_args):
    unittest.main()

if __name__ == '__main__':
    run_tests(*sys.argv[1:])
