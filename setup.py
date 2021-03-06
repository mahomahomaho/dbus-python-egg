"""DBus setup script to build Python egg from a DBus tarball release.

DBus' bindings for Python can be found at `dbus-python`_. This script should be
able to compile and manage any version of ``dbus-python``, without needing to
change it.

Be sure to first run the ``./configure`` script before creating the egg, since C
source files are depending on some files generated by this autotools script.

Then, you can just drop this setup.py file into the unpacked ``dbus-python``
directory, and running ``python setup.py bdist_egg`` should be sufficient.
Alternatively, you can also build a source distribution by running ``python
setup.py sdist``.

You will need to have the following C development libraries installed in order
to create this egg:

    * dbus
    * glib2 and dbus-glib (required only to build dbus-python with Glib
      bindings)

.. _dbus-python: http://dbus.freedesktop.org/releases/dbus-python/
"""

CONFIG_FILE = 'config.h'

import os, sys

# First, check that config file exists
if not os.path.exists(CONFIG_FILE):
    print "%s file doesn't exist in the current directory." % CONFIG_FILE
    print "Please run ./configure before running setup.py script."
    sys.exit(1)



# Then, get the version from the config file
import re

regex_version = r'#define VERSION "([0-9\.]+)"'
version_search = re.search(regex_version, open(CONFIG_FILE).read())

if version_search is None:
    print "Can't find version pattern %r in %s file." % (regex_version,
                                                         CONFIG_FILE)
    print "Maybe you should re-run ./configure ?"
    sys.exit(1)
else:
    version = version_search.groups()[0]
    print "Found dbus-python version %r" % version



# Get correct flags to compile C source files
import glob
import subprocess

from setuptools import setup, Extension


def get_include_flags(package):
    """Return include flags for the specified pkg-config package name."""

    pkg_config = ['pkg-config', '--cflags-only-I', package]

    try:
        proc = subprocess.Popen(pkg_config, close_fds=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except OSError, e:
        print "Unable to execute pkg-config command: %s" % e
        sys.exit(1)

    output = proc.stdout.read()
    err = proc.stderr.read()

    if err != '':
        raise OSError('Unable to get include flags for package %r. '
                      'pkg-config error was:\n\n%s' % (package, err))

    return [inc.strip()[2:]
        for inc in output.strip().split()
        if inc.startswith('-I')]


LOCAL_INCLUDE = [
    'include',
    './', # for CONFIG_FILE
]

DBUS_INCLUDE = get_include_flags('dbus-1')
DBUS_LIB = ['dbus-1']

packages=['dbus']
extensions = [
    Extension(
        '_dbus_bindings', glob.glob('_dbus_bindings/*.c'),
        include_dirs=LOCAL_INCLUDE + DBUS_INCLUDE,
        libraries=DBUS_LIB),
]


# Try to compile with glib support. It won't if glib development librairies
# can't be found.
try:
    GLIB_INCLUDE = get_include_flags('glib-2.0')
    GLIB_LIB=['glib-2.0', 'dbus-glib-1']
except OSError:
    print "Compiled without glib bindings"
    pass
else:
    print "Compiled with glib bindings"
    packages.append('dbus.mainloop')
    glib_ext = Extension(
        '_dbus_glib_bindings', glob.glob('_dbus_glib_bindings/*.c'),
        include_dirs=LOCAL_INCLUDE + DBUS_INCLUDE + GLIB_INCLUDE,
        libraries=DBUS_LIB + GLIB_LIB,
    )
    extensions.append(glib_ext)


setup(
    name='dbus',
    version=version,
    maintainer="Jonathan Ballet",
    maintainer_email="jon@multani.info",
    url="http://dbus.freedesktop.org/",
    install_requires=['setuptools'],
    packages=packages,
    ext_modules=extensions,
    zip_safe = False
)
