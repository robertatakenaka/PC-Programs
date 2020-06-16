# coding=utf-8

from prodtools import _
from prodtools import TABLES_PATH
from prodtools.utils import utils
from prodtools.utils.fs_utils import read_file
from prodtools.reports import validation_status
from prodtools.reports import html_reports


REFTYPE_AND_TAG_ITEMS = {'aff': ['aff'], 'app': ['app'], 'author-notes': ['fn'], 'bibr': ['ref'], 'boxed-text': ['boxed-text'], 'contrib': ['fn'], 'corresp': ['corresp'], 'disp-formula': ['disp-formula'], 
            'fig': ['fig', 'fig-group'], 
            'fn': ['fn'], 'list': ['list'], 'other': ['?'], 'supplementary-material': ['supplementary-material'], 
            'table': ['table-wrap', 'table-wrap-group']
            }

DOCTOPIC = {
                'research-article': 'oa',
                'editorial': 'ed',
                'abstract': 'ab',
                'announcement': 'an',
                'article-commentary': 'co',
                'case-report': 'cr',
                'letter': 'le',
                'review-article': 'ra',
                'rapid-communication': 'sc',
                'addendum': 'addendum',
                'book-review': 'rc',
                'books-received': 'books-received',
                'brief-report': 'rn',
                'calendar': 'calendar',
                'clinical-trial': 'oa',
                'collection': 'zz',
                'correction': 'er',
                'discussion': 'discussion',
                'dissertation': 'dissertation',
                'editorial-material': 'ed',
                'in-brief': 'pr',
                'introduction': 'ed',
                'meeting-report': 'meeting-report',
                'news': 'news',
                'obituary': 'obituary',
                'oration': 'oration',
                'partial-retraction': 'partial-retraction',
                'product-review': 'product-review',
                'reply': 'reply',
                'reprint': 'reprint',
                'retraction': 're',
                'translation': 'translation',
                'technical-report': 'oa',
                'other': 'zz',
                'guideline': 'guideline',
                'interview': 'in',
                'data-article': 'data-article',
}

DOCTOPIC_IN_USE = DOCTOPIC.keys()

PEER_REVIEW_DOCTOPICS = [
    'aggregated-review-documents',
    'referee-report',
    'editor-report',
    'author-comment',
    'community-comment',
    'recommendation',
]

PEER_REVIEW_CONTRIB_ROLES_FOR_ANON = [
    'reviewer',
    'reader',
    'author',
    'editor',
]

# para todos INDEXABLE exigir aff, contrib, xref, ref
INDEXABLE = [
    'research-article',
    'article-commentary',
    'rapid-communication',
    'brief-report',
    'case-report',
    'correction',
    'editorial',
    'interview',
    'letter',
    'other',
    'retraction',
    'partial-retraction',
    'review-article',
    'book-review',
    'addendum',
    'guidelines',
    'oration',
    'discussion',
    'obituary',
    'reply',
    'data-article',
    'aggregated-review-documents',
]

# para todos INDEXABLE_WITH_FLEXIBLE_REQUIREMENTS exigir aff?, contrib?, xref?, ref?
INDEXABLE_WITH_FLEXIBLE_REQUIREMENTS = {
    'editorial': ['aff', 'contrib'],
}

INDEXABLE_AND_DONT_REQUIRE_CONTRIB_AFF_XREF_REF = [
    'correction',
    'retraction',
    'partial-retraction',
    'other',
]

HISTORY_REQUIRED_FOR_DOCTOPIC = [
    'case-report', 
    'research-article',    
]

AUTHORS_REQUIRED_FOR_DOCTOPIC = list(set(INDEXABLE)-set(INDEXABLE_AND_DONT_REQUIRE_CONTRIB_AFF_XREF_REF))

AUTHORS_NOT_REQUIRED_FOR_DOCTOPIC = INDEXABLE_AND_DONT_REQUIRE_CONTRIB_AFF_XREF_REF

ABSTRACT_REQUIRED_FOR_DOCTOPIC = [
    'brief-report', 
    'case-report', 
    'research-article', 
    'review-article', 
    ]

ABSTRACT_UNEXPECTED_FOR_DOCTOPIC = [
    'editorial', 
    'in-brief', 
    'letter', 
    'other', 
    ]

REFS_REQUIRED_FOR_DOCTOPIC = list(
    set(INDEXABLE) -
    set(INDEXABLE_AND_DONT_REQUIRE_CONTRIB_AFF_XREF_REF) -
    {'editorial'})

TOC_SECTIONS = { 
    u'carta': u'letter', 
    u'revisão': u'review', 
    u'resenha': u'review', 
    u'reseña': u'review', 
    u'origin': u'research', 
    u'informe': u'report', 
    u'revisión': u'review', 
    u'relato': u'report', 
    u'artigo': u'article', 
    u'artículo': u'article', 
    u'errata': u'correction', 
    u'erratum': u'correction'
}


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


BIBLIOMETRICS_USE = ['journal', 'book', 'thesis', 'confproc']

scholars_level1 = ['journal', 'book']
scholars_level2 = ['thesis', 'confproc']

PUBLICATION_TYPE = []
PUBLICATION_TYPE.append('journal')
PUBLICATION_TYPE.append('book')
PUBLICATION_TYPE.append('thesis')
PUBLICATION_TYPE.append('data')
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
REFERENCE_REQUIRED_SUBELEMENTS['data'] = ['year', 'pub-id[@pub-id-type="art-access-id"] or ext-link']


REFERENCE_NOT_ALLOWED_SUBELEMENTS = {}
REFERENCE_NOT_ALLOWED_SUBELEMENTS['journal'] = ['chapter-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['book'] = ['article-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['thesis'] = ['article-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['confproc'] = ['chapter-title', 'patent']

LANGUAGES = {
    'en': _('English'),
    'pt': _('Portuguese'),
    'es': _('Spanish'),
    'af': _('Afrikaans'),
    'ar': _('Arabic'),
    'bg': _('Bulgarian'),
    'zh': _('Chinese'),
    'cs': _('Czech'),
    'da': _('Danish'),
    'nl': _('Dutch'),
    'eo': _('Esperanto'),
    'fr': _('French'),
    'de': _('German'),
    'gr': _('Greek'),
    'he': _('Hebrew'),
    'hi': _('Hindi'),
    'hu': _('Hungarian'),
    'in': _('Indonesian'),
    'ia': _('Interlingua'),
    'ie': _('Interlingue'),
    'it': _('Italian'),
    'ja': _('Japanese'),
    'ko': _('Korean'),
    'la': _('Latin'),
    'no': _('Norwergian'),
    'pl': _('Polish'),
    'ro': _('Romanian'),
    'ru': _('Russian'),
    'sa': _('Sanskrit'),
    'sh': _('Serbo-Croat'),
    'sk': _('Slovak'),
    'sn': _('Slovenian'),
    'sv': _('Swedish'),
    'tr': _('Turkish'),
    'uk': _('Ukrainian'),
    'ur': _('Urdu'),
    'zz': _('Other'),
    'gl': _('Galician'),
    'eu': _('Basque'),
    'ca': _('Catalan'),
}


COUNTRY_CODES = [
 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 
 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 
 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 
 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 
 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 
 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 
 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 
 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 
 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 
 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 
 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 
 'KV',
 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 
 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 
 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 
 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 
 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 
 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 
 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 
 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 
 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 
 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW',
 ]

PERMISSION_ELEMENTS = ['license', 'copyright-holder', 'copyright-year', 'copyright-statement']

related_articles_type = ['corrected-article', 'commentary-article', 'press-release', 'retracted-article']

CONTRIB_ID_URLS = {
    'lattes': 'https://lattes.cnpq.br/',
    'orcid': 'https://orcid.org/',
    'researchid': 'https://www.researcherid.com/rid/',
    'scopus': 'https://www.scopus.com/authid/detail.uri?authorId=',
}


LICENSES = read_file(TABLES_PATH + '/licenses.csv')
if LICENSES is None:
    LICENSES = []
else:
    LICENSES = LICENSES.split()


LICENSE_TEXTS = {
    'pt': u'Este é um artigo publicado em acesso aberto sob uma '
            u'licença Creative Commons',
    'en': u'This is an article published in open access under a '
            'Creative Commons license',
    'es': u'Este es un artículo publicado en acceso abierto bajo una '
            u'licencia Creative Commons',
}

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


def normalize_doctopic(_doctopic):
    r = DOCTOPIC.get(_doctopic)
    return _doctopic if r == '??' else r


def normalize_role(_role):
    r = ROLE.get(_role)
    if r == '??' or _role is None or r is None:
        r = 'ND'
    return r


def doctopic_label(code):
    label = [k for k, v in DOCTOPIC.items() if v == code]
    if len(label) == 0:
        label = None
    else:
        label = label[0]
    return label


def deduce_article_type_from_article_section(section_title):
    section_title_vs_article_type = dict([
        ('original', 'research-article'),
        ('article', 'research-article'),
        ('artículo', 'research-article'),
        ('artigo', 'research-article'),
        ('relatório técnico', 'research-article'),
        ('informe técnico', 'research-article'),
        ('technical report', 'research-article'),
        ('comment', 'article-commentary'),
        ('coment', 'article-commentary'),
        ('updat', 'rapid-communication'),
        ('actualiza', 'rapid-communication'),
        ('atualiza', 'rapid-communication'),
        ('comunica', 'rapid-communication'),
        ('communica', 'rapid-communication'),
        ('brief report', 'brief-report'),
        ('nota de pesquisa', 'brief-report'),
        ('nota de investigación', 'brief-report'),
        ('research note', 'brief-report'),
        ('informe de caso', 'case-report'),
        ('relato de caso', 'case-report'),
        ('case report', 'case-report'),
        ('errata', 'correction'),
        ('erratum', 'correction'),
        ('interview', 'other'),
        ('point-of-view', 'editorial'),
        ('entrevista', 'other'),
        ('punto de vista', 'editorial'),
        ('ponto de vista', 'editorial'),
        ('letter', 'letter'),
        ('carta', 'letter'),
        ('reply', 'letter'),
        ('correspond', 'letter'),
        ('retraction', 'retraction'),
        ('retratación', 'retraction'),
        ('retractación', 'retraction'),
        ('retratação', 'retraction'),
        ('book review', 'book-review'),
        ('reseña', 'book-review'),
        ('resenha', 'book-review'),
        ('review', 'review-article'),
        ('revisão', 'review-article'),
        ('revisión', 'review-article'),
        ('resum', 'abstract'),
        ('parecer', 'aggregated-review-documents'),
        ('peer review', 'aggregated-review-documents'),
    ])

    suggestions = []
    if section_title is not None:
        lower_section_title = section_title.lower().strip()
        most_common_titles = (INDEXABLE +
                              list(section_title_vs_article_type.keys()))
        similarity = utils.similarity(most_common_titles, lower_section_title)
        highiest_rate, items = utils.most_similar(similarity)
        if highiest_rate > 0.8:
            suggestions = items
    return suggestions


def normalize_section_title(text):
    if text is None:
        text = ''

    text = text.lower().replace('-', ' ')
    text = text.replace('update article', 'rapid communication')
    text = text.replace(u'artículo de actualización', 'rapid communication')
    text = text.replace(u'artigo de atualização', 'rapid communication')
    text = text.replace(u'comunicação breve', 'rapid communication')
    text = text.replace(u'comunicación breve', 'rapid communication')
    text = text.replace(u'nota técnica', 'brief report')
    text = text.replace(u'nota de pesquisa', 'brief report')
    text = text.replace(u'nota de investigación', 'brief report')
    text = text.replace(u'research note', 'brief report')
    text = text.replace(u'relato breve', 'brief report')
    text = text.replace(u'informe breve', 'brief report')

    text = ' '.join([item for item in text.split(' ') if len(item) > 2])

    text = ' '.join([item for item in sorted(text.split(' '))])
    if text is not None:
        for term, transl in TOC_SECTIONS.items():
            text = text.replace(term, transl)
    return text


def translate_code_languages(lang_items):
    items = []
    for item in lang_items:
        items.append(LANGUAGES.get(item))
    return [item for item in items if item is not None]


def check_lang(lang):
    if lang in LANGUAGES.keys():
        return (True, LANGUAGES.get(lang))
    else:
        return (False, _('{value} is an invalid value for {label}. ').format(value=lang, label='@xml:lang') + _('Expected values: {expected}. ').format(expected=', '.join(sorted(LANGUAGES.keys())) + '. ' + ' | '.join(sorted([k + '(' + v + ')' for k, v in LANGUAGES.items()]))))


def validate_article_type_and_section(article_type, article_section, has_abstract):
    results = []

    article_type = article_type or ''
    article_section = article_section or ''
    if article_type == article_section:
        return results

    suggestions = deduce_article_type_from_article_section(article_section)

    if article_type in suggestions:
        return results

    if len(suggestions) > 0:
        status = validation_status.STATUS_ERROR
    else:
        status = validation_status.STATUS_WARNING
        if has_abstract is True:
            suggestions = ABSTRACT_REQUIRED_FOR_DOCTOPIC
        else:
            suggestions = [item
                           for item in DOCTOPIC_IN_USE
                           if item not in ABSTRACT_REQUIRED_FOR_DOCTOPIC]

    if article_type not in suggestions:
        suggestions_msg = _('Maybe {} is not a valid value for {}. ').format(
            article_type,
            '@article-type')
        suggestions_msg += _('Suggested values: {}. ').format(
            _(' or ').join(suggestions))
        elem1 = '@article-type' + ' ({}) '.format(article_type)
        elem2 = 'subject' + ' (' + article_section + ')'
        msg = _('Be sure that the elements {elem1} and {elem2} '
                'are properly identified. ').format(
                    elem1=elem1, elem2=elem2)
        results.append(('@article-type', status, msg + suggestions_msg))
    return results


def validate_iso_country_code(iso_country_code):
    r = []
    if iso_country_code is None:
        r.append(('aff/country/@country', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='aff/country/@country')))
    else:
        if iso_country_code not in COUNTRY_CODES:
            r.append(('aff/country/@country', validation_status.STATUS_FATAL_ERROR, 
                _('{value} is an invalid value for {label}. ').format(value=iso_country_code, label='aff/country/@country') + _('Expected values: {expected}. ').format(expected=' | '.join(COUNTRY_CODES))))
    return r


def validate_license_href(license_href):
    result = None
    if license_href is None:
        result = ('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='license/@href'))
    elif license_href in LICENSES or license_href + '/' in LICENSES:
        result = ('license/@xlink:href', validation_status.STATUS_VALID, license_href)
    else:
        result = ('license/@xlink:href', validation_status.STATUS_WARNING, _('{value} is an invalid value for {label}. ').format(value=license_href, label='license/@href') + _('Expected values: {expected}. ').format(expected=_(' or ').join(LICENSES)))
        #if not ws_requester.wsr.is_valid_url(license_href):
        #    result = ('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('{value} is an invalid value for {label}. ').format(value=license_href, label='license/@href'))
    return result


def sps_help(label):
    r = label
    docs_website_url = 'docs.scielo.org'
    docs_website_url = 'scielo.readthedocs.io'

    href = 'https://{}/projects/scielo-publishing-schema/pt_BR/latest/'.format(docs_website_url)
    element_name = label
    if element_name not in SPS_HELP_ELEMENTS and ' ' in element_name:
        element_name = element_name[:element_name.find(' ')]
    if element_name in SPS_HELP_ELEMENTS:
        href += 'tagset/elemento-{element_name}.html'.format(element_name=element_name)
    elif ' ' not in label:
        href += u'/search.html?q={element_name}&check_keywords=yes&area=default'.format(element_name=element_name)
    r += ' ' + html_reports.link(href, '[?]')
    return r
