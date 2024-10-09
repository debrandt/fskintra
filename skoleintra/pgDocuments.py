# -*- coding: utf-8 -*-

import json

from . import config
from . import sbs4
from . import schildren
from . import semail
from . import surllib

SECTION = 'doc'
MAX_CACHE_AGE = .99


def docFindDocuments(cname, rootTitle, bs, title):
    '''Search a folder for new documents'''
    folder = rootTitle
    if title:
        folder += ' / ' + title.replace('>', '/')

    docs = bs.findAll('div', 'sk-document')
    config.clog(cname, '%s: %d dokumenter fundet ' %
                (folder, len(docs)))

    for doc in docs:
        if doc.find('span', 'sk-documents-document-title') is not None:
            docTitle = doc.find('span', 'sk-documents-document-title').text.strip()
        else:
            continue
            
        if doc.find('div', 'sk-documents-date-column') is not None:
            docDate = doc.find('div', 'sk-documents-date-column').text.strip()
        else:
            continue

        a = doc.find('a')
        url = a and a['href'] or ''
        if '.' in docTitle:
            sfn = docTitle.rsplit('.', 1)[0]
        else:
            sfn = docTitle

        if docTitle and docDate and url:
            # Create HTML snippet
            html = "<p>Nyt dokument: <span></span> / <b></b></p>\n"
            html += "<!-- Sidst opdateret: %s -->" % docDate
            h = sbs4.beautify(html)
            h.span.string = folder
            h.b.string = docTitle

            msg = semail.Message(cname, SECTION, str(h))
            msg.setTitle(sfn)
            msg.setDateTime(docDate)
            msg.addAttachment(url, docTitle)
            msg.setMessageID(url.split('/')[-1])
            msg.maybeSend()


@config.Section(SECTION)
def skoleDocuments(cname):
    'Dokumenter'
    for rootTitle, folder in [('Klassens dokumenter', 'class')]:
        config.clog(cname, '%s: Kigger efter dokumenter' % rootTitle)
        url = schildren.getChildURL(cname, '/documents/' + folder)

        bs = surllib.skoleGetURL(url, True, MAX_CACHE_AGE)
        docFindDocuments(cname, rootTitle, bs, '')

        # look for sub folders
        js = bs.find(id='FoldersJson')
        if js and js.has_attr('value'):
            sfs = json.loads(js['value'])

            for sf in sfs:
                if sf['Name'].startswith('$'):
                    continue

                title = sf['Title']
                url = sf['Url']
                bs = surllib.skoleGetURL(url, True, MAX_CACHE_AGE, None, True)

                docFindDocuments(cname, rootTitle, bs, title)
