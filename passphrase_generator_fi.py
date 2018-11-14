from bs4 import BeautifulSoup
import secrets
import re
from helpers import initialize_rules


"""A simple passphrase generator for Finnish"""

# TODO:
# - add support for alternative forms in e.g. plural genitive and partitive
# - add support for forming compounds
# - reduce startup time by saving the parsed XML into a file? is that possible?
# - refactor code
# - add option for only using base forms of words
# - write actual tests

# Sets for noun endings
GRAM_NUMBER = ['+Sg', '+Pl']
INFLECTIONS = [
    '+Nom', '+Gen', '+Par', '+Ine', '+Ela', '+Ill', '+Ade', '+Abl', '+All',
    '+Ess', '+Tra'
]
CLITICS = ['', 'hAn', 'kin', 'kO', 'pA', 'pAs']
GRADATION_RULES = initialize_rules('gradation-patterns.txt')
INFLECTION_RULES = initialize_rules('inflection-patterns.txt')


def prepare_full_list(file_path):
    """Parse an XML file containing a word list with BeautifulSoup and return
       a bs4.element.ResultSet object with all word entries from the file."""

    print("Parsing XML file...\n")
    with open(file_path, 'r') as fp:
        soup = BeautifulSoup(fp, 'lxml')
    # Read all word entries directly into a variable: the resulting
    # bs4.element.ResultSet object can be manipulated like a list
    print("Listing word entries...\n")
    word_entries = soup.find_all('st')
    return word_entries


# TODO: use *args to pass an arbitrary set of inflection numbers
#       to the function?
# Note that some entries do not have a <t> field in the word list:
# these appear to be compound nouns. Currently these entries are excluded.
def select_inflection_paradigms(word_entries, lower_limit, upper_limit):
    """Select word entries that have specific inflection paradigms
       in the Kotus word list. Return the word entries as a list."""

    print("Picking words with desired inflection paradigms...")
    word_entries_with_selected_infls = []
    for entry in word_entries:
        if entry.t is not None and int(entry.t.tn.string) >= lower_limit \
           and int(entry.t.tn.string) <= upper_limit:
            word_entries_with_selected_infls.append(entry)
    return word_entries_with_selected_infls


def pick_random_set(word_list, size_of_set):
    """Randomly select a subset of the input word list."""
    random_entries = [secrets.choice(word_list) for i in range(size_of_set)]
    return random_entries


def compose_nouns(word_list):
    """Prepend all noun entries in the list with their inflection
       and gradation paradigms. Return the entries as a list.
       
       If words in the list contain spaces, the spaces are replaced with
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
       with gradation replace rules applied. If no, return the original word
       in order to avoid returning None values."""
    for match_rule, grad_rule in GRADATION_RULES:
        if match_rule(word):
            return grad_rule(word)

    return word


def inflect(word):
    """Check if a word matches any inflection patterns: if yes, return the word
       with inflection replace rules applied. If no, return the original word
       in order to avoid returning None values."""
    for match_rule, inflect_rule in INFLECTION_RULES:
        if match_rule(word):
            return inflect_rule(word)

    return word


# TODO: remove temporary variable
def convert_to_plural(word):
    """Helper function for ensuring that words only appearing in the
       plural form (such as 'aivot' or 'häät') are lexically represented
       as plural."""
    word = re.sub(r't\+Sg', r'+Pl', word)
    return word


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
            word = convert_to_plural(word)
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
    word = re.sub(r'(\w)aia', r'\1aja', word)
    return word


def apply_other_transformations(word_list):
    words = []
    for word in word_list:
        if re.search(r'[^t]aia', word):
            word = replace_i_with_j(word)
        words.append(word)

    return words


# TODO: remove temporary variable
def form_passphrase(word_list):
    """A helper function for turning four random words in a list
       into a passphrase that is returned as a string."""
    four_words = pick_random_set(word_list, 4)
    # clear possible internal spaces from words
    phrase = ' '.join([word.replace(' ', '') for word in four_words])
    return phrase


def debug():
    """Printouts for debugging consonant gradation patterns
       and other features"""

    print("Debugging consonant gradation:")
    print("\nSingulars:")
    singulars = apply_consonant_gradation(['<N1A>baarimikko+Sg+Tra',
                                           '<N48A>hake+Sg+Gen',
                                           '<N5C>attentaatti+Sg+Tra',
                                           '<N5B>kaappi+Sg+Tra',
                                           '<N9E>lapa+Sg+Gen',
                                           '<N48E>taive+Sg+Gen',
                                           '<N1F>satu+Sg+All',
                                           '<N5J>evakuointi+Sg+Gen',
                                           '<N9D>vika+Sg+Gen',
                                           '<N32D>ien+Sg+Ill'])
    print("\nApplied consonant gradation:")
    for word in singulars:
        print(word)

    print("\nPlurals:")
    plurals = apply_consonant_gradation(['<N1A>baarimikko+Pl+Tra',
                                         '<N5C>attentaatti+Pl+Tra',
                                         '<N5B>kaappi+Pl+Tra',
                                         '<N9E>lapa+Pl+Nom',
                                         '<N48E>taive+Pl+Nom',
                                         '<N1F>satu+Pl+Ine',
                                         '<N5J>evakuointi+Pl+Ade',
                                         '<N5J>fosforointi+Pl+Gen',
                                         '<N9D>vika+Pl+Nom',
                                         '<N32D>ien+Pl+Par'])
    print("\nApplied consonant gradation:")
    for word in plurals:
        print(word)

    print("\nDebugging word-internal hyphens:")
    words = apply_inflection_rules(apply_consonant_gradation(
            ['<N6>agar-agar+Pl+Abl']
            ))
    for word in words:
        print(word)

    print("\nDebugging plural-only words:")
    words = apply_inflection_rules(apply_consonant_gradation(
            ['<N1>aivot+Sg+Abl']
            ))
    for word in words:
        print(word)

    print("\nDebugging loan words ending in consonants:")
    words = apply_inflection_rules(apply_consonant_gradation(
            ['<N5>ekstranet+Pl+Tra']
            ))
    for word in words:
        print(word)

    print("\nDebugging inflection patterns:")
    words = apply_inflection_rules(apply_consonant_gradation(
            ['<N7>salmi+Pl+Tra',
             '<N7>salmi+Sg+Ill',
             '<N8>genre+Sg+Ill',
             '<N8>genre+Pl+Ill',
             '<N9J>kähmintä+Pl+Par',
             '<N9>kala+Pl+Ill',
             '<N10F>pöytä+Sg+Gen',
             '<N10>koira+Pl+Ill']
            ))
    for word in apply_vowel_harmony(words):
        print(word)
    print()


def main():
    print("Welcome to the Finnish passphrase generator!\n")

    # Parse the XML file for the full word list
    full_word_list = prepare_full_list('kotus-sanalista_v1/kotus-sanalista_v1.xml')

    # Pick nouns from inflection paradigms 1-10
    nouns = select_inflection_paradigms(full_word_list, 1, 10)

    while True:
        # Simple control loop that only enforces exit condition
        command = input("Generate phrases? y/n ")
        if command == "n":
            print("Bye!")
            break

        # For each run of the loop, pick a new random set from the list of
        # nouns created earlier. Then determine their inflection and gradation
        # paradigms using the compose_nouns() function and apply gradation,
        # inflection, and vowel harmony rules in sequence.
        random_nouns = pick_random_set(nouns, 50)
        lexical_nouns = compose_nouns(random_nouns)
        gradated_nouns = apply_consonant_gradation(lexical_nouns)
        inflected_nouns = apply_inflection_rules(gradated_nouns)
        almost_done = apply_other_transformations(inflected_nouns)
        final_nouns = apply_vowel_harmony(almost_done)

        print("\nHere are the words with all transformations applied:")
        for word in final_nouns:
            print(word)

        print("\nHere are some possible phrases:\n")
        for i in range(0, 4):
            phrase = form_passphrase(final_nouns)
            print("{0} characters: {1}\n".format(len(phrase), phrase))

        print()

        # Uncomment to enable debugging output
        # debug()


if __name__ == '__main__':
    main()
