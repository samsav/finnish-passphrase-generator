"""Tests for the passphrase generator"""

import passphrase_generator_fi as ppgen


def debug():
    """Printouts for debugging consonant gradation patterns
       and other features"""

    print("Debugging consonant gradation:")
    print("\nSingulars:")
    singulars = ppgen.apply_consonant_gradation([
        '<N1A>baarimikko+Sg+Tra', '<N48A>hake+Sg+Gen',
        '<N5C>attentaatti+Sg+Tra', '<N5B>kaappi+Sg+Tra', '<N9E>lapa+Sg+Gen',
        '<N48E>taive+Sg+Gen', '<N1F>satu+Sg+All', '<N5J>evakuointi+Sg+Gen',
        '<N9D>vika+Sg+Gen', '<N32D>ien+Sg+Ill'
    ])
    print("\nApplied consonant gradation:")
    for word in singulars:
        print(word)

    print("\nPlurals:")
    plurals = ppgen.apply_consonant_gradation([
        '<N1A>baarimikko+Pl+Tra', '<N5C>attentaatti+Pl+Tra',
        '<N5B>kaappi+Pl+Tra', '<N9E>lapa+Pl+Nom', '<N48E>taive+Pl+Nom',
        '<N1F>satu+Pl+Ine', '<N5J>evakuointi+Pl+Ade',
        '<N5J>fosforointi+Pl+Gen', '<N9D>vika+Pl+Nom', '<N32D>ien+Pl+Par'
    ])
    print("\nApplied consonant gradation:")
    for word in plurals:
        print(word)

    print("\nDebugging word-internal hyphens:")
    words = ppgen.apply_inflection_rules(
        ppgen.apply_consonant_gradation(['<N6>agar-agar+Pl+Abl']))
    for word in words:
        print(word)

    print("\nDebugging plural-only words:")
    words = ppgen.apply_inflection_rules(
        ppgen.apply_consonant_gradation(['<N1>aivot+Sg+Abl']))
    for word in words:
        print(word)

    print("\nDebugging loan words ending in consonants:")
    words = ppgen.apply_inflection_rules(
        ppgen.apply_consonant_gradation(['<N5>ekstranet+Pl+Tra']))
    for word in words:
        print(word)

    print("\nDebugging inflection patterns:")
    words = ppgen.apply_inflection_rules(
        ppgen.apply_consonant_gradation([
            '<N7>salmi+Pl+Tra', '<N7>salmi+Sg+Ill', '<N8>genre+Sg+Ill',
            '<N8>genre+Pl+Ill', '<N9J>kähmintä+Pl+Par', '<N9>kala+Pl+Ill',
            '<N10F>pöytä+Sg+Gen', '<N10>koira+Pl+Ill'
        ]))
    for word in ppgen.apply_vowel_harmony(words):
        print(word)
    print()


if __name__ == "__main__":
    debug()
