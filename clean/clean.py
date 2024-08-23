#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# Set BASE_DIR to the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



INDIC_NLP_LIB_HOME="./indic_nlp_library"
#INDIC_NLP_RESOURCES="./indic_nlp_resources"
# Since indic_nlp_resources is inside the 'clean' folder, adjust the path accordingly
INDIC_NLP_RESOURCES = os.path.join(BASE_DIR, "indic_nlp_resources")

from indicnlp import common
common.set_resources_path(INDIC_NLP_RESOURCES)

from indicnlp import loader
loader.load()
import json
import re
from langdetect import detect_langs
from indicnlp.tokenize import sentence_tokenize
from clean.badwords_en_hi_hiR import badword_list
# Constants
_MIN_WORDS_PER_LINE = 3
_MIN_NUM_SENTENCES = 3
_MAX_WORD_LENGTH = 150
_HINDI_END_MARKS = ("।", "?", "!", "\"", "," ,"॥")
_ELLIPSIS = "..."
_POLICY_SUBSTRINGS = [
    "terms of use", "privacy policy", "cookie policy", "uses cookies",
    "use of cookies", "use cookies", "उपयोग की शर्तें", "गोपनीयता नीति",
    "कुकी नीति", "कुकीज़ का उपयोग करता है"
]

# Regex patterns
URL_REGEX = re.compile(r'http[s]?://\S+|www\.\S+')
EMAIL_REGEX = re.compile(r'\S+@\S+\.\S+')
EXTRA_SPACES_REGEX = re.compile(r'[ \t]+')

badwords_regex = re.compile(r"(?:\W|^)({})(?:\W|$)".format("|".join(badword_list)))


# Load the JSON mapping file
with open('/mnt/d/python-projects/IndusNLPToolkit/clean/closed-html-tags-dictionary.json', 'r', encoding='utf-8') as file:
    mappings = json.load(file)

# Load the JSON mapping file for CSS properties
with open('/mnt/d/python-projects/IndusNLPToolkit/clean/css-dictionary.json', 'r', encoding='utf-8') as file:
    css_mappings = json.load(file)

# Swap the key-value pairs and normalize the keys to lowercase
swapped_html_mappings = {value.lower(): key for key, value in mappings.items()}
swapped_css_mappings = {value.lower(): key for key, value in css_mappings.items()}

def badwords_filter(text):
    badwords_found = badwords_regex.search(text.lower())
    return badwords_found is None

def remove_urls_and_emails(text):
    text = URL_REGEX.sub("", text)
    text = EMAIL_REGEX.sub("", text)
    return text

def remove_extra_spaces(text):
    return EXTRA_SPACES_REGEX.sub(" ", text).strip()

def replace_html_tags_css(text, html_mapping,css_mapping):
    # Replace the HTML tags and CSS properties
    #for eng_tag, hindi_tag in mapping.items():
        #text = re.sub(re.escape(eng_tag), hindi_tag, text)

    for eng_tag in sorted(html_mapping.keys(), key=len, reverse=True):
        hindi_tag = html_mapping[eng_tag]
        # Match exact HTML tags or properties using non-word characters as boundaries
        text = re.sub(r'(?<!\w)' + re.escape(eng_tag) + r'(?!\w)', hindi_tag, text, flags=re.IGNORECASE)

        # Replace the CSS properties
    for css_property in sorted(css_mapping.keys(), key=len, reverse=True):
        eng_property = css_mapping[css_property]
        text = re.sub(r'(?<!\w)' + re.escape(css_property) + r'(?!\w)', eng_property, text, flags=re.IGNORECASE)

    return text

def clean_text(text, min_words_per_line=_MIN_WORDS_PER_LINE, min_num_sentences=_MIN_NUM_SENTENCES, max_word_length=_MAX_WORD_LENGTH):
    '''if not isinstance(text, str):
        return None  # Skip non-string inputs
    try:
        # Language check
        probabilities = detect_langs(text)
        if not any(lang.lang == 'hi' and lang.prob > 0.99 for lang in probabilities):
            return None  # Skip text if not Hindi with high probability

        # Remove URLs and emails
        text = remove_urls_and_emails(text)
        text = remove_extra_spaces(text)

        lines = text.splitlines()
        valid_lines = []
        num_sentences = 0'''
    text = remove_urls_and_emails(text)

    text = replace_html_tags_css(text, swapped_html_mappings, swapped_css_mappings)

    if not badwords_filter(text):
        return None
    return text

    #     for line in lines:
    #         line = line.strip()
    #         if len(line.split()) < min_words_per_line or any(len(word) > max_word_length for word in line.split()):
    #             continue
    #         if not line.endswith(_HINDI_END_MARKS) or line.endswith(_ELLIPSIS):
    #             continue
    #         if any(policy in line for policy in _POLICY_SUBSTRINGS):
    #             continue
    #         num_sentences += len(sentence_tokenize.sentence_split(line, lang='hi'))
    #         valid_lines.append(line)
    #
    #     if num_sentences < min_num_sentences:
    #         return None
    #
    #     result = "\n".join(valid_lines).strip()
    #     return result if 500 <= len(result) <= 50000 else None
    #
    # except Exception as e:
    #     # print(f"An error occurred: {e}")
    #     return None'''

if __name__ == "__main__":

    test_string = """"6 साल की बच्ची अपनी मां के लिए बनी मां | UPUKLive <p> column-width:
    6 साल की बच्ची अपनी मां के लिए बनी मां
    जो प्यार, करुणा और देखभाल का स्वभाव ईश्वर ने बेटियों को दिया है, वह बेटों को हासिल नहीं है। मां को ब्रेन हैमरेज हो जाने के बाद छह साल की मासूम ने जिस तरह से मां की देखभाल की, उसे देखकर लगता है कि मां असल में बेटी है और बेटी मां है। काई चेंगचेंग जब महज छह साल की थी, तो उसकी मां चेन ली को ब्रेन हैमरेज हो गया था। इसकी वजह से उनकी याददाश्त खराब हो गई।
    बीते चार साल से अपनी मां को पढ़ना, लिखना और बोलना सिखाना ही काई की दिनचर्या का हिस्सा हो गया है। वह कहती है कि कभी मां ने मुझे पढ़ना, लिखना सिखाया था, अब मेरी बारी है कि मैं अपनी मां को पढ़ना लिखना सिखाऊं। मैं मां के लिए पढ़ाई किसी खेल की तरह सिखाती हूं, ताकि उनके लिए इसे समझना https://3.bp.blogspot.com/-CJyEsqibU60/W_Q7SAtg7MI/AAAAAAADdhM/8xf2fBeqM7EYImZcZM-WAYu79KjX0JocwCK4BGAYYCw/s640/-%2Bupuklive%2B-%2BCopy%2B%25282%2529.PNG
    आसान हो http://www.upuklive.com/2018/11/6_20.html जाए।
    उदाहरण के लिए जब मैं उन्हें एपल के बारे में बताती हूं, तो उन्हें सेब देती हूं, ताकि वह इसे खाकर उसका स्वाद और उसके बारे में जान सकें। जब मैं रैबिट के बारे में बताती हूं, तो उन्हें खरगोश पकड़ने के लिए देती हूं।
    काई के पिता एक छोटी सी दुकान चलाकर परिवार का पालन-पोषण और पत्नी के इलाज का खर्च निकाल रहे हैं। इसलिए वह पत्नी की देखभाल के लिए ज्यादा समय नहीं निकाल पाते हैं। वहीं, बड़ा भाई काई लिंग ने हाई स्कूल में दाखिला लिया है, जिसकी वजह से वह भी मां की देखभाल नहीं कर पाता है। ऐसे में काई ही अपनी मां की देखभाल करती हैं।
    वह मां को चीनी भाषा सिखाने के साथ ही उन्हें रोज समय पर दवाएं देना भी नहीं भूलती हैं। इसके साथ ही मां को जल्दी से ठीक करने के लिए वह फीजियोथैरेपी एक्सरसाइज कराती हैं। काई कहती हैं कि मां को हाई ब्लड प्रेशर की बीमारी है और ठीक होने के लिए उन्हें लगातार समय पर दवाएं लेना जरूरी है। यदि कोई उन्हें याद नहीं दिलाए, तो वह दवा लेना ही भूल जाती हैं।
    बीचे चार साल से काई लगातार कड़ी चुनौतियों का सामना करने के बावजूद स्कूल में न सिर्फ अच्छे ग्रेड हासिल करती हैं, बल्कि लीडरशिप रोल भी निभाती हैं। मां के प्रति काई के समर्पण को देखते हुए स्थानीय सरकार ने उन्हें पुरस्कृत किया है और स्थानीय सरकारी ब्रॉडकास्टर सीसीटीवी ने भी उन्हें पहचान दी है। चीन की मीडिया उन लोगों के बारे में अक्सर समाचार दिखाती है, जो इस तरह के काम करते हैं।
    UPUKLive: 6 साल की बच्ची अपनी मां के लिए बनी मां
    https://3.bp.blogspot.com/-CJyEsqibU60/W_Q7SAtg7MI/AAAAAAADdhM/8xf2fBeqM7EYImZcZM-WAYu79KjX0JocwCK4BGAYYCw/s72-c/-%2Bupuklive%2B-%2BCopy%2B%25282%2529.PNG
    "
    """
    cleaned_text = clean_text(test_string)
    if cleaned_text:
        print("Cleaned Text:\n", cleaned_text)
    else:
        print("Text was not processed or did not meet the criteria for cleaning.")
