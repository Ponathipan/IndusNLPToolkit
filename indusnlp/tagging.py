from nltk.corpus import indian
from nltk.tag import tnt


class Tagging:
    def __init__(self):
        pass

    def tagger_train(self):
        """Trains a POS tagger.

        Returns:
        - object: The trained POS tagger.
        """
        taggedSet = "hindi.pos"
        wordSet = indian.sents(taggedSet)
        count = 0
        for sen in wordSet:
            count += 1

        trainPerc = 0.9
        trainRows = int(trainPerc * count)
        testRows = trainRows + 1

        data = indian.tagged_sents(taggedSet)
        train_data = data[:trainRows]
        test_data = data[testRows:]

        pos_tagger = tnt.TnT()
        pos_tagger.train(train_data)
        return pos_tagger

    def pos_tags(self, input_text, tokenizer):
        """Provides POS tags for the input text.

        Args:
        - input_text (str): The text to be tagged.
        - tokenizer (object): An instance of a tokenizer to tokenize the input text.

        Returns:
        - list: A list of tuples with word tokens and their corresponding POS tags.
        """
        tokens = tokenizer.word_tokenize(input_text)
        pos_tagger = self.tagger_train()
        return pos_tagger.tag(tokens)


if __name__ == "__main__":
    from tokenization import Tokenization

    tagger = Tagging()
    tokenizer = Tokenization()
    sample_text = "मैं भारत में रहता हूँ।"
    pos_tags = tagger.pos_tags(sample_text, tokenizer)
    print("POS Tags:", pos_tags)
