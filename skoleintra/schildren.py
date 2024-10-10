# -*- coding: utf-8 -*-

import re

from . import config
from . import surllib

# Map of children => urlPrefix
# 'Andrea 0A' => '/parent/1234/Andrea/'
_children = None


def getChildren():
    '''Returns of list of "available" children in the system'''
    global _children

    def ckey(n): return tuple(n.rsplit(' ', 1)[::-1])

    if not _children:
        _children = dict()
        seen = set()

        config.log('Henter liste af børn')
        data = surllib.skoleLogin()

        # Name of "First child"
        fst = data.find(id="sk-personal-menu-button").text.strip()

        for a in data.findAll('a', href=re.compile('^(/[^/]*){3}/Index$')):
            url = a['href'].rsplit('/', 1)[0].rstrip('/')
            if url in seen:
                continue
            seen.add(url)
            name = a.text.strip() or fst
            if name not in _children:
                config.log('Barn %s => %s' % (name, url), 2)
                _children[name] = url
        cns = sorted(list(_children.keys()), key=ckey)
        config.log('Følgende børn blev fundet: ' + ', '.join(cns))

    return sorted(list(_children.keys()), key=ckey)


def getChildURLPrefix(cname):
    getChildren()
    assert(cname in _children)

    return surllib.absurl(_children[cname])


def getChildURL(cname, suffix):
    # Guessing a bug in forældre intra as weekplan urls have the following
    # format: parent/CHILD_ID/CHILD_NAMEitem/weeklyplansandhomework/list
    assert(suffix.startswith('/') or suffix.startswith('item/'))
    return getChildURLPrefix(cname) + suffix
