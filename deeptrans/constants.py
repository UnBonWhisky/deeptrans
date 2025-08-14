LANGUAGES = {
    'ar': 'arabic',
    'bg': 'bulgarian',
    'cs': 'czech',
    'da': 'danish',
    'de': 'german',
    'el': 'greek',
    'en-us': 'english',
    'es': 'spanish',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'hu': 'hungarian',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'ko': 'korean',
    'lt': 'lithuanian',
    'lv': 'latvian',
    'nb': 'norwegian',
    'nl': 'dutch',
    'pl': 'polish',
    'pt-br': 'portuguese (brazil)',
    'pt-pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'sv': 'swedish',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'zh-hans': 'chinese (simplified)',
    'zh-hant': 'chinese (traditional)',
}

SOURCE_LANGUAGES = {
    'ar': 'arabic',
    'bg': 'bulgarian',
    'cs': 'czech',
    'da': 'danish',
    'de': 'german',
    'el': 'greek',
    'en': 'english',
    'es': 'spanish',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'hu': 'hungarian',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'ko': 'korean',
    'lt': 'lithuanian',
    'lv': 'latvian',
    'nb': 'norwegian',
    'nl': 'dutch',
    'pl': 'polish',
    
    'pt': 'portuguese (brazil)',
    'pt': 'portuguese',
    
    'ro': 'romanian',
    'ru': 'russian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'sv': 'swedish',
    'tr': 'turkish',
    'uk': 'ukrainian',
    
    'zh': 'chinese (simplified)',
    'zh': 'chinese (traditional)',
    'zh': 'chinese',
}

LANGKEYS = list(LANGUAGES.keys())
LANGNAMES = list(LANGUAGES.values())
SOURCE_LANGKEYS = list(SOURCE_LANGUAGES.keys())
SOURCE_LANGNAMES = list(SOURCE_LANGUAGES.values())

LANGCODES = dict(map(reversed, LANGUAGES.items()))
SOURCE_LANGCODES = dict(map(reversed, SOURCE_LANGUAGES.items()))