import argparse
import json
import math
import os

from src.common.helper_classes import Pony


def parse_args():
    parser = argparse.ArgumentParser(description="Compute TF-IDF of pony speech")
    parser.add_argument(
        "-c", type=argparse.FileType("r"), metavar="Path to data", required=True
    )
    parser.add_argument("-n", type=int, metavar="Number of words", required=True)

    # Verify that the data file exists
    args = parser.parse_args()
    if not os.path.isfile(args.c.name):
        parser.error("The data file does not exist.")

    return args.c, args.n


def compute_tf_idf(word: str, pony: Pony, script):
    # Number of times word appears in pony's speech
    tf = script[pony.value][word]

    idf = math.log(len(script) / number_of_ponies_that_speak(word, script))

    return tf * idf


def number_of_ponies_that_speak(word, script):
    return sum(1 for pony in Pony if word in script[pony.value])


def main():
    input, n = parse_args()

    script = json.load(input)

    all_tf_idfs = {}
    highest_tf_idfs = {}

    # for each pony, for each word, get tf-idf
    for pony in Pony:
        all_tf_idfs[pony.value] = {}
        for word in script[pony.value]:
            all_tf_idfs[pony.value][word] = compute_tf_idf(word, pony, script)
        # sort tf-idfs by value
        all_tf_idfs[pony.value] = sorted(
            all_tf_idfs[pony.value].items(), key=lambda x: x[1], reverse=True
        )
        # get top n tf-idfs
        tf_idf = all_tf_idfs[pony.value][:n]
        top_words = [word for word, _ in tf_idf]
        highest_tf_idfs[pony.value] = top_words

    print(json.dumps(highest_tf_idfs, indent=4))
    pass


if __name__ == "__main__":
    main()
