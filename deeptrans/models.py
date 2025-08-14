from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Formality(Enum):
    """
    Formality options for translation.
    
    Parameters:
        DEFAULT: Default formality.
        MORE: More formal translation.
        LESS: Less formal translation.
        PREFER_MORE: Prefer more formal translation if available.
        PREFER_LESS: Prefer less formal translation if available.
    """
    DEFAULT = "default"
    MORE = "more"
    LESS = "less"
    PREFER_MORE = "prefer_more"
    PREFER_LESS = "prefer_less"


class SplitSentences(Enum):
    """
    Options for sentence splitting.
    
    Parameters:
        ON: Split sentences automatically.
        OFF: Do not split sentences.
        NO_NEWLINES: Do not split sentences, but allow newlines.
    """
    ON = "1"
    OFF = "0"
    NO_NEWLINES = "nonewlines"


class ModelType(Enum):
    """
    Translation model types.
    
    Parameters:
        LATENCY_OPTIMIZED: Optimized for low latency.
        QUALITY_OPTIMIZED: Optimized for translation quality.
        PREFER_QUALITY_OPTIMIZED: Prefer quality optimized model if available.
    """
    LATENCY_OPTIMIZED = "latency_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    PREFER_QUALITY_OPTIMIZED = "prefer_quality_optimized"


@dataclass
class TextResult:
    """
    Result of a text translation.
    
    Attributes:
        text (str): Translated text.
        input (str): Original input text.
        src (str): Detected source language code.
        dest (str): Target language code.
        billed_characters (int, optional): Number of characters billed for this translation (if applicable).
        model_type_used (str, optional): Model type used for the translation (if applicable).
    """
    text: str
    input: str
    src: str
    dest: str
    billed_characters: Optional[int] = None
    model_type_used: Optional[str] = None


@dataclass
class Language:
    """
    Language information.
    
    Attributes:
        code (str): Language code (e.g., "EN", "FR").
        name (str): Language name (e.g., "English", "French").
        supports_formality (bool): Whether the language supports formality options.
    """
    code: str
    name: str
    supports_formality: bool = False


@dataclass
class Usage:
    """
    API usage information.
    
    Attributes:
        character_count (int): Number of characters used in the current billing period.
        character_limit (int): Maximum number of characters allowed in the current billing period.
    """
    character_count: int
    character_limit: int