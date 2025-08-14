LANGUAGES = {
    'ar': 'arabic',
    'bg': 'bulgarian',
    'zh-hans': 'chinese (simplified)',
    'zh-hant': 'chinese (traditional)',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en-us': 'english',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'hu': 'hungarian',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'ko': 'korean',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'nb': 'norwegian',
    'pl': 'polish',
    'pt-pt': 'portuguese',
    'pt-br': 'portuguese (brazil)',
    'ro': 'romanian',
    'ru': 'russian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish',
    'uk': 'ukrainian',
}

SOURCE_LANGUAGES = {
    'ar': 'arabic',
    'bg': 'bulgarian',
    
    'zh': 'chinese (simplified)',
    'zh': 'chinese (traditional)',
    'zh': 'chinese',
    
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'hu': 'hungarian',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'ko': 'korean',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'nb': 'norwegian',
    'pl': 'polish',
    
    'pt': 'portuguese',
    'pt': 'portuguese (brazil)',
    
    'ro': 'romanian',
    'ru': 'russian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish',
    'uk': 'ukrainian',
}

LANGKEYS = list(LANGUAGES.keys())
LANGNAMES = list(LANGUAGES.values())
SOURCE_LANGKEYS = list(SOURCE_LANGUAGES.keys())
SOURCE_LANGNAMES = list(SOURCE_LANGUAGES.values())

LANGCODES = dict(map(reversed, LANGUAGES.items()))
SOURCE_LANGCODES = dict(map(reversed, SOURCE_LANGUAGES.items()))