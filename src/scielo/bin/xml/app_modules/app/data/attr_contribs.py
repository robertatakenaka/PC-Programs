# coding=utf-8


ROLE = {
    'author': 'ND',
    'editor': 'ED',
    'assignee': 'assignee',
    'compiler': 'compiler',
    'director': 'director',
    'guest-editor': 'guest-editor',
    'inventor': 'inventor',
    'transed': 'transed',
    'translator': 'TR',    
}


CONTRIB_ID_URLS = {
    'lattes': 'https://lattes.cnpq.br/',
    'orcid': 'https://orcid.org/',
    'researchid': 'https://www.researcherid.com/rid/',
    'scopus': 'https://www.scopus.com/authid/detail.uri?authorId=',
}


SUFFIX_LIST = [u'Netto',
               u'Nieto',
               u'Sobrino',
               u'Hijo',
               u'Neto',
               u'Sobrinho',
               u'Filho',
               u'Júnior',
               u'Junior',
               u'Senior',
               'Jr.',
               'Jr',
               'Sr',
               ]


def identified_suffixes():
    return SUFFIX_LIST + [item.upper() for item in SUFFIX_LIST]


def normalize_role(_role):
    r = ROLE.get(_role)
    if r == '??' or _role is None or r is None:
        r = 'ND'
    return r
