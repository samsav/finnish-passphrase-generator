from bs4 import BeautifulSoup
import secrets
import nlp
from helpers import random_set
"""A simple passphrase generator for Finnish"""

# TODO:
# - add support for alternative forms in e.g. plural genitive and partitive
# - add support for forming compounds
# - add option for only using base forms of words
# - reduce startup time by saving the parsed XML into a file? is that possible?
# - refactor code
# - write actual tests
# - move all print statements to main function


def read_kotus_xml(file_path):
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
    """Select word entries that have specified inflection paradigms
       in the Kotus word list. Return the word entries as a list."""

    print("Picking words with desired inflection paradigms...")
    word_entries_with_selected_infls = []
    for entry in word_entries:
        if entry.t is not None and int(entry.t.tn.string) >= lower_limit \
           and int(entry.t.tn.string) <= upper_limit:
            word_entries_with_selected_infls.append(entry)
    return word_entries_with_selected_infls


def form_passphrase(wordlist, length):
    """A helper function for turning random words in a list
       into a passphrase that is returned as a string."""
    words = random_set(wordlist, length)
    # clear possible internal spaces from words
    return ' '.join([word.replace(' ', '') for word in words])


def main():
    print("Welcome to the Finnish passphrase generator!\n")

    # Parse the XML file for the full word list
    full_word_list = read_kotus_xml(
        'kotus-sanalista_v1/kotus-sanalista_v1.xml')

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
        random_nouns = random_set(nouns, 50)
        preprocessed_nouns = nlp.prepend_lexical_info(random_nouns)
        lexical_nouns = nlp.generate_lexical_forms(preprocessed_nouns)
        gradated_nouns = nlp.apply_consonant_gradation(lexical_nouns)
        inflected_nouns = nlp.apply_inflection_rules(gradated_nouns)
        almost_done = nlp.apply_other_transformations(inflected_nouns)
        final_nouns = nlp.apply_vowel_harmony(almost_done)

        processing_chain = [
            [
                lexical_nouns[i], gradated_nouns[i],
                inflected_nouns[i], final_nouns[i]
            ]
            for i in range(50)
        ]

        print("\nHere are the transformations applied to the words:")
        for word in processing_chain:
            print("{}\t{}\t{}\t{}\t".format(*word))

        print("\nHere are some possible phrases:\n")
        for i in range(0, 4):
            phrase = form_passphrase(final_nouns, 4)
            print("{0} characters: {1}\n".format(len(phrase), phrase))

        print()


if __name__ == '__main__':
    main()
