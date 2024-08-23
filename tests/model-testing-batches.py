from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import torch
import gc

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained("/mnt/d/indus-finetuned-datasets/Inference-model-weights")
tokenizer = AutoTokenizer.from_pretrained("/mnt/d/indus-finetuned-datasets/Inference-model-weights")


# Example inference function
def format_template(user_prompt):
    messages = [
        {"role": "user", "content": user_prompt},
    ]
    response = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    return response


# Define a function that formats the prompt and generates a response
def generate_response(row):
    with torch.no_grad():  # Disable gradient calculation to save memory
        # Format the input prompt
        input_ids = format_template(row['Prompt'])

        # Generate text using the model
        output = model.generate(input_ids,
                                  eos_token_id=tokenizer.eos_token_id,
                                  pad_token_id=tokenizer.eos_token_id,
                                  max_length=1024,
                                  num_beams=5,
                                  do_sample=True,
                                  early_stopping=True,
                                  temperature=0.7,
                                  top_k=50,
                                  top_p=0.95,
                                  repetition_penalty=1.2,
                                  no_repeat_ngram_size=3,
                                  num_return_sequences=1)

        # Decode the generated output
        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
        return decoded_output


# Function to process dataset in batches
def process_in_batches(dataset, batch_size=10):
    all_responses = []

    # Iterate over the dataset in batches
    for i in range(0, len(dataset), batch_size):
        batch = dataset.select(range(i, min(i + batch_size, len(dataset))))
        responses = batch.map(lambda row: {"Response": generate_response(row)})

        # Append responses to the list
        all_responses.extend(responses['Response'])

        # Clear cache to free up memory
        #torch.cuda.empty_cache()  # If using GPU
        gc.collect()  # Clear memory on CPU

    return all_responses


# Load the dataset from a CSV file
datasets = load_dataset("csv", data_files="/mnt/d/indus-finetuned-datasets/testing-indus/Indus_Testing_Prompts_V2.csv")
train_dataset = datasets['train']

# Process the dataset in batches
batch_size = 1  # Adjust this batch size depending on your available memory
responses = process_in_batches(train_dataset, batch_size=batch_size)

# Add the responses to the dataset
train_dataset = train_dataset.add_column('Response', responses)

# Save the dataset with generated responses to a CSV file
train_dataset.to_csv('/mnt/d/indus-finetuned-datasets/testing-indus/Indus_Testing_Prompts_V2_Response_1.csv',
                     index=False)