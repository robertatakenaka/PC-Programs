# coding=utf-8

from datetime import datetime

from ...generics import date_utils
from ...generics.reports import html_reports


SPS_expiration_dates = [
    ('sps-1.8', ['20180401', '20190401']),
    ('sps-1.7', ['20171001', '20181001']),
    ('sps-1.6', ['20170401', '20180401']),
    ('sps-1.5', ['20161001', '20171001']),
    ('sps-1.4', ['20160401', '20170401']),
    ('sps-1.3', ['20150901', '20160901']),
    ('sps-1.2', ['20150301', '20160301']),
    ('sps-1.1', ['20140901', '20150901']),
    ('sps-1.0', ['20140301', '20150301']),
    ('None', ['00000000', '20140901']),
]

dict_SPS_expiration_dates = dict(SPS_expiration_dates)

SPS_HELP_ELEMENTS = [
    'abbrev-journal-title',
    'abstract',
    'ack',
    'addr-line',
    'aff',
    'app',
    'article-categories',
    'article-id',
    'article-meta',
    'article-title',
    'article',
    'attrib',
    'author-notes',
    'award-group',
    'award-id',
    'back',
    'body',
    'boxed-text',
    'caption',
    'chapter-title',
    'collab',
    'comment',
    'conf-date',
    'conf-loc',
    'conf-name',
    'contrib-group',
    'contrib-id',
    'contrib',
    'copyright-holder',
    'copyright-statement',
    'copyright-year',
    'corresp',
    'country',
    'counts',
    'date-in-citation',
    'date',
    'day',
    'def-list',
    'disp-formula',
    'disp-quote',
    'edition',
    'element-citation',
    'elocation-id',
    'email',
    'etal',
    'ext-link',
    'fig',
    'fn-group',
    'fn',
    'fpage',
    'front-stub',
    'front',
    'funding-group',
    'funding-source',
    'funding-statement',
    'given-names',
    'glossary',
    'history',
    'inline-formula',
    'inline-graphic',
    'inline-supplementary-material',
    'institution',
    'isbn',
    'issn',
    'issue',
    'journal-id',
    'journal-meta',
    'journal-title-group',
    'journal-title',
    'kwd-group',
    'kwd',
    'label',
    'license',
    'list',
    'lpage',
    'media',
    'mixed-citation',
    'month',
    'name',
    'named-content',
    'on-behalf-of',
    'p',
    'page-range',
    'patent',
    'permissions',
    'person-group',
    'prefix',
    'product',
    'pub-date',
    'pub-id',
    'publisher-loc',
    'publisher-name',
    'publisher',
    'ref-list',
    'ref',
    'related-article',
    'response',
    'role',
    'season',
    'sec',
    'sig-block',
    'size',
    'source',
    'sub-article',
    'subj-group',
    'suffix',
    'supplementary-material',
    'surname',
    'table-wrap-foot',
    'table-wrap',
    'table',
    'title-group',
    'trans-abstract',
    'trans-title-group',
    'trans-title',
    'verse-group',
    'volume',
    'xref',
    'year',
]


def expected_sps_versions(article_dateiso):
    if article_dateiso <= SPS_expiration_dates[-1][1][0]:
        # qualquer versao
        return [item[0] for item in SPS_expiration_dates]

    valid_versions = []
    for version, dates in SPS_expiration_dates:
        if dates[0] <= article_dateiso <= dates[1]:
            valid_versions.append(version)
    return valid_versions


def sps_current_versions():
    return [item[0] for item in SPS_expiration_dates[:2]]


def sps_version_expiration_days(sps_version):
    days = None
    sps_dates = dict_SPS_expiration_dates.get(sps_version)
    if sps_dates is not None:
        sps_dates = date_utils.dateiso2datetime(sps_dates[1])
        now = datetime.now()
        diff = sps_dates - now
        days = diff.days
    return days


def sps_help(label):
    r = label
    href = 'https://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/latest/'
    element_name = label
    if element_name not in SPS_HELP_ELEMENTS and ' ' in element_name:
        element_name = element_name[:element_name.find(' ')]
    if element_name in SPS_HELP_ELEMENTS:
        href += 'tagset/elemento-{element_name}.html'.format(element_name=element_name)
    elif ' ' not in label:
        href += u'/search.html?q={element_name}&check_keywords=yes&area=default'.format(element_name=element_name)
    r += ' ' + html_reports.link(href, '[?]')
    return r
