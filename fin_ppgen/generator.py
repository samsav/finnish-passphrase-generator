"""A simple passphrase generator for Finnish"""

from pathlib import Path
import os
import secrets
import csv
import re
import nlp


# TODO:
# - add support for alternative forms in e.g. plural genitive and partitive
# - add support for forming compounds
# - add option for only using base forms of words


def read_csv_to_dict(csv_file_path: Path) -> dict[str, dict[str, list[str]]]:
    """
    Reads a CSV file containing word data and parses it into a dictionary.

    Args:
        csv_file_path (Path): The path to the CSV file.

    Returns:
        dict[str, dict[str, list[str]]]: A dictionary where keys are words
        and values are dictionaries containing word data about its word class and
        inflection paradigms. The values are lists of strings.

        Example item in the dictionary: {'mussukka', {'word_class': ['S'], 'inflection': ['14*A']}}
    """
    word_dict: dict[str, dict[str, list[str]]] = {}
    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter="\t")
        for row in csv_reader:
            # The word itself is in the 'Hakusana' column.
            word: str = row["Hakusana"]
            # The word class is in the 'Sanaluokka' column.
            # Some words can belong to more than one word class. Some words are missing word class data.
            word_class_list: list[str] = [
                wc.strip() if wc else None for wc in row["Sanaluokka"].split(",")
            ]
            # Some words have alternative inflection paradigms separated by a comma.
            # Remove parentheses that denote optionality for a paradigm and strip any whitespace.
            # Words that do not have inflection data associated with them have an empty string in the 'Taivutustiedot' column.
            inflection_paradigm_list: list[str] = [
                re.sub(r"[\(\)]", "", p.strip()) if p else None
                for p in row["Taivutustiedot"].split(",")
            ]

            # The inflection paradigms in the data consist of a number optionally followed by an asterisk and an uppercase letter.
            # For example: 38, 4*A. Filter out rare exceptions to this pattern.
            if inflection_paradigm_list[0]:
                inflection_paradigm_list = [
                    inflection
                    for inflection in inflection_paradigm_list
                    if re.match(r"^\d", inflection)
                ]

            word_dict[word] = {
                "word_class": word_class_list,
                "inflection": inflection_paradigm_list,
            }
    return word_dict


def filter_dict_by_inflection(
    word_dict: dict[str, dict[str, list[str]]],
    lower_limit: int = 1,
    upper_limit: int = 15,
    get_only_noninflecting: bool = False,
):
    """
    Filters a dictionary of word data based on the inflection paradigm within a specified range.

    Args:
        word_dict (dict[str, dict[str, list[str]]]): A dictionary containing word data where keys are words
            and values are dictionaries containing word class and inflection paradigms.
            The 'inflection' value is expected to be a list of strings representing inflection paradigms.
        lower_limit (int, optional): The lower limit of the inflection paradigm range to filter.
            Defaults to 1.
        upper_limit (int, optional): The upper limit of the inflection paradigm range to filter.
            Defaults to 15.
        get_only_noninflecting (bool, optional): If True, only return words with non-inflecting paradigms
            marked as '99' or None. Defaults to False.

    Returns:
        dict[str, dict[str, list[str]]]: A filtered dictionary where keys are words and values are dictionaries
        containing word class and inflection paradigms, filtered based on the inflection paradigms within the
        specified range and the condition of including non-inflecting paradigms if specified.

        The structure of the filtered dictionary is the same as in the input dictionary.
    """

    filtered_dict: dict[str, dict[str, list[str]]] = dict()
    for word, data in word_dict.items():
        if get_only_noninflecting:
            if data["inflection"][0] in ("99", None):
                filtered_dict[word] = data

        else:
            for inflection in data["inflection"]:
                if (
                    inflection
                    and lower_limit <= int(inflection.split("*")[0]) <= upper_limit
                ):
                    filtered_dict[word] = data

    return filtered_dict


# TODO: filter dict by word class
def filter_dict_by_word_class(
    word_dict: dict[str, dict[str, list[str]]],
    word_classes: list[str],
    include_all: bool = False,
):
    return None


def filter_prefix_words(
    word_dict: dict[str, dict[str, list[str]]]
) -> dict[str, dict[str, list[str]]]:
    """
    Filters words in a dictionary based on whether they end with a hyphen ('-').

    Args:
        word_dict (dict[str, dict[str, list[str]]]): A dictionary where keys are words
            and values are dictionaries containing word data on word class and
            inflection paradigms stored as lists of strings.

    Returns:
        dict[str, dict[str, list[str]]]: A filtered dictionary where keys are words
            ending with a hyphen ('-') and values are dictionaries containing word data
            on word class and inflection paradigms.
    """
    return {word: data for word, data in word_dict.items() if word.endswith("-")}


def filter_suffix_words(word_dict: dict[str, dict[str, list[str]]]):
    """
    Filters words in a dictionary based on whether they start with a hyphen ('-').

    Args:
        word_dict (dict[str, dict[str, list[str]]]): A dictionary where keys are words
            and values are dictionaries containing word data on word class and
            inflection paradigms stored as lists of strings.

    Returns:
        dict[str, dict[str, list[str]]]: A filtered dictionary where keys are words
            starting with a hyphen ('-') and values are dictionaries containing word data
            on word class and inflection paradigms.
    """
    return {word: data for word, data in word_dict.items() if word.startswith("-")}


def random_set(word_list, size_of_set):
    """Randomly select a subset of the input word list."""
    random_entries = [secrets.choice(word_list) for i in range(size_of_set)]
    return random_entries


def form_passphrase(wordlist, length):
    """A helper function for turning random words in a list
    into a passphrase that is returned as a string."""
    words = random_set(wordlist, length)
    # clear possible internal spaces from words
    return " ".join([word.replace(" ", "") for word in words])


def main():
    """Main passphrase generation function"""

    print("Welcome to the Finnish passphrase generator!\n")

    csv_file_path: os.PathLike = Path(
        "../lang_data/nykysuomensanalista2022.csv"
    ).resolve()
    # Read the CSV word list file into a dict
    word_dict = read_csv_to_dict(csv_file_path)

    # Pick words from inflection paradigms 1-15
    filtered_inflections_dict = filter_dict_by_inflection(word_dict, 1, 15)
    # Get noninflecting words into a separate dictionary
    noninflecting_words_dict = filter_dict_by_inflection(
        word_dict, get_only_noninflecting=True
    )
    # Get words that can be used as prefixes or suffixes into separate dictionaries
    prefix_words_dict = filter_prefix_words(word_dict)
    suffix_words_dict = filter_suffix_words(word_dict)

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
            [lexical_nouns[i], gradated_nouns[i], inflected_nouns[i], final_nouns[i]]
            for i in range(50)
        ]

        print("\nHere are the transformations applied to the words:")
        print(
            "\n{:30}\t{:30}\t{:20}\t{:20}\t".format(
                "LEXICAL", "GRADATED", "INFLECTED", "FINAL"
            )
        )
        for word in processing_chain:
            print("{:30}\t{:30}\t{:20}\t{:20}\t".format(*word))

        print("\nHere are some possible phrases:\n")
        for i in range(0, 4):
            phrase = form_passphrase(final_nouns, 4)
            print("{0} characters: {1}\n".format(len(phrase), phrase))


if __name__ == "__main__":
    main()
