def process_interactions(example):
    # Transforming the interactions into the desired format
    messages = []
    for interaction in example['interactions']:
        messages.append({"role": "user", "content": clean_content(interaction[0])})
        messages.append({"role": "assistant", "content": clean_content(interaction[1])})

    formatted_interaction = tokenizer.apply_chat_template(messages, tokenize=False)
    return {"text": formatted_interaction}


# Applying the transformation
processed_dataset = dataset.map(process_interactions, num_proc=90)
processed_dataset