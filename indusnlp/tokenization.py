import re
import os
import json


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


class Tokenization:
    def __init__(self, hindi_punctuations=None):
        data_dir = os.path.join(os.path.dirname(__file__), "data")

        if hindi_punctuations is None:
            self.hindi_punctuations = load_json(
                os.path.join(data_dir, "hindi_punctuations.json")
            )["punctuations"]
        else:
            self.hindi_punctuations = hindi_punctuations

    def word_tokenize(self, input_text):
        """Tokenizes the input text into words.

        Args:
        - input_text (str): The text to be tokenized.

        Returns:
        - list: A list of word tokens.
        """
        for punc in self.hindi_punctuations:
            if punc != "-":
                input_text = input_text.replace(punc, "")
        return input_text.split(" ")

    def sent_tokenize(self, input_text):
        """Tokenizes the input text into sentences.

        Args:
        - input_text (str): The text to be tokenized.

        Returns:
        - list: A list of sentence tokens.
        """
        return input_text.split("।")


if __name__ == "__main__":
    tokenizer = Tokenization()
    sample_text = "हेल्लो, नमस्ते। कैसे हैं? आप कहाँ हैं।"

    word_tokens = tokenizer.word_tokenize(sample_text)
    print("Word Tokens:", word_tokens)

    sentence_tokens = tokenizer.sent_tokenize(sample_text)
    print("Sentence Tokens:", sentence_tokens)
