# IndusNLPToolkit

A toolkit for processing and analyzing Hindi and related dialects.

<h1 align="center">

<img src="branding/logo/primary/IndusLogo.png" width="300">
</h1><br>

India's rich civilization mirrors a tapestry of human cultural heritage, thriving amidst a diversity of languages and traditions. The nation's linguistic mosaic encompasses over 1,600 languages, showcasing the vast linguistic diversity spread across its extensive landscapes. From Hindi to Tamil, Bengali to Gujarati, each language narrates a unique story, adding colors to the vibrant social fabric of India.

The `IndusNLPToolkit` is an open-source toolkit designed to facilitate specific NLP tasks required for the exploration of 40+ Hindi dialects, with plans to include additional dialects in subsequent phases.

## Features

- **Tokenization**: Efficiently tokenize Hindi text into words and sentences.
- **Cleaning**: Clean English words, convert English numbers to Hindi, and more.
- **Tagging**: Perform POS tagging on Hindi text.

## Installation

To install the toolkit, clone the repository and navigate to the root directory:

```bash
git clone https://github.com/Tech-Mahindra-Makers-Lab/IndusNLPToolkit.git
cd IndusNLPToolkit
```

Then, run the setup script:

```bash
python setup.py install
```

or

```bash
pip install git+https://github.com/Tech-Mahindra-Makers-Lab/IndusNLPToolkit.git
```

## Usage

Here's a basic usage example:

```python
from indusnlp import Tokenization
from indusnlp import HindiTextCleaner, TextCleaner
from indusnlp import Tagging

# Sample text in Hindi
text_hindi = "संसद के विशेष सत्र के बीच ..."

# Tokenization
tokenizer = Tokenization()
words = tokenizer.word_tokenize(text_hindi)
sentences = tokenizer.sent_tokenize(text_hindi)

# Output example
print(words)
# ['संसद', 'के', 'विशेष', 'सत्र', 'के', 'बीच', ...]

print(sentences)
# ['संसद के विशेष सत्र के बीच ...']

# Cleaning
cleaner = HindiTextCleaner(transliterate=True)
cleaned_text = cleaner(text_hindi)

# Output example
print(cleaned_text)
# 'संसद के विशेष सत्र के बीच ...'

# Tagging
tagger = Tagging()
tags = tagger.pos_tags(text_hindi, tokenizer=tokenizer)

# Output example
print(tags)
# [('संसद', 'NN'), ('के', 'PREP'), ...]
```

For detailed usage and examples, refer to the individual module documentation.

## Contributing

We welcome contributions to the `IndusNLPToolkit`. Whether it's bug reports, feature requests, or new dialects, your input is valuable. Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

---
