"""Tests for the passphrase generator"""

import nlp

import pytest


@pytest.mark.parametrize("test_input, expected",
                         [('<N1A>baarimikko+Sg+Gen', '<N1A>baarimiko+Sg+Gen'),
                          ('<N48A>hake+Sg+Gen', '<N48A>hakke+Sg+Gen'),
                          ('<N5B>kaappi+Sg+Gen', '<N5B>kaapi+Sg+Gen'),
                          ('<N41B>opas+Sg+Gen', '<N41B>oppas+Sg+Gen'),
                          ('<N1C>tyttö+Sg+Gen', '<N1C>tytö+Sg+Gen'),
                          ('<N48C>kate+Sg+Gen', '<N48C>katte+Sg+Gen'),
                          ('<N9D>vika+Sg+Gen', '<N9D>via+Sg+Gen'),
                          ('<N32D>ien+Sg+Gen', '<N32D>iken+Sg+Gen'),
                          ('<N1E>sopu+Sg+Gen', '<N1E>sovu+Sg+Gen'),
                          ('<N48E>taive+Sg+Gen', '<N48E>taipe+Sg+Gen'),
                          ('<N1F>satu+Sg+Gen', '<N1F>sadu+Sg+Gen'),
                          ('<N41F>keidas+Sg+Gen', '<N41F>keitas+Sg+Gen'),
                          ('<N1J>hento+Sg+Gen', '<N1J>henno+Sg+Gen'),
                          ('<N48J>vanne+Sg+Gen', '<N48J>vante+Sg+Gen')])
def test_consonant_gradation_sg_gen(test_input, expected):
    assert nlp.gradate(test_input) == expected


def debug():
    """Printouts for debugging consonant gradation patterns
       and other features"""

    print("Debugging consonant gradation:")
    print("\nSingulars:")
    singulars = nlp.apply_consonant_gradation([
        '<N1A>baarimikko+Sg+Tra', '<N48A>hake+Sg+Gen',
        '<N5C>attentaatti+Sg+Tra', '<N5B>kaappi+Sg+Tra', '<N9E>lapa+Sg+Gen',
        '<N48E>taive+Sg+Gen', '<N1F>satu+Sg+All', '<N10F>risteyskohta+Sg+Abl',
        '<N10F>päätekohta+Sg+Ela', '<N5J>evakuointi+Sg+Gen', '<N9D>vika+Sg+Gen',
        '<N32D>ien+Sg+Ill'
    ])
    print("\nApplied consonant gradation:")
    for word in singulars:
        print(word)

    print("\nPlurals:")
    plurals = nlp.apply_consonant_gradation([
        '<N1A>baarimikko+Pl+Tra', '<N5C>attentaatti+Pl+Tra',
        '<N5B>kaappi+Pl+Tra', '<N9E>lapa+Pl+Nom', '<N48E>taive+Pl+Nom',
        '<N1F>satu+Pl+Ine', '<N5J>evakuointi+Pl+Ade',
        '<N5J>fosforointi+Pl+Gen', '<N9D>vika+Pl+Nom', '<N32D>ien+Pl+Par'
    ])
    print("\nApplied consonant gradation:")
    for word in plurals:
        print(word)

    print("\nDebugging word-internal hyphens:")
    words = nlp.apply_inflection_rules(
        nlp.apply_consonant_gradation(['<N6>agar-agar+Pl+Abl']))
    for word in words:
        print(word)

    print("\nDebugging plural-only words:")
    words = nlp.apply_inflection_rules(
        nlp.apply_consonant_gradation(['<N1>aivot+Sg+Abl']))
    for word in words:
        print(word)

    print("\nDebugging loan words ending in consonants:")
    words = nlp.apply_inflection_rules(
        nlp.apply_consonant_gradation(['<N5>ekstranet+Pl+Tra']))
    for word in words:
        print(word)

    print("\nDebugging inflection patterns:")
    words = nlp.apply_inflection_rules(
        nlp.apply_consonant_gradation([
            '<N7>salmi+Pl+Tra', '<N7>salmi+Sg+Ill', '<N8>genre+Sg+Ill',
            '<N8>genre+Pl+Ill', '<N9J>kähmintä+Pl+Par', '<N9>kala+Pl+Ill',
            '<N10F>pöytä+Sg+Gen', '<N10>koira+Pl+Ill'
        ]))
    for word in nlp.apply_vowel_harmony(words):
        print(word)
    print()


if __name__ == "__main__":
    debug()
