from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
from datasets import load_dataset
import gc







model_1 = AutoModelForCausalLM.from_pretrained("/mnt/d/indus-finetuned-datasets/Inference-model-weights/16-bit-model")
tokenizer_1 = AutoTokenizer.from_pretrained("/mnt/d/indus-finetuned-datasets/Inference-model-weights/16-bit-model")




# Example inference
def format_template(user_prompt):
    messages = [
        {"role": "user", "content": user_prompt},
    ]
    response = tokenizer_1.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    return response


# Define a function that formats the prompt and generates a response
def generate_response(row):
    # Format the input prompt
    input_ids = format_template(row['Prompt'])

    # Generate text using the model
    output = model_1.generate(input_ids,
                            eos_token_id=tokenizer_1.eos_token_id,
                            pad_token_id=tokenizer_1.eos_token_id,
                            max_length=1024,
                            num_beams=5,
                            do_sample=True,
                            early_stopping=True,
                            temperature=0.7,
                            top_k=50,
                            top_p=0.95,
                            repetition_penalty=1.2,
                            no_repeat_ngram_size=3,
                            num_return_sequences=1,
                            )

    # Decode the generated output
    decoded_output = tokenizer_1.decode(output[0], skip_special_tokens=True)
    print(decoded_output)
    del input_ids, output
    # Run garbage collection
    gc.collect()
    return {"Response":decoded_output}

# Load the Excel file
#df_1 = pd.read_csv('/mnt/d/indus-finetuned-datasets/testing-indus/Indus_Testing_Prompts_V2.csv')
datasets = load_dataset("csv",data_files="/mnt/d/indus-finetuned-datasets/testing-indus/Indus_Testing_Prompts_V2.csv")
print(datasets)
# Apply the function to each row in the Dataset
datasets = datasets.map(generate_response)

#%%
datasets['train'].to_csv('/mnt/d/indus-finetuned-datasets/testing-indus/Indus_Testing_Prompts_V2_Response_1.csv')




# Apply the function to each row in the 'prompts' column
#df_1['Response'] = df_1['Prompt'].apply(generate_response)
#print(df_1.head())
#len(df_1['Prompt'])
# Save the DataFrame to a new Excel file
#df_1.to_csv('/mnt/d/indus-finetuned-datasets/testing-indus/Indus_Testing_Prompts_V2_Response_1.csv', index=False)



