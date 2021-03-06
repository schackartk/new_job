#!/usr/bin/env python3
""" tests for new.py """

import io
import os
import random
import string
from subprocess import getstatusoutput
from shutil import rmtree
from new_job import get_defaults

PRG = './new_job.py'


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_get_defaults():
    """ Test get_defaults() """

    expected = {
        random_string(): random_string()
        for _ in range(random.randint(3, 7))
    }
    text = io.StringIO('\n'.join(f'{k}={v}' for k, v in expected.items()))
    assert get_defaults(text) == expected
    assert get_defaults(None) == {}


# --------------------------------------------------
def test_usage():
    """ Prints usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_ok():
    """ Runs ok """

    cwd = os.path.abspath(os.getcwd())
    dirname = os.path.join(cwd, random_string())
    abs_new = os.path.abspath(PRG)

    if os.path.isdir(dirname):
        rmtree(dirname)

    os.makedirs(dirname)
    os.chdir(dirname)

    try:
        basename = random_string()
        name = basename + '.sh'
        retval, out = getstatusoutput(f'{abs_new} {name}')
        assert retval == 0
        assert os.path.isfile(name)
        assert out == f'Done, see new script "{name}".'

    finally:
        if os.path.isdir(dirname):
            rmtree(dirname)
        os.chdir(cwd)


# --------------------------------------------------
def random_string():
    """ generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
