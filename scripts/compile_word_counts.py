import argparse
import json
import os

import pandas as pd

from src.common.helper_classes import Headers, Pony


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", type=argparse.FileType("r"), metavar="Path to data", required=True
    )
    parser.add_argument("--output", type=argparse.FileType("w"), required=True)

    # Verify that the data file exists
    args = parser.parse_args()
    if not os.path.isfile(args.d.name):
        parser.error("The data file does not exist.")

    return args.d, args.output


def retrieve_stopwords():
    # Read the stopwords file
    stopwords = pd.read_csv("data/stopwords.txt", header=None)
    return stopwords


def import_data_from_file(input, stopwords):
    # Read the data file
    data = pd.read_csv(input, sep=",")

    data[Headers.pony.value] = data[Headers.pony.value].str.lower()

    # Only select the columns we need
    data = data[[Headers.pony.value, Headers.dialog.value]]

    # Filter lowercased data to only include the ponies
    data = data[data[Headers.pony.value].isin([pony.value for pony in Pony])]
    data.reset_index(drop=True, inplace=True)

    # Remove punctuation
    data[Headers.dialog.value] = data[Headers.dialog.value].str.replace(
        r"[^\w\s|']", "", regex=True
    )

    # Lowercase all words
    data[Headers.dialog.value] = data[Headers.dialog.value].str.lower()

    # Remove stopwords
    data[Headers.dialog.value] = data[Headers.dialog.value].apply(
        lambda x: " ".join(x for x in x.split() if x not in stopwords[0].values)
    )
    return data


def count_words(data):
    counts = {}
    for pony in Pony:
        pony_data = data[data[Headers.pony.value] == pony.value]
        pony_dialog = pony_data[Headers.dialog.value]
        # count appearances of each word, remove punctuation
        word_counts = pony_dialog.str.split(expand=True).stack().value_counts()

        pony_words = {}
        for word, count in word_counts.items():
            if "'" in word:
                continue
            if count >= 5:
                pony_words[word] = count

        counts[pony.value] = pony_words

    return counts


def main():
    input, output = parse_args()

    stopwords = retrieve_stopwords()

    data = import_data_from_file(input, stopwords)

    counts = count_words(data)

    json.dump(counts, output)
    pass


if __name__ == "__main__":
    main()
