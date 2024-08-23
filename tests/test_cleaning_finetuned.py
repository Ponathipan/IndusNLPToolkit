from indusnlp import TextCleaner, HindiTextCleaner
import pandas as pd
from datasets import load_dataset
from multiprocessing import cpu_count
from clean import clean_text

# Configuration for the text cleaning
config = [

    ("handle_whitespace", None),
    ("remove_redundant_lines", None),
    ("remove_blank_lines", None),
]
textcleaner = TextCleaner(config)
hicleaner = HindiTextCleaner(transliterate=True)


def clean_content(example):
    # Strip whitespace from 'question' and 'answer'
    question = example["question"].strip() if example["question"] is not None else ''
    answer = example["answer"].strip()  if example["answer"] is not None else ''

    question_bad_word = clean_text(question)
    if question_bad_word is not None:
        answer_bad_word = clean_text(answer)
        if answer_bad_word is not None:
            # Apply text cleaning functions
            cleaned_question = hicleaner(textcleaner(question))
            cleaned_answer = hicleaner(textcleaner(answer))
            return {"question": cleaned_question, "answer": cleaned_answer}
    return {"question": None, "answer": None}




#df = pd.read_csv('/mnt/d/indus-finetuned-datasets/Nilesh/SFT_Nilesh_Translated_GAIR_lima_train_hi_translated_cleaned.csv')
#df['text'] = df['text'].apply(clean_content)
#df = df[df['text'].notnull() & df['text'].str.len() > 0]




# Load the CSV file into a Dataset
#dataset = load_dataset('csv', data_files='/mnt/d/indus-finetuned-datasets/Nilesh/SFT_Nilesh_Translated_GAIR_lima_train_hi_translated_cleaned.csv')
dataset = load_dataset('csv', data_files='/mnt/d/indus-finetuned-datasets/Nilesh/translated/SFT_Nilesh_Translated_GAIR_lima_train_hi_translated.csv')
#dataset = load_dataset("zicsx/mC4-hindi",split='train')
#dataset = dataset.remove_columns(['timestamp', 'url'])

# View the available splits
print(dataset)

# Alternatively, list the split names
#print(dataset.keys())


# View the structure of the 'train' split
#print(dataset['train'])

# View the column names and types
#print(dataset['train'].column_names)
#print(dataset['train'].features)


# Apply the cleaning function
dataset = dataset.map(clean_content,num_proc=cpu_count())

# Remove empty rows
#dataset = dataset.filter(lambda example: example["text"] is not None and len(example["text"]) > 0)

dataset = dataset.filter(
    lambda example: example["question"] is not None and len(example["question"]) > 0 and
                    example["answer"] is not None and len(example["answer"]) > 0
)

# View the available splits
print(dataset)


#dataset['train'].to_csv('/mnt/d/indus-finetuned-datasets/Nilesh/SFT_Nilesh_Translated_GAIR_lima_train_hi_translated_cleaned.csv')
#dataset['train'].to_csv('/mnt/d/indus-finetuned-datasets/Nilesh/jondurbin_airoboros-3.1_train_hi_translated_cleaned.csv')
pass
#dataset.save_to_disk('mC4-hindi-Cleaned')
#dataset.push_to_hub('zicsx/mC4-hindi-Cleaned')






