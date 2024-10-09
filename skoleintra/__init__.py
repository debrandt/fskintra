# -*- coding: utf-8 -*-

import sys
import locale


def dependencyError(package, required, current=None):
    err = 'fskintra kræver %s version %s' % (package, required)
    if current:
        err += '\n%s version %s er installeret' % (package, current)
    sys.exit('''%s
Se evt. her for hjælp:
    https://svalgaard.github.io/fskintra/install#krav''' % err)


#
# Beautiful Soup ?
#
try:
    import bs4
    if bs4.__version__ < '4.10':
        dependencyError('BeautifulSoup', '4.10.x', bs4.__version__)
except ImportError:
    dependencyError('BeautifulSoup', '4.10.x')

#
# lxml in a version suitable for BeautifulSoup4
#
try:
    b = bs4.BeautifulSoup('<i>test</i>', 'lxml')
except bs4.FeatureNotFound:
    dependencyError('lxml', 'i en version der kan køre sammen med '
                    'BeautifulSoup 4')

#
# Mechanize
#
# try:
#     import mechanize
#     if mechanize.__version__ < (0, 4):
#         dependencyError('Mechanize', '0.4.x',
#                         '.'.join(map(str, mechanize.__version__[:3])))
# except ImportError as e:
#     raise e
#     dependencyError('Mechanize', '0.4.x')

#
# Check that a Danish locale is available
# o.w. fail nicely
#
for loc in ['da_DK.utf-8', 'da_DK.iso8859-1', 'da_DK.iso8859-15', 'da_DK']:
    try:
        locale.setlocale(locale.LC_TIME, loc)
    except locale.Error:
        continue  # Try the next locale
    break  # Found a valid Danish locale
else:
    sys.exit('''
fskintra kræver at Python kan forstå datoformater på dansk (dansk locale).
Se evt. her for hjælp:
    https://svalgaard.github.io/fskintra/troubleshooting#dansk-locale
'''.lstrip())
