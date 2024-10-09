# -*- coding: utf-8 -*-

from . import config
from . import sbs4
from . import schildren
from . import semail
from . import surllib

SECTION = 'ctc'
MAX_CACHE_AGE = 6.9


def contactCard(cname, bs):
    'Check for new contact information for a single pupil'
    # Find name
    name = bs.select('.sk-contact-person-name span.sk-labeledtext-value')
    assert(name)
    name = name[0].text.strip()

    # Change all the div+div+span's into a table
    table = bs.find('div', 'text-block')
    assert(table)  # If this fails, the design has changed drastically
    table.name = 'table'

    for span in table.select('div > span'):
        span.name = 'td'
        span.parent.name = 'tr'
        span['valign'] = 'top'
        if 'sk-labeledtext-value' in span['class']:
            span['style'] = 'font-weight:bold;'

    sbs4.unwrap(table, 'div')

    for h2 in table.select('h2'):
        h2.wrap(bs.new_tag('tr'))
        h2.name = 'td'
        h2['colspan'] = '2'
        h2['style'] = 'font-weight:bold; font-size:18px; padding-top:12px'

    # We do now have two cases depending on whether the image is available
    photob = bs.find('div', 'photo-block')
    img = photob.find('img')

    if img and 'placeholder' not in img['src']:
        # Image is here
        img['style'] = (
            'width:auto;'
            'height:auto;'
            'max-height:200px;'
            'max-width:200px;')
        table.wrap(bs.new_tag('td'))
        photob.name = 'td'
        photob['valign'] = 'top'
        photob['style'] = 'padding-right: 15px;'

        photob.parent.name = 'tr'
        photob.parent.wrap(bs.new_tag('table'))
    else:
        # Either no image or image-placeholder is used
        if photob:
            photob.decompose()

    msg = semail.Message(cname, SECTION, str(bs))
    msg.setTitle(name)
    message_id = bs.url.decode('utf-8').split('/')[-1]
    msg.setMessageID(message_id)
    msg.maybeSend()


@config.Section(SECTION)
def skoleContacts(cname):
    'Kontaktinformation'
    config.clog(cname, 'Kigger efter ny kontaktinformation')
    url = schildren.getChildURL(cname, '/contacts/students/cards')

    bs = surllib.skoleGetURL(url, True, MAX_CACHE_AGE)

    opts = bs.select('#sk-toolbar-contact-dropdown option')
    if not opts:
        config.clog(cname, 'Kan ikke finde nogen elever?')
        return

    for opt in opts:
        url = opt['value']
        bs2 = surllib.skoleGetURL(url, True, bs.cacheage + .01)

        contactCard(cname, bs2)
