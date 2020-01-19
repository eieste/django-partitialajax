#!/usr/bin/env python

import sys
import os

try:
    import django
    from django.conf import settings

    from django.test.utils import get_runner
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "partitialajax")
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "partitialajax",
        ],
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, "templates")],
            }
        ]
    )
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
