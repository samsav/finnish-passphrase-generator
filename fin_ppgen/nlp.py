"""
This module contains NLP functions for processing strings read from the
Kotus word list into lexical representations and into final word forms.
"""

from pathlib import Path
from helpers import initialize_rules

import re
import secrets


# Sets for noun endings
# Grammatical number: singular or plural
GRAM_NUMBER: list[str] = ['+Sg', '+Pl']
# The accusative, comitative, and instructive case are not included since their use is more restricted.
INFLECTIONS: list[str] = [
    '+Nom', '+Gen', '+Par', '+Ine', '+Ela', '+Ill', '+Ade', '+Abl', '+All',
    '+Ess', '+Tra'
]
# Clitic particles. See clitics in VISK: https://scripta.kotus.fi/visk/sisallys.php?p=126
CLITICS: list[str] = ['kO', 'pA', 'kAAn', 'hAn', 'kin']

# Paths for the current file and the language data folder
FILE_PATH = Path(__file__).resolve()
LANG_DATA_PATH = FILE_PATH.parent / 'lang_data'

# Regex match and replace rules
GRADATION_RULES = initialize_rules(
    LANG_DATA_PATH / 'gradation-patterns.txt')
INFLECTION_RULES = initialize_rules(
    LANG_DATA_PATH / 'inflection-patterns.txt')


def prepend_lexical_info(word: str, data: dict[str, list[str]]) -> str:
    # replace spaces with underscores to simplify later regexes
    word: str = word.replace(' ', '_')
    if data['inflection'][0] is not None:
        inflection: str = secrets.choice(data['inflection'])  # Some words have alternative inflection paradigms
        gradation: str = ''
        if '*' in inflection:
            inflection, gradation = inflection.split('*')
    
    return '<' + inflection + gradation + '>' + word


def randomize_clitics(p1: int = 10, p2: int = 10) -> str:
    clitics = []
    if secrets.randbelow(100) < p1:
        clitics.append(secrets.choice(CLITICS))
        if secrets.randbelow(100) < p2:
            # TODO: finish working out clitic combinations
            match clitics:
                case ['hAn']:
                    clitics.append(secrets.choice(['kin', 'pAs']))
                case ['kin']:
                    clitics.append('kO')
    return ''.join(c for c in clitics)


def attach_noun_endings(word: str) -> str:
    """Attach random grammatical number, inflection, and clitic endings to a noun."""
    grammatical_number: str = secrets.choice(GRAM_NUMBER)
    inflection: str = secrets.choice(INFLECTIONS)
    clitics: str = randomize_clitics()
    return word + grammatical_number + inflection + clitics


def attach_verb_endings(word: str) -> str:
    return ''


def gradate(word: str) -> str:
    """Check if a word matches any gradation patterns: if yes, return the word
       with gradation replace rules applied. If not, return the original word
       in order to avoid returning None values."""
    for match_rule, gradation_rule in GRADATION_RULES:
        if match_rule(word):
            return gradation_rule(word)

    return word


def inflect(word: str) -> str:
    """Check if a word matches any inflection patterns: if yes, return the word
       with inflection replace rules applied. If not, return the original word
       in order to avoid returning None values."""
    for match_rule, inflect_rule in INFLECTION_RULES:
        if match_rule(word):
            return inflect_rule(word)

    return word


def convert_to_lexical_plural(word: str) -> str:
    """Helper function for ensuring that words only appearing in the
       plural form (such as 'aivot' or 'häät') are lexically represented
       as plural."""
    return re.sub(r't\+Sg', r'+Pl', word)


def remove_lexical_prefix(word: str) -> str:
    """
    Removes lexical prefixes from a word.

    Lexical prefixes are represented as a sequence of an uppercase letter, one or more digits, and optionally
    another uppercase letter from 'A' to 'M' enclosed in elbow brackets. For example, <S5B>.
    This function removes any occurrences of such patterns from the word.

    Args:
        word (str): The word from which lexical prefixes need to be removed.

    Returns:
        str: The word with lexical prefixes removed.
    """
    return re.sub(r'\<N\d+[A-M]?\>', '', word)


def apply_consonant_gradation(wordlist):
    """Apply consonant gradation rules to a list of words and return
       the results in a list."""
    # TODO: after removing checking for plurals, rewrite as list comprehension
    gradated_words = []
    for word in wordlist:
        # TODO: move checking for plurals to a separate function
        if re.search(r't\+Sg', word) and '_' not in word:
            word = convert_to_lexical_plural(word)
        word = gradate(word)
        gradated_words.append(word)
    return gradated_words


def apply_inflection_rules(wordlist):
    """Apply inflection rules to a list of words and return
       the results in a list."""
    inflected_words = []
    for word in wordlist:
        inflected = inflect(word)
        # TODO: move cleanup to a separate function
        cleaned = re.sub('_', ' ', inflected)
        inflected_words.append(cleaned)
    return inflected_words


def apply_vowel_harmony(wordlist):
    """Apply vowel harmony transformations to a list of words
       and return the results in a list."""
    words_with_vowel_harmony = []
    for word in wordlist:
        if back_vowel_determines_harmony(word):
            words_with_vowel_harmony.append(
                word.translate(str.maketrans("AO", "ao")))
        else:
            words_with_vowel_harmony.append(
                word.translate(str.maketrans("AO", "äö")))
    return words_with_vowel_harmony


# The vowel harmony of loan words containing both back and front vowels
# is not entirely straightforward. The following way for determining
# vowel harmony is based on the rules in the article "Kompromisseja vai
# kompromissejä: vierassanojen taivutuspäätteen vokaali" by Sari Maamies.
#
# The algorithm below only implements the rules for non-compounded loan words,
# which also produce mostly the correct forms of non-compounded non-loan words.
def back_vowel_determines_harmony(word: str) -> bool:
    """A simplistic algorithm for determining the vowel harmony
       of a word."""
    for c in word[::-1]:
        if c in 'äö':
            return False
        if c in 'aou':
            return True


def replace_i_with_j(word: str) -> str:
    return re.sub(r'(\w)aia', r'\1aja', word)


def apply_other_transformations(wordlist):
    words = []
    for word in wordlist:
        if re.search(r'[^t]aia', word):
            word = replace_i_with_j(word)
        words.append(word)

    return words


def kaikkikotona(nouns):
    nouns = prepend_lexical_info(nouns)
    nouns[0] = nouns[0] + "+Pl" + "+Nom"
    nouns[1] = nouns[1] + "+Sg" + "+Ine"
    nouns = apply_consonant_gradation(nouns)
    nouns = apply_inflection_rules(nouns)
    nouns = apply_other_transformations(nouns)
    nouns = apply_vowel_harmony(nouns)

    return f"Ei ole kaikki {nouns[0]} {nouns[1]}"
