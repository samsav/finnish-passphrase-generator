from bs4 import BeautifulSoup
import random
import re

"""A simple passphrase generator for Finnish"""

# TODO:
# - use secrets instead of random?
# - add support for alternative forms in e.g. plural genitive and partitive?
# - fix vowel harmony
# - enable clitics
# - add support for forming compounds?


def prepare_full_list(file_path):
    """Parse an XML file containing a word list with BeautifulSoup and return
       a bs4.element.ResultSet object with all word entries from the file."""

    print("Parsing XML file...\n")
    with open(file_path, 'r') as fp:
        soup = BeautifulSoup(fp, 'lxml')
    # Read all word entries directly into a variable; the resulting
    # bs4.element.ResultSet object can be manipulated like a list
    print("Listing word entries...\n")
    word_entries = soup.find_all('st')
    return word_entries


# TODO: use *args to pass an arbitrary set of inflection numbers
#       to the function?
# Note that some entries do not have a <t> field in the word list;
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


# Pick X word entries at random. Using random.sample here to avoid getting
# duplicates. Will replace with random.choices for final version. (Or secrets.)
def pick_random_set(word_list, size_of_set):
    """Randomly select a subset of the input word list."""
    random_entries = random.sample(word_list, k=size_of_set)
    return random_entries


def compose_nouns(word_list):
    """Prepend all noun entries in the list with their inflection
       and gradation paradigms. Return the entries as a list."""

    print("Composing noun entries...")
    nouns = []
    for word_entry in word_list:
        # replace spaces with underscores to simplify later regexes
        word = word_entry.s.string.replace(' ', '_')
        infl_paradigm = 'N'
        grad_paradigm = ''
        # the first 51 inflection paradigms in the Kotus word list cover nouns
        if word_entry.t is not None and int(word_entry.t.tn.string) < 52:
            infl_paradigm += word_entry.t.tn.string
        if word_entry.av is not None:
            grad_paradigm = word_entry.av.string
        word = '<' + infl_paradigm + grad_paradigm + '>' + word
        word = attach_noun_endings(word)
        nouns.append(word)

    return nouns


def attach_noun_endings(noun):
    """Attach random number, inflection, and clitic endings to a noun."""
    number = random.choice(number_set)
    inflection = random.choice(inflection_set)
    # clitic = random.choice(clitic_set)
    noun = noun + number + inflection
    return noun


number_set = ['+Sg', '+Pl']

inflection_set = ['+Nom', '+Gen', '+Par',
                  '+Ine', '+Ela', '+Ill',
                  '+Ade', '+Abl', '+All',
                  '+Ess', '+Tra']

clitic_set = ['', 'hAn', 'kin', 'kO', 'pA']


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
            rules.append(build_inflect_functions(
                            pattern, search, replace))

    return rules


gradations = initialize_rules('gradation-patterns.txt')
inflections = initialize_rules('inflection-patterns.txt')


def gradate(word):
    """Check if a word matches any gradation patterns: if yes, return the word
       with gradation replace rules applied. If no, return the original word
       in order to avoid returning None values."""
    for match_rule, grad_rule in gradations:
        if match_rule(word):
            return grad_rule(word)

    return word


def inflect(word):
    """Check if a word matches any inflection patterns: if yes, return the word
       with inflection replace rules applied. If no, return the original word
       in order to avoid returning None values."""
    for match_rule, inflect_rule in inflections:
        if match_rule(word):
            return inflect_rule(word)

    return word


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
    gradated_words = []
    for word in word_list:
        print(word)
        # TODO: move checking for plurals to a separate function
        if re.search(r't\+Sg', word):
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
        if determine_vowel_harmony(word):
            word = word.translate(str.maketrans("AO", "ao"))
            words_with_vowel_harmony.append(word)
        else:
            word = word.translate(str.maketrans("AO", "äö"))
            words_with_vowel_harmony.append(word)
    return words_with_vowel_harmony


def determine_vowel_harmony(word):
    """A fairly simplistic algorithm for determining the vowel harmony
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


def form_passphrase(word_list):
    """A helper function for turning four random words in a list
       into a passphrase that is returned as a string."""
    four_words = pick_random_set(word_list, 4)
    phrase = ' '.join(four_words)
    return phrase


def debug():
    """Printouts for debugging consonant gradation patterns
       and other features"""

    print("Debugging consonant gradation:")
    print("\nSingulars:")
    singulars = apply_consonant_gradation(['<N1A>baarimikko+Sg+Tra',
                                           '<N5C>attentaatti+Sg+Tra',
                                           '<N5B>kaappi+Sg+Tra',
                                           '<N9E>lapa+Sg+Gen',
                                           '<N48E>taive+Sg+Gen',
                                           '<N1F>satu+Sg+All',
                                           '<N5J>evakuointi+Sg+Gen'])
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
                                         '<N5J>fosforointi+Pl+Gen'])
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


def main():
    print("Welcome to the Finnish passphrase generator!\n")

    # Parse the XML file for the full word list
    full_word_list = prepare_full_list('kotus_sanalista/testilista.xml')

    # Pick nouns from inflection paradigms 1-6
    nouns = select_inflection_paradigms(full_word_list, 1, 6)

    while True:
        # Simple control loop that only enforces exit condition
        command = input("Generate phrases? y/n ")
        if command == "n":
            break

        # For each run of the loop, pick a new random set from the list of
        # nouns created earlier. Then determine their inflection and gradation
        # paradigms using the compose_nouns() function and apply gradation,
        # inflection, and vowel harmony rules in sequence.
        random_nouns = pick_random_set(nouns, 50)
        lexical_nouns = compose_nouns(random_nouns)
        gradated_nouns = apply_consonant_gradation(lexical_nouns)
        inflected_nouns = apply_inflection_rules(gradated_nouns)
        final_nouns = apply_vowel_harmony(inflected_nouns)

        print("\nHere are the words with all transformations applied:")
        for word in final_nouns:
            print(word)

        print("\nHere are some possible phrases:\n")
        for i in range(0, 4):
            phrase = form_passphrase(final_nouns)
            print("{0} merkkiä: {1}\n".format(len(phrase), phrase))

        print()

        debug()


if __name__ == '__main__':
    main()
