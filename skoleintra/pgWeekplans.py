# -*- coding: utf-8 -*-

from . import config
from . import sbs4
from . import schildren
from . import semail
from . import surllib


SECTION = 'pln'


def formatWeekplan(bs):
    '''Format the weekplan nicely for email'''
    weekplan = bs.find('div', "sk-weekly-plan-container")
    if not weekplan:
        # Sometimes there is actually not a weekly plan
        return None
    # Change into table
    table = weekplan.div
    table.name = 'table'
    # Remove a couple of unneeded tags
    sbs4.unwrap(weekplan, 'div.sk-weekly-plan-grid')
    sbs4.unwrap(weekplan, 'ul.sk-weekly-plan-grid-row')

    # li -> tr + wrap div content in td
    for li in weekplan.select('.sk-weekly-plan-header'):
        li.name = 'tr'
        # Clear attributes, so next loop can access ul in
        # li.sk-weekly-plan-grid-cell
        li.attrs = {}
        li.div.wrap(bs.new_tag('td'))
        li.div.wrap(bs.new_tag('b'))

    # li -> tr + wrap ul content in td
    for li in weekplan.select('.sk-weekly-plan-grid-cell'):
        li.name = 'tr'
        li.attrs = {}
        li.ul.wrap(bs.new_tag('td'))

    # format
    for span in weekplan.select('.sk-weekly-plan-day'):
        span["style"] = 'display: block; font-weight: 600;'

    # format
    for span in weekplan.select('.sk-weekly-plan-date'):
        span['style'] = 'display: block;'

    # format
    for ul in weekplan.select('.sk-list'):
        ul['style'] = 'list-style-type:none;'

    return weekplan


def getWeekplan(cname, url):
    bs = surllib.skoleGetURL(url, True, noCache=True)
    return formatWeekplan(bs)


@config.Section(SECTION)
def skoleWeekplans(cname):
    'Ugeplaner'
    config.clog(cname, 'Kigger efter nye ugeplaner')
    url = schildren.getChildURL(cname, 'item/weeklyplansandhomework/list/')

    bs = surllib.skoleGetURL(url, True, noCache=True)

    ul = bs.find('ul', 'sk-weekly-plans-list-container')
    if ul:
        for a in ul.find_all('a', href=True):
            url = a['href']
            plan = getWeekplan(cname, url)
            if not plan:
                continue
            wid = url.split('/')[-1]  # e.g. 35-2018
            title = plan.find('h3').text.strip()

            msg = semail.Message(cname, SECTION, str(plan))
            msg.setTitle(title)
            msg.setMessageID(wid)
            msg.maybeSend()
    else:
        if 'ikke autoriseret' in bs.text:
            config.clog(cname, 'Din skole bruger ikke ugeplaner. '
                        "Du bør bruge '--section ,-%s'" % SECTION)
