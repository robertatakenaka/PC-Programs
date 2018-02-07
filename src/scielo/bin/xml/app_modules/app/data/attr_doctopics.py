# coding=utf-8

from ...__init__ import _
from ...generics.reports import validation_status


DOCTOPIC = {
                'research-article': 'oa',
                'editorial': 'ed',
                'abstract': 'zz',
                'announcement': 'zz',
                'article-commentary': 'co',
                'case-report': 'cr',
                'letter': 'le',
                'review-article': 'ra',
                'rapid-communication': 'sc',
                'addendum': 'zz',
                'book-review': 'rc',
                'books-received': 'zz',
                'brief-report': 'rn',
                'calendar': 'zz',
                'clinical-trial': 'oa',
                'collection': 'zz',
                'correction': 'er',
                'discussion': 'ed',
                'dissertation': 'ed',
                'editorial-material': 'ed',
                'in-brief': 'pr',
                'introduction': 'ed',
                'meeting-report': 'zz',
                'news': 'zz',
                'obituary': 'zz',
                'oration': 'zz',
                'partial-retraction': 'partial-retraction',
                'product-review': 'zz',
                'reply': 'reply',
                'reprint': 'zz',
                'retraction': 're',
                'translation': 'zz',
                'technical-report': 'oa',
                'other': 'zz',
}

DOCTOPIC_IN_USE = [
    'article-commentary', 
    'book-review', 
    'brief-report', 
    'case-report', 
    'correction', 
    'editorial', 
    'in-brief', 
    'letter', 
    'other', 
    'rapid-communication', 
    'research-article', 
    'partial-retraction', 
    'retraction', 
    'reply', 
    'review-article', 
    ]

HISTORY_REQUIRED_FOR_DOCTOPIC = [
    'case-report', 
    'research-article',    
]

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
    'guideline',
    'oration',
    'discussion',
    'obituary',
    'reply',
]

AUTHORS_REQUIRED_FOR_DOCTOPIC = INDEXABLE

AUTHORS_NOT_REQUIRED_FOR_DOCTOPIC = [
    'correction',
    ]

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

REFS_REQUIRED_FOR_DOCTOPIC = [
    'brief-report', 
    'case-report', 
    'rapid-communication', 
    'research-article', 
    'review-article', 
    ]

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


related_articles_type = ['corrected-article', 'commentary-article', 'press-release', 'retracted-article']


def normalize_doctopic(_doctopic):
    r = DOCTOPIC.get(_doctopic)
    return _doctopic if r == '??' else r


def doctopic_label(code):
    label = [k for k, v in DOCTOPIC.items() if v == code]
    if len(label) == 0:
        label = None
    else:
        label = label[0]
    return label


def suggestions_of_article_type_by_section_title(section_title):
    suggestions = []
    if section_title is not None:
        lower_section_title = section_title.lower().strip()
        if 'retra' in lower_section_title:
            suggestions.append('retraction')
        elif 'abstract' in lower_section_title or 'resum' in lower_section_title:
            suggestions.append('abstract')
        elif 'book' in lower_section_title or 'resenha' in lower_section_title or u'reseñ' in lower_section_title:
            suggestions.append('book-review')
        elif 'brief report' in lower_section_title or ('pesquisa' in lower_section_title and 'nota' in lower_section_title) or ('research' in lower_section_title and 'note' in lower_section_title):
            suggestions.append('brief-report')
        elif 'case' in lower_section_title or 'caso' in lower_section_title:
            suggestions.append('case-report')
        elif 'correction' in lower_section_title or 'errat' in lower_section_title:
            suggestions.append('correction')
        elif 'carta' in lower_section_title or 'letter' in lower_section_title or 'reply' in lower_section_title or 'correspond' in lower_section_title:
            suggestions.append('letter')
        elif 'editoria' in lower_section_title:
            suggestions.append('editorial')
        elif 'interview' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'entrevista' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'point' in lower_section_title and 'view' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'ponto' in lower_section_title and 'vista' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'punto' in lower_section_title and 'vista' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'opini' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'communication' in lower_section_title or 'comunica' in lower_section_title:
            suggestions.append('rapid-communication')
        elif 'atualiza' in lower_section_title or 'actualiza' in lower_section_title or 'updat' in lower_section_title:
            suggestions.append('rapid-communication')
        elif 'art' in lower_section_title and 'origin' in lower_section_title:
            suggestions.append('research-article')
        elif 'review' in lower_section_title and 'article' in lower_section_title:
            suggestions.append('review-article')
        elif 'review' in lower_section_title and 'article' in lower_section_title:
            suggestions.append('review-article')
        elif 'revis' in lower_section_title and ('artigo' in lower_section_title or u'artículo' in lower_section_title):
            suggestions.append('review-article')
        elif ('tech' in lower_section_title and 'article' in lower_section_title) or (u'técnico' in lower_section_title and 'informe' in lower_section_title) or (u'técnico' in lower_section_title and u'relatório' in lower_section_title):
            suggestions.append('technical-report')
        elif 'comment' in lower_section_title or 'coment' in lower_section_title:
            suggestions.append('article-commentary')
        elif 'article' in lower_section_title or u'artículo' in lower_section_title or 'artigo' in lower_section_title:
            suggestions.append('research-article')
        elif 'original' in lower_section_title:
            suggestions.append('research-article')

    if 'editorial-material' in suggestions:
        suggestions = [item.replace('editorial-material', 'other') for item in suggestions]
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


# FIXME
def validate_article_type_and_section(article_type, article_section, has_abstract):
    results = []
    if article_type is None:
        article_type = 'None'
    if article_section is None:
        article_section = 'None'

    status = ''
    suggestions = suggestions_of_article_type_by_section_title(article_section)
    if article_type not in suggestions:
        suggestions_msg = ''
        status = validation_status.STATUS_ERROR
        if len(suggestions) == 0:
            status = validation_status.STATUS_WARNING
            if has_abstract is True:
                suggestions = ABSTRACT_REQUIRED_FOR_DOCTOPIC
            else:
                suggestions = [item for item in DOCTOPIC_IN_USE if item not in ABSTRACT_REQUIRED_FOR_DOCTOPIC]
    if article_type not in suggestions:
        suggestions_msg = _('{value} is an invalid value for {label}. ').format(value=article_type, label='@article-type') + _('Expected values: {expected}. ').format(expected=_(' or ').join(suggestions))
        results.append(('@article-type', status, _('Be sure that the elements {elem1} and {elem2} are properly identified. ').format(elem1='@article-type', elem2=_('section title') + '(' + article_section + ')') + suggestions_msg))

    return results
