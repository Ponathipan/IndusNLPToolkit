import re
import json

# Load the JSON mapping file
with open('/mnt/d/python-projects/IndusNLPToolkit/clean/closed-html-tags-dictionary.json', 'r', encoding='utf-8') as file:
    mappings = json.load(file)

# Load the JSON mapping file for CSS properties
with open('/mnt/d/python-projects/IndusNLPToolkit/clean/css-dictionary.json', 'r', encoding='utf-8') as file:
    css_mappings = json.load(file)

# Swap the key-value pairs and normalize the keys to lowercase
swapped_html_mappings = {value.lower(): key for key, value in mappings.items()}
swapped_css_mappings = {value.lower(): key for key, value in css_mappings.items()}

# Function to replace English tags with Hindi tags
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

# Input sentence
sentence = """<P> srclang= background-blend-mode: column-width: <small> <head> 6 साल की बच्ची अपनी मां के लिए बनी मां | UPUKLive 
6 साल की बच्ची अपनी मां के लिए बनी मां
जो प्यार, करुणा और देखभाल का स्वभाव ईश्वर ने बेटियों को दिया है, वह बेटों को हासिल नहीं है। मां को ब्रेन हैमरेज हो जाने के बाद छह साल की मासूम ने जिस तरह से मां की देखभाल की, उसे देखकर लगता है कि मां असल में बेटी है और बेटी मां है। काई चेंगचेंग जब महज छह साल की"""

# Replacing English tags with Hindi tags
result = replace_html_tags_css(sentence, swapped_html_mappings, swapped_css_mappings)

print(result)

