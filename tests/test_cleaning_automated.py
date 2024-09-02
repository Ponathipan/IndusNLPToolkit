import os
from indusnlp import TextCleaner, HindiTextCleaner
import pandas as pd
from datasets import load_dataset
from multiprocessing import cpu_count
from clean import clean_text
import ast

# Configuration for the text cleaning
config = [
    ("handle_whitespace", None),
    ("remove_redundant_lines", None),
    ("remove_blank_lines", None),
]
textcleaner = TextCleaner(config)
hicleaner = HindiTextCleaner(transliterate=True)


def clean_content(example):
    conversation_str = example["conversations"]

    if conversation_str is None:
        return {"conversations": None}
    # Replace escaped backslashes with actual backslashes
    # Sanitize the string

    # Remove the outer double quotes
    # Replace escaped newlines with actual newlines
    #conversation_str = conversation_str.replace("\\n", "\n")
    try:
        conversation_list = ast.literal_eval(conversation_str)
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing conversation: {conversation_str}")
        print(f"Exception: {e}")
        return {"conversations": None}
        #conversation_list = ast.literal_eval(example["conversations"])

    # Process each element in the list of lists
    cleaned_conversations = []
    for pair in conversation_list:
        # Assuming each element in the list is a valid string pair
        cleaned_pair = []
        for text in pair:
            #text = text.replace("\\n", "\n")
            if not isinstance(text, str):
                return {"conversations": None}

            # Check for bad words in the conversation
            text_bad_word = clean_text(text)

            if text_bad_word is not None:
                # Apply text cleaning functions
                cleaned_text = hicleaner(textcleaner(text))
                cleaned_pair.append(cleaned_text)
            else:
                return {"conversations": None}  # Return None if bad words are found

        cleaned_conversations.append(cleaned_pair)
    #cleaned_conversations = repr(cleaned_conversations)
    return {"conversations": cleaned_conversations}



'''def clean_content(example):
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
    return {"question": None, "answer": None}'''


def process_dataset(folder_path):
    translated_folder = os.path.join(folder_path, "translated")
    cleaned_folder = os.path.join(folder_path, "cleaned")

    # Ensure the cleaned folder exists
    os.makedirs(cleaned_folder, exist_ok=True)

    # Process each CSV file in the translated folder
    for filename in os.listdir(translated_folder):
        if filename.endswith(".csv"):
            translated_file = os.path.join(translated_folder, filename)

            # Load the CSV file
            dataset = load_dataset('csv', data_files=translated_file)

            # Apply the cleaning function
            dataset = dataset.map(clean_content, num_proc=cpu_count())

            # Remove empty rows
            '''dataset = dataset.filter(
                lambda example: example["question"] is not None and len(example["question"]) > 0 and
                                example["answer"] is not None and len(example["answer"]) > 0
            )'''

            # Remove empty rows
            '''dataset = dataset.filter(
                lambda example: example["conversations"] is not None and len(example["conversations"]) > 0
            )'''

            # Remove empty rows and rows where sublists contain None
            dataset = dataset.filter(
                lambda example: (
                        example["conversations"] is not None and
                        len(example["conversations"]) > 0 and
                        all(
                            len(sublist) > 0 and
                            all(text is not None and text.strip() != "" for text in sublist)
                            for sublist in example["conversations"]
                        )
                )
            )

            # Convert list of lists to string before saving
            dataset = dataset.map(lambda example: {"conversations": repr(example["conversations"])})

            # Save the cleaned dataset with the same filename in the cleaned folder

            cleaned_file = os.path.join(cleaned_folder, filename.replace(".csv", "_cleaned.csv"))
            dataset['train'].to_csv(cleaned_file)
            #df_cleaned = pd.DataFrame(dataset['train'])
           # df_cleaned.to_csv(cleaned_file, index=False)


# Example usage:
folder_name = '/mnt/e/indus-phase-2/phase-2-fine-tuning/Bhavini'
process_dataset(folder_name)