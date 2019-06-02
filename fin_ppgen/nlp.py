"""
This module contains NLP functions for processing strings read from the
Kotus word list into lexical representations and into final word forms.
"""

import os.path

import re
import secrets


# This approach of handling the necessary regex functions by using closures
# to dynamically build the functions is taken from Dive into Python 3
# by Mark Pilgrim (see http://www.diveintopython3.net/generators.html)
def build_inflect_functions(pattern, search, replace):
    """Dynamically build regex search and replace functions."""

    def match_rule(word):
        return re.search(pattern, word)

    def inflect_rule(word):
        return re.sub(search, replace, word)

    return (match_rule, inflect_rule)


def initialize_rules(pattern_file):
    """A helper function for extracting regex search and replace rules
       from an external file."""

    rules = []
    with open(pattern_file, encoding='utf-8') as fp:
        for line in fp:
            if line[0] in ['#', '\n', '\r']:  # skip comments and empty lines
                continue
            pattern, search, replace = line.split(None, 3)
            rules.append(build_inflect_functions(pattern, search, replace))

    return rules


# Sets for noun endings
GRAM_NUMBER = ['+Sg', '+Pl']
INFLECTIONS = [
    '+Nom', '+Gen', '+Par', '+Ine', '+Ela', '+Ill', '+Ade', '+Abl', '+All',
    '+Ess', '+Tra'
]
CLITICS = ['', 'hAn', 'kin', 'kO', 'pA', 'pAs']
# Regex match and replace rules
FPATH = os.path.dirname(__file__)
GRADATION_RULES = initialize_rules(
    os.path.join(FPATH, '../lang_data/gradation-patterns.txt'))
INFLECTION_RULES = initialize_rules(
    os.path.join(FPATH, '../lang_data/inflection-patterns.txt'))


def prepend_lexical_info(wordlist):
    """
    Prepend all noun entries in the list with their inflection
    and gradation paradigms. Return the entries as a list.

    If a word in the list contains spaces, the spaces are replaced with
    underscores (_).
    """

    print("Composing noun entries...")
    words_with_lex = []
    for word_entry in wordlist:
        # replace spaces with underscores to simplify later regexes
        word = word_entry.s.string.replace(' ', '_')
        infl_paradigm = 'N'
        grad_paradigm = ''
        if word_entry.t is not None:
            infl_paradigm += word_entry.t.tn.string
        if word_entry.av is not None:
            grad_paradigm = word_entry.av.string
        word = '<' + infl_paradigm + grad_paradigm + '>' + word
        words_with_lex.append(word)

    return words_with_lex


def generate_lexical_forms(wordlist):
    return [attach_noun_endings(word) for word in wordlist]


def attach_noun_endings(noun):
    """Attach random number, inflection, and clitic endings to a noun."""
    number = secrets.choice(GRAM_NUMBER)
    inflection = secrets.choice(INFLECTIONS)
    # Note: clitic particles are turned off.
    # clitic = secrets.choice(CLITICS)
    noun = noun + number + inflection

    return noun


def gradate(word):
    """Check if a word matches any gradation patterns: if yes, return the word
       with gradation replace rules applied. If not, return the original word
       in order to avoid returning None values."""
    for match_rule, grad_rule in GRADATION_RULES:
        if match_rule(word):
            return grad_rule(word)

    return word


def inflect(word):
    """Check if a word matches any inflection patterns: if yes, return the word
       with inflection replace rules applied. If not, return the original word
       in order to avoid returning None values."""
    for match_rule, inflect_rule in INFLECTION_RULES:
        if match_rule(word):
            return inflect_rule(word)

    return word


def convert_to_lexical_plural(word):
    """Helper function for ensuring that words only appearing in the
       plural form (such as 'aivot' or 'häät') are lexically represented
       as plural."""
    return re.sub(r't\+Sg', r'+Pl', word)


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
        cleaned = re.sub(r'\<N\d+[A-M]?\>', '', inflected)
        cleaned = re.sub('_', ' ', cleaned)
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
def back_vowel_determines_harmony(word):
    """A simplistic algorithm for determining the vowel harmony
       of a word."""
    for c in word[::-1]:
        if c in 'äö':
            return False
        if c in 'aou':
            return True


def replace_i_with_j(word):
    return re.sub(r'(\w)aia', r'\1aja', word)


def apply_other_transformations(wordlist):
    words = []
    for word in wordlist:
        if re.search(r'[^t]aia', word):
            word = replace_i_with_j(word)
        words.append(word)

    return words
