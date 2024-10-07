import pandas as pd
import os

# Base directory where all the model folders are located
base_dir = '../data/test_corpus/'  # Update this to your actual base directory

# List of all models
models = ['gemini', 'llama3.2:latest', 'llama_3.1', 'mistral:latest', 'qwen2.5:latest']

# List of metrics and their respective subdirectories and file patterns
metrics = {
    'ai_generated_content': ['num_of_words_5.csv', 'num_of_words_10.csv', 'num_of_words_15.csv', 'num_of_words_20.csv'],
    'temperature': ['temperature_0.2.csv', 'temperature_0.4.csv', 'temperature_0.6.csv', 'temperature_0.8.csv', 'temperature_1.csv'],
    'top_p': ['top_p_0.2.csv', 'top_p_0.4.csv', 'top_p_0.6.csv', 'top_p_0.8.csv']
}

def load_and_concatenate(metric, files):
    # Create an empty DataFrame to store concatenated data
    concatenated_df = pd.DataFrame()
    
    # Loop through each model and file pattern
    for model in models:
        for file_name in files:
            file_path = os.path.join(base_dir, model, metric, file_name)
            if os.path.exists(file_path):  # Check if the file exists
                df = pd.read_csv(file_path)
                df['model'] = model  # Add a column to identify the model
                concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)
    
    return concatenated_df

# Example usage
for metric, files in metrics.items():
    result_df = load_and_concatenate(metric, files)
    print(f"Concatenated data for {metric}:")
    print(result_df.head())  # Print the first few rows of the concatenated DataFrame
    # Optionally, save to CSV
    result_df.to_csv(f'../data/test_corpus/concatenated/concatenated_{metric}.csv', index=False)
