"""Inflection pattern tests"""

import pytest
import fin_ppgen.nlp as nlp

INFL_01 = [
    ('<N1A>baarimikko+Sg+Nom', '<N1A>baarimikko_'),
    ('<N1A>baarimikko+Sg+Gen', '<N1A>baarimikkon'),
    ('<N1A>baarimikko+Sg+Par', '<N1A>baarimikkoA'),
    ('<N1A>baarimikko+Sg+Ill', '<N1A>baarimikkoon'),
    ('<N1A>baarimikko+Sg+Ine', '<N1A>baarimikkossA'),
    ('<N1A>baarimikko+Sg+Ela', '<N1A>baarimikkostA'),
    ('<N1A>baarimikko+Sg+Ade', '<N1A>baarimikkollA'),
    ('<N1A>baarimikko+Sg+Abl', '<N1A>baarimikkoltA'),
    ('<N1A>baarimikko+Sg+All', '<N1A>baarimikkolle'),
    ('<N1A>baarimikko+Sg+Ess', '<N1A>baarimikkonA'),
    ('<N1A>baarimikko+Sg+Tra', '<N1A>baarimikkoksi'),
    ('<N1A>baarimikko+Pl+Nom', '<N1A>baarimikkot'),
    ('<N1A>baarimikko+Pl+Gen', '<N1A>baarimikkojen'),
    ('<N1A>baarimikko+Pl+Par', '<N1A>baarimikkojA'),
    ('<N1A>baarimikko+Pl+Ill', '<N1A>baarimikkoihin'),
    ('<N1A>baarimikko+Pl+Ine', '<N1A>baarimikkoissA'),
    ('<N1A>baarimikko+Pl+Ela', '<N1A>baarimikkoistA'),
    ('<N1A>baarimikko+Pl+Ade', '<N1A>baarimikkoillA'),
    ('<N1A>baarimikko+Pl+Abl', '<N1A>baarimikkoiltA'),
    ('<N1A>baarimikko+Pl+All', '<N1A>baarimikkoille'),
    ('<N1A>baarimikko+Pl+Ess', '<N1A>baarimikkoinA'),
    ('<N1A>baarimikko+Pl+Tra', '<N1A>baarimikkoiksi'),
]

INFL_02 = [
    ('<N2>aakkosto+Sg+Nom', '<N2>aakkosto_'),
    ('<N2>aakkosto+Sg+Gen', '<N2>aakkoston'),
    ('<N2>aakkosto+Sg+Par', '<N2>aakkostoA'),
    ('<N2>aakkosto+Sg+Ill', '<N2>aakkostoon'),
    ('<N2>aakkosto+Sg+Ine', '<N2>aakkostossA'),
    ('<N2>aakkosto+Sg+Ela', '<N2>aakkostostA'),
    ('<N2>aakkosto+Sg+Ade', '<N2>aakkostollA'),
    ('<N2>aakkosto+Sg+Abl', '<N2>aakkostoltA'),
    ('<N2>aakkosto+Sg+All', '<N2>aakkostolle'),
    ('<N2>aakkosto+Sg+Ess', '<N2>aakkostonA'),
    ('<N2>aakkosto+Sg+Tra', '<N2>aakkostoksi'),
    ('<N2>aakkosto+Pl+Nom', '<N2>aakkostot'),
    ('<N2>aakkosto+Pl+Gen', '<N2>aakkostojen'),
    ('<N2>aakkosto+Pl+Par', '<N2>aakkostojA'),
    ('<N2>aakkosto+Pl+Ill', '<N2>aakkostoihin'),
    ('<N2>aakkosto+Pl+Ine', '<N2>aakkostoissA'),
    ('<N2>aakkosto+Pl+Ela', '<N2>aakkostoistA'),
    ('<N2>aakkosto+Pl+Ade', '<N2>aakkostoillA'),
    ('<N2>aakkosto+Pl+Abl', '<N2>aakkostoiltA'),
    ('<N2>aakkosto+Pl+All', '<N2>aakkostoille'),
    ('<N2>aakkosto+Pl+Ess', '<N2>aakkostoinA'),
    ('<N2>aakkosto+Pl+Tra', '<N2>aakkostoiksi'),
]

INFL_11 = [
    ('<N11>omena+Sg+Nom', '<N11>omena_'),
    ('<N11>omena+Sg+Gen', '<N11>omenan'),
    ('<N11>omena+Sg+Par', '<N11>omenaA'),
    ('<N11>omena+Sg+Ill', '<N11>omenaAn'),
    ('<N11>omena+Sg+Ine', '<N11>omenassA'),
    ('<N11>omena+Sg+Ela', '<N11>omenastA'),
    ('<N11>omena+Sg+Ade', '<N11>omenallA'),
    ('<N11>omena+Sg+Abl', '<N11>omenaltA'),
    ('<N11>omena+Sg+All', '<N11>omenalle'),
    ('<N11>omena+Sg+Ess', '<N11>omenanA'),
    ('<N11>omena+Sg+Tra', '<N11>omenaksi'),
    ('<N11>omena+Pl+Nom', '<N11>omenat'),
    ('<N11>omena+Pl+Gen', '<N11>omenoiden'),
    ('<N11>omena+Pl+Par', '<N11>omenoitA'),
    ('<N11>omena+Pl+Ill', '<N11>omenoihin'),
    ('<N11>omena+Pl+Ine', '<N11>omenoissA'),
    ('<N11>omena+Pl+Ela', '<N11>omenoistA'),
    ('<N11>omena+Pl+Ade', '<N11>omenoillA'),
    ('<N11>omena+Pl+Abl', '<N11>omenoiltA'),
    ('<N11>omena+Pl+All', '<N11>omenoille'),
    ('<N11>omena+Pl+Ess', '<N11>omenoinA'),
    ('<N11>omena+Pl+Tra', '<N11>omenoiksi'),
]

INFL_12 = [
    ('<N12>kulkija+Sg+Nom', '<N12>kulkija_'),
    ('<N12>kulkija+Sg+Gen', '<N12>kulkijan'),
    ('<N12>kulkija+Sg+Par', '<N12>kulkijaA'),
    ('<N12>kulkija+Sg+Ill', '<N12>kulkijaAn'),
    ('<N12>kulkija+Sg+Ine', '<N12>kulkijassA'),
    ('<N12>kulkija+Sg+Ela', '<N12>kulkijastA'),
    ('<N12>kulkija+Sg+Ade', '<N12>kulkijallA'),
    ('<N12>kulkija+Sg+Abl', '<N12>kulkijaltA'),
    ('<N12>kulkija+Sg+All', '<N12>kulkijalle'),
    ('<N12>kulkija+Sg+Ess', '<N12>kulkijanA'),
    ('<N12>kulkija+Sg+Tra', '<N12>kulkijaksi'),
    ('<N12>kulkija+Pl+Nom', '<N12>kulkijat'),
    ('<N12>kulkija+Pl+Gen', '<N12>kulkijoiden'),
    ('<N12>kulkija+Pl+Par', '<N12>kulkijoitA'),
    ('<N12>kulkija+Pl+Ill', '<N12>kulkijoihin'),
    ('<N12>kulkija+Pl+Ine', '<N12>kulkijoissA'),
    ('<N12>kulkija+Pl+Ela', '<N12>kulkijoistA'),
    ('<N12>kulkija+Pl+Ade', '<N12>kulkijoillA'),
    ('<N12>kulkija+Pl+Abl', '<N12>kulkijoiltA'),
    ('<N12>kulkija+Pl+All', '<N12>kulkijoille'),
    ('<N12>kulkija+Pl+Ess', '<N12>kulkijoinA'),
    ('<N12>kulkija+Pl+Tra', '<N12>kulkijoiksi'),
]

INFL_13 = [
    ('<N13>katiska+Sg+Nom', '<N13>katiska_'),
    ('<N13>katiska+Sg+Gen', '<N13>katiskan'),
    ('<N13>katiska+Sg+Par', '<N13>katiskaA'),
    ('<N13>katiska+Sg+Ill', '<N13>katiskaAn'),
    ('<N13>katiska+Sg+Ine', '<N13>katiskassA'),
    ('<N13>katiska+Sg+Ela', '<N13>katiskastA'),
    ('<N13>katiska+Sg+Ade', '<N13>katiskallA'),
    ('<N13>katiska+Sg+Abl', '<N13>katiskaltA'),
    ('<N13>katiska+Sg+All', '<N13>katiskalle'),
    ('<N13>katiska+Sg+Ess', '<N13>katiskanA'),
    ('<N13>katiska+Sg+Tra', '<N13>katiskaksi'),
    ('<N13>katiska+Pl+Nom', '<N13>katiskat'),
    ('<N13>katiska+Pl+Gen', '<N13>katiskoiden'),
    ('<N13>katiska+Pl+Par', '<N13>katiskoitA'),
    ('<N13>katiska+Pl+Ill', '<N13>katiskoihin'),
    ('<N13>katiska+Pl+Ine', '<N13>katiskoissA'),
    ('<N13>katiska+Pl+Ela', '<N13>katiskoistA'),
    ('<N13>katiska+Pl+Ade', '<N13>katiskoillA'),
    ('<N13>katiska+Pl+Abl', '<N13>katiskoiltA'),
    ('<N13>katiska+Pl+All', '<N13>katiskoille'),
    ('<N13>katiska+Pl+Ess', '<N13>katiskoinA'),
    ('<N13>katiska+Pl+Tra', '<N13>katiskoiksi'),
]

INFL_14 = [
    ('<N14>solakka+Sg+Nom', '<N14>solakka_'),
    ('<N14>solakka+Sg+Gen', '<N14>solakan'),
    ('<N14>solakka+Sg+Par', '<N14>solakkaA'),
    ('<N14>solakka+Sg+Ill', '<N14>solakkaAn'),
    ('<N14>solakka+Sg+Ine', '<N14>solakassA'),
    ('<N14>solakka+Sg+Ela', '<N14>solakastA'),
    ('<N14>solakka+Sg+Ade', '<N14>solakallA'),
    ('<N14>solakka+Sg+Abl', '<N14>solakaltA'),
    ('<N14>solakka+Sg+All', '<N14>solakalle'),
    ('<N14>solakka+Sg+Ess', '<N14>solakkanA'),
    ('<N14>solakka+Sg+Tra', '<N14>solakaksi'),
    ('<N14>solakka+Pl+Nom', '<N14>solakat'),
    ('<N14>solakka+Pl+Gen', '<N14>solakoiden'),
    ('<N14>solakka+Pl+Par', '<N14>solakoitA'),
    ('<N14>solakka+Pl+Ill', '<N14>solakoihin'),
    ('<N14>solakka+Pl+Ine', '<N14>solakoissA'),
    ('<N14>solakka+Pl+Ela', '<N14>solakoistA'),
    ('<N14>solakka+Pl+Ade', '<N14>solakoillA'),
    ('<N14>solakka+Pl+Abl', '<N14>solakoiltA'),
    ('<N14>solakka+Pl+All', '<N14>solakoille'),
    ('<N14>solakka+Pl+Ess', '<N14>solakoinA'),
    ('<N14>solakka+Pl+Tra', '<N14>solakoiksi'),
]


@pytest.mark.parametrize("test_input, expected", INFL_01)
def test_inflection_pattern_01(test_input, expected):
    """Test inflection pattern 1"""
    assert nlp.inflect(test_input) == expected


@pytest.mark.parametrize("test_input, expected", INFL_02)
def test_inflection_pattern_02(test_input, expected):
    """Test inflection pattern 2"""
    assert nlp.inflect(test_input) == expected


@pytest.mark.parametrize("test_input, expected", INFL_11)
def test_test_inflection_pattern_11(test_input, expected):
    """Test inflection pattern 11"""
    assert nlp.inflect(test_input) == expected


@pytest.mark.parametrize("test_input, expected", INFL_12)
def test_test_inflection_pattern_12(test_input, expected):
    """Test inflection pattern 12"""
    assert nlp.inflect(test_input) == expected

@pytest.mark.parametrize("test_input, expected", INFL_13)
def test_test_inflection_pattern_13(test_input, expected):
    """Test inflection pattern 13"""
    assert nlp.inflect(test_input) == expected

@pytest.mark.parametrize("test_input, expected", INFL_14)
def test_test_inflection_pattern_14(test_input, expected):
    """Test inflection pattern 14"""
    assert nlp.inflect(test_input) == expected
