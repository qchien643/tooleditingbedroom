# import json
# import pandas as pd
# import os

# # Function to calculate average scores for each attribute of each model
# def calculate_average_scores(file_paths):
#     model_scores = {}

#     for file_path in file_paths:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#             for model, details in data.items():
#                 attributes = details['attributes']
                
#                 if model not in model_scores:
#                     model_scores[model] = {attr: [] for attr in attributes}

#                 for attr, score in attributes.items():
#                     if score != -1:
#                         model_scores[model][attr].append(score)

#     average_scores = {}
#     for model, attributes in model_scores.items():
#         average_scores[model] = {attr: sum(scores) / len(scores) if scores else 0 for attr, scores in attributes.items()}

#     return average_scores

# # Create 'attr' directory
# output_directory = 'attr'
# os.makedirs(output_directory, exist_ok=True)

# # Example usage
# file_paths = ['./data1.json' , './data2.json']  # Add your file paths here
# average_scores = calculate_average_scores(file_paths)

# # Organize scores by attribute
# attribute_scores = {}

# for model, scores in average_scores.items():
#     for attr, score in scores.items():
#         if attr not in attribute_scores:
#             attribute_scores[attr] = []
#         attribute_scores[attr].append((model, score))

# # Create JSON files for each attribute
# for attr, scores in attribute_scores.items():
#     # Sort scores from high to low
#     sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
#     # Prepare data to write to JSON
#     output_data = {model: score for model, score in sorted_scores}
    
#     # Write to JSON file
#     output_file = os.path.join(output_directory, f"{attr}.json")
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(output_data, f, ensure_ascii=False, indent=4)

# print(f'Attribute files have been created in the "{output_directory}" directory.')

import json
import pandas as pd
import os

# Function to calculate average scores for each attribute of each model
def calculate_average_scores(file_paths):
    model_scores = {}

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for model, details in data.items():
                attributes = details['attributes']
                
                if model not in model_scores:
                    model_scores[model] = {attr: [] for attr in attributes}

                for attr, score in attributes.items():
                    if score != -1:
                        model_scores[model][attr].append(score)

    average_scores = {}
    for model, attributes in model_scores.items():
        average_scores[model] = {attr: sum(scores) / len(scores) if scores else 0 for attr, scores in attributes.items()}

    return average_scores

# Example usage
file_paths = ['../data/data1.json', '../data/data2.json']  # Add your file paths here
average_scores = calculate_average_scores(file_paths)

# Convert average scores to a DataFrame
df = pd.DataFrame.from_dict(average_scores, orient='index')

# Save to Excel file
output_directory = 'output'
os.makedirs(output_directory, exist_ok=True)
output_file = os.path.join(output_directory, 'model_scores.xlsx')
df.to_excel(output_file)

print(f'Model scores have been saved to "{output_file}".')
