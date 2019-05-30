"""Inflection pattern tests"""

import pytest

# from context import fin_ppgen
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
