"""
This module contains NLP functions for turning processing strings read 
from the Kotus word list into lexical representations and into final word forms.
"""

import re
import secrets
from helpers import initialize_rules

# Sets for noun endings
GRAM_NUMBER = ['+Sg', '+Pl']
INFLECTIONS = [
    '+Nom', '+Gen', '+Par', '+Ine', '+Ela', '+Ill', '+Ade', '+Abl', '+All',
    '+Ess', '+Tra'
]
CLITICS = ['', 'hAn', 'kin', 'kO', 'pA', 'pAs']
# Regex match and replace rules
GRADATION_RULES = initialize_rules('gradation-patterns.txt')
INFLECTION_RULES = initialize_rules('inflection-patterns.txt')


def compose_nouns(word_list):
    """Prepend all noun entries in the list with their inflection
       and gradation paradigms. Return the entries as a list.
       
       If a word in the list contains spaces, the spaces are replaced with
       underscores (_)."""

    print("Composing noun entries...")
    nouns = []
    # TODO: separate prepending paradigms and attaching endings into different
    # functions? can list comprehensions be used here?
    for word_entry in word_list:
        # replace spaces with underscores to simplify later regexes
        word = word_entry.s.string.replace(' ', '_')
        infl_paradigm = 'N'
        grad_paradigm = ''
        if word_entry.t is not None:
            infl_paradigm += word_entry.t.tn.string
        if word_entry.av is not None:
            grad_paradigm = word_entry.av.string
        word = '<' + infl_paradigm + grad_paradigm + '>' + word
        word = attach_noun_endings(word)
        nouns.append(word)

    return nouns


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


def apply_consonant_gradation(word_list):
    """Apply consonant gradation rules to a list of words and return
       the results in a list."""
    # include a print statement for debugging
    print("\nApplying gradation rules to these lexical forms:")
    # TODO: after removing checking for plurals, rewrite as list comprehension
    gradated_words = []
    for word in word_list:
        print(word)
        # TODO: move checking for plurals to a separate function
        if re.search(r't\+Sg', word) and '_' not in word:
            word = convert_to_lexical_plural(word)
        word = gradate(word)
        gradated_words.append(word)
    return gradated_words


def apply_inflection_rules(word_list):
    """Apply inflection rules to a list of words and return
       the results in a list."""
    # include a print statement for debugging
    print("\nApplying inflection rules to these lexical forms:")
    inflected_words = []
    for word in word_list:
        print(word)
        inflected = inflect(word)
        # TODO: move cleanup to a separate function
        cleaned = re.sub(r'\<N\d+[A-M]?\>', '', inflected)
        cleaned = re.sub('_', ' ', cleaned)
        inflected_words.append(cleaned)
    return inflected_words


def apply_vowel_harmony(word_list):
    """Apply vowel harmony transformations to a list of words
       and return the results in a list."""
    # include a print statement for debugging
    print("\nApplying vowel harmony to these forms:")
    words_with_vowel_harmony = []
    for word in word_list:
        print(word)
        if back_vowel_determines_harmony(word):
            word = word.translate(str.maketrans("AO", "ao"))
            words_with_vowel_harmony.append(word)
        else:
            word = word.translate(str.maketrans("AO", "äö"))
            words_with_vowel_harmony.append(word)
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
    reversed_word = word[::-1]
    back_vowel_determines_harmony = False
    for c in reversed_word:
        if c in 'äö':
            break
        if c in 'aou':
            back_vowel_determines_harmony = True
            break

    return back_vowel_determines_harmony


def replace_i_with_j(word):
    return re.sub(r'(\w)aia', r'\1aja', word)


def apply_other_transformations(word_list):
    words = []
    for word in word_list:
        if re.search(r'[^t]aia', word):
            word = replace_i_with_j(word)
        words.append(word)

    return words
