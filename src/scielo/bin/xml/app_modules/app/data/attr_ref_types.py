# coding=utf-8


BIBLIOMETRICS_USE = ['journal', 'book', 'thesis', 'confproc']

scholars_level1 = ['journal', 'book']
scholars_level2 = ['thesis', 'confproc']

PUBLICATION_TYPE = []
PUBLICATION_TYPE.append('journal')
PUBLICATION_TYPE.append('book')
PUBLICATION_TYPE.append('thesis')
PUBLICATION_TYPE.append('patent')
PUBLICATION_TYPE.append('report')
PUBLICATION_TYPE.append('software')
PUBLICATION_TYPE.append('webpage')
PUBLICATION_TYPE.append('database')
PUBLICATION_TYPE.append('confproc')
PUBLICATION_TYPE.append('legal-doc')
PUBLICATION_TYPE.append('newspaper')
PUBLICATION_TYPE.append('other')


REFERENCE_REQUIRED_SUBELEMENTS = {}
REFERENCE_REQUIRED_SUBELEMENTS['journal'] = ['article-title', 'person-group', 'year', 'source']
REFERENCE_REQUIRED_SUBELEMENTS['book'] = ['year', 'source']
REFERENCE_REQUIRED_SUBELEMENTS['confproc'] = ['conf-name', 'source', 'year']
REFERENCE_REQUIRED_SUBELEMENTS['thesis'] = ['comment', 'source', 'year']
REFERENCE_REQUIRED_SUBELEMENTS['webpage'] = ['ext-link', 'date-in-citation[@content-type="access-date"]']


REFERENCE_NOT_ALLOWED_SUBELEMENTS = {}
REFERENCE_NOT_ALLOWED_SUBELEMENTS['journal'] = ['chapter-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['book'] = ['article-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['thesis'] = ['article-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['confproc'] = ['chapter-title', 'patent']
