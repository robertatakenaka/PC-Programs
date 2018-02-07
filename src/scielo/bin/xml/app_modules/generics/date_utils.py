
# coding=utf-8

from datetime import datetime

from ..__init__ import _


URL_CHECKED = []

MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }
_MONTHS = {v: k for k, v in MONTHS.items()}
MONTHS_ABBREV = '|' + '|'.join([_MONTHS[k] for k in sorted(_MONTHS.keys()) if k != '00']) + '|'


def days(begin_label, begin_dateiso, end_label, end_dateiso):
    if begin_dateiso is not None and end_dateiso is not None:
        errors = []
        errors.extend(is_fulldate(begin_label, begin_dateiso))
        errors.extend(is_fulldate(end_label, end_dateiso))
        if len(errors) == 0:
            return (dateiso2datetime(end_dateiso) - dateiso2datetime(begin_dateiso)).days


def is_fulldate(label, dateiso):
    y, m, d = dateiso[0:4], dateiso[4:6], dateiso[6:8]
    y = int(dateiso[0:4]) if y.isdigit() else 0
    m = int(dateiso[4:6]) if m.isdigit() else 0
    d = int(dateiso[6:8]) if d.isdigit() else 0
    msg = []
    if not y > 0:
        msg.append(_('{value} is an invalid value for {label}. ').format(value=y, label='year (' + label + ')'))
    if not 0 < m <= 12:
        msg.append(_('{value} is an invalid value for {label}. ').format(value=m, label='month (' + label + ')'))
    if not d <= 31:
        msg.append(_('{value} is an invalid value for {label}. ').format(value=d, label='day (' + label + ')'))
    if len(msg) == 0:
        try:
            r = datetime(y, m, d)
        except:
            msg.append(_('{value} is an invalid value for {label}. ').format(value=d, label=label + ': day '))
    return msg


def dateiso2datetime(dateiso):
    r = None
    if dateiso is not None:
        dateiso = dateiso + '0'*8
        dateiso = dateiso[0:8]
        y = int(dateiso[0:4])
        m = int(dateiso[4:6])
        d = int(dateiso[6:8])
        if y == 0:
            y = 1
        if d == 0:
            d = 1
        if m == 0:
            m = 1
        r = datetime(y, m, d)
    return r


def format_dateiso_from_date(year, month, day):
    return year + month + day


def format_dateiso(adate):
    if adate is not None:
        month = adate.get('season')
        if month is None:
            month = adate.get('month')
        if month is None:
            month = '00'
        else:
            if '-' in month:
                month = month[month.find('-')+1:]
            if not month.isdigit():
                month = MONTHS.get(month, '00')
            month = '00' + month
            month = month[-2:]
        y = adate.get('year', '0000')
        if y is None:
            y = '0000'
        d = adate.get('day', '00')
        if d is None:
            d = '00'
        d = '00' + d
        d = d[-2:]
        return y + month + d


def format_date(dates):
    r = ''
    if dates is not None:
        r = ' '.join([k + ': ' + v for k, v in dates.items() if v is not None])
    return r


def four_digits_year(year):
    if year is not None:
        if not year.isdigit():
            if 's/d' not in year and 's.d' not in year:
                year = year.replace('/', '-')
                splited = None
                if '-' in year:
                    splited = year.split('-')
                elif ' ' in year:
                    splited = year.split(' ')
                if splited is None:
                    splited = [year]
                splited = [y for y in splited if len(y) == 4 and y.isdigit()]
                if len(splited) > 0:
                    year = splited[0]
        if len(year) > 4:
            if year[0:4].isdigit():
                year = year[0:4]
            elif year[1:5].isdigit():
                year = year[1:5]
    return year
