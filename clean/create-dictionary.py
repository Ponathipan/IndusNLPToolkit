import json
import re
# Initialize an empty dictionary
my_dict = {}

# Open and read the text file
with open('/mnt/d/python-projects/IndusNLPToolkit/clean/html-css-dictionay.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()


  # Process each line to create key-value pairs
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if ":" in line:  # Ensure the line has a key-value pair
            # Handle cases where colons might be present in values by limiting the split
            key, value = line.split(":", 1)
            # Further cleaning in case of unwanted characters or spaces
            key = key.strip().strip('"')
            value = value.strip().strip('",')

            # Add to dictionary
            my_dict[key] = value


# If you need to clean up the dictionary (remove unwanted characters or fix formatting):
cleaned_dict = {key.strip().strip('"'): value.strip().strip('"') for key, value in my_dict.items()}


# Swapping keys and values
swapped_dict = {value: key for key, value in my_dict.items()}
# Write the dictionary to a JSON file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(swapped_dict, json_file, ensure_ascii=False, indent=4)

print("JSON file created successfully.")