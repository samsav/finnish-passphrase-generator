"""Gradation pattern tests"""

import pytest

# from context import fin_ppgen
import fin_ppgen.nlp


GRADS = [('<N1A>baarimikko+Sg+Gen', '<N1A>baarimiko+Sg+Gen'),
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
         ('<N48J>vanne+Sg+Gen', '<N48J>vante+Sg+Gen')]

@pytest.mark.parametrize("test_input, expected", GRADS)
def test_consonant_gradation_sg_gen(test_input, expected):
    """Test all consonant gradation paradigms in the singular genitive case"""
    assert fin_ppgen.nlp.gradate(test_input) == expected


@pytest.mark.parametrize("test_input, expected",
                         [('<N1A>baarimikko+Pl+Nom', '<N1A>baarimiko+Pl+Nom'),
                          ('<N48A>hake+Pl+Nom', '<N48A>hakke+Pl+Nom'),
                          ('<N5B>kaappi+Pl+Nom', '<N5B>kaapi+Pl+Nom'),
                          ('<N41B>opas+Pl+Nom', '<N41B>oppas+Pl+Nom'),
                          ('<N1C>tyttö+Pl+Nom', '<N1C>tytö+Pl+Nom'),
                          ('<N48C>kate+Pl+Nom', '<N48C>katte+Pl+Nom'),
                          ('<N9D>vika+Pl+Nom', '<N9D>via+Pl+Nom'),
                          ('<N32D>ien+Pl+Nom', '<N32D>iken+Pl+Nom'),
                          ('<N1E>sopu+Pl+Nom', '<N1E>sovu+Pl+Nom'),
                          ('<N48E>taive+Pl+Nom', '<N48E>taipe+Pl+Nom'),
                          ('<N1F>satu+Pl+Nom', '<N1F>sadu+Pl+Nom'),
                          ('<N41F>keidas+Pl+Nom', '<N41F>keitas+Pl+Nom'),
                          ('<N1J>hento+Pl+Nom', '<N1J>henno+Pl+Nom'),
                          ('<N48J>vanne+Pl+Nom', '<N48J>vante+Pl+Nom')])
def test_consonant_gradation_pl_nom(test_input, expected):
    """Test all consonant gradation paradigms in the plural nominative case"""
    assert fin_ppgen.nlp.gradate(test_input) == expected


# Legacy debugging code
# def debug():
#     """Printouts for debugging consonant gradation patterns
#        and other features"""

#     print("\nDebugging word-internal hyphens:")
#     words = nlp.apply_inflection_rules(
#         nlp.apply_consonant_gradation(['<N6>agar-agar+Pl+Abl']))
#     for word in words:
#         print(word)

#     print("\nDebugging plural-only words:")
#     words = nlp.apply_inflection_rules(
#         nlp.apply_consonant_gradation(['<N1>aivot+Sg+Abl']))
#     for word in words:
#         print(word)

#     print("\nDebugging loan words ending in consonants:")
#     words = nlp.apply_inflection_rules(
#         nlp.apply_consonant_gradation(['<N5>ekstranet+Pl+Tra']))
#     for word in words:
#         print(word)

#     print("\nDebugging inflection patterns:")
#     words = nlp.apply_inflection_rules(
#         nlp.apply_consonant_gradation([
#             '<N7>salmi+Pl+Tra', '<N7>salmi+Sg+Ill', '<N8>genre+Sg+Ill',
#             '<N8>genre+Pl+Ill', '<N9J>kähmintä+Pl+Par', '<N9>kala+Pl+Ill',
#             '<N10F>pöytä+Sg+Gen', '<N10>koira+Pl+Ill'
#         ]))
#     for word in nlp.apply_vowel_harmony(words):
#         print(word)
#     print()


# if __name__ == "__main__":
#     debug()
