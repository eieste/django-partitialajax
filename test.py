#!/usr/bin/env python

import sys

try:
    import django
    from django.conf import settings

    from django.test.utils import get_runner
    settings.configure(      
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "partitialajax",
        ])
    django.setup()
    
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements.txt")


def run_tests(*test_args):
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["partitialajax"])
    sys.exit(bool(failures))
    
    
    
    
if __name__ == '__main__':
    run_tests(*sys.argv[1:])
