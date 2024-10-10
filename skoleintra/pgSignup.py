# -*- coding: utf-8 -*-

from . import config
from . import sbs4
from . import schildren
from . import semail
from . import surllib

SECTION = 'sgn'
MAX_CACHE_AGE = .49


def findEvents(cname, bs):
    '''Look for new events'''
    toptitle = bs.select('.sk-grid-top-header li')
    toptitle = toptitle[0].string.strip() if toptitle else 'Ukendt'

    for ul in bs.select('.sk-signup-container ul.ccl-rwgm-row'):
        if 'sk-grid-top-header' in ul['class']:
            continue   # Ignore top header
        ebs = sbs4.beautify('<p><dl></dl></p>')
        dl = ebs.dl

        key = ''
        kv, kvl = {}, []
        for li in ul.select('li'):
            # Kill a tags inside, if any
            for a in (li.findAll('a') or []):
                a.unwrap()
            s = li.text.strip()

            if 'sk-grid-inline-header' in li['class']:
                li.name = 'dt'
                li['style'] = 'font-weight:bold'
                key = s.rstrip(':')
            else:
                li.name = 'dd'
                kvl.append((key, s))
                kv[key.lower()] = s
            dl.append(li)

        if list(k for k, v in list(kv.items()) if k.startswith('status') and
                v.lower().startswith('lukket')):
            continue  # Ignore this line

        msg = semail.Message(cname, SECTION, str(ebs))
        msg.setTitle('%s: %s' % kvl[0])
        msg.maybeSend()


@config.Section(SECTION, True)
def skoleSignup(cname):
    'Tilmelding til samtaler/arrangementer'
    config.clog(cname, 'Kigger efter nye samtaler/arrangementer')
    for suffix in ('conversation', 'event'):
        url = schildren.getChildURL(cname, '/signup/' + suffix)
        bs = surllib.skoleGetURL(url, True, MAX_CACHE_AGE)
        findEvents(cname, bs)
