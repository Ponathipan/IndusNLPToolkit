from datasets import load_dataset
from transformers import AutoTokenizer


datasets = load_dataset("csv",data_files="/mnt/d/indus-finetuned-datasets/Final-indus3-cleaned-v1/*.csv")
print(datasets)
#datasets['train'].to_csv('/mnt/d/indus-finetuned-datasets/combine-datasets/combined_cleaned.csv')



#model = AutoModelForCausalLM.from_pretrained("nickmalhotra/ProjectIndus")
tokenizer = AutoTokenizer.from_pretrained("nickmalhotra/ProjectIndus")




# Define the format_template function to work with Hugging Face datasets
def format_template(row):
    messages = [
        {"role": "user", "content": row['question']},
        {"role": "assistant", "content": row['answer']}
    ]
    response = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, return_tensors="pt")
    return response

# Apply the function to each row in the Dataset
datasets = datasets.map(lambda x: {"text": format_template(x)})

# Display the formatted message for the 100th element (index 99)
print(datasets)
print(datasets['text'][99])
