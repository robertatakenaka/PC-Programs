# coding=utf-8

from ...__init__ import _


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
