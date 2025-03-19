import json
import os

# Define the path to the input JSON file
input_json_path = 'dataset.json'

# Define the path to save the cleaned JSON file
output_json_path = 'cleaned_dataset.json'

# Read the dataset from the input JSON file
with open(input_json_path, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Process the dataset: drop unwanted attributes and filter rows
cleaned_dataset = []

for example in dataset:
    # Drop unwanted attributes
    example_dict = {
        key: value for key, value in example.items()
        if key not in ["Pattern", "Other Details", "Clipinfo"]
    }

    # Filter out rows where Description is "unknown"
    if example_dict.get("Description", "").lower() != "unknown":
        cleaned_dataset.append(example_dict)

# Save the cleaned dataset to the output JSON file
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(cleaned_dataset, f, ensure_ascii=False, indent=4)

# Check if the cleaned dataset is saved correctly
if os.path.exists(output_json_path):
    print(f"Cleaned dataset successfully saved to {output_json_path}")
else:
    print(f"Failed to save the cleaned dataset to {output_json_path}")