import pandas as pd
import requests
import os

# List of initial text fragments
import pandas as pd
df = pd.read_csv('../data/test_corpus/test_original.csv')


# Define the URL for the API endpoint
url = 'http://localhost:11434/api/generate'

# LLMs hosted locally
llms = [
    'llama3.2:latest',
    # 'llama3:latest',
    'qwen2.5:latest',
    'mistral:latest',

]

def get_prompt(sentence, num_words):
    prompt = f"""You are an expert sentence completion bot. I will provide you with incomplete sentences. Your job is to complete these sentences in {num_words} words. Also, the output should just be the remaining part of the sentence and not the entire sentence. I am providing you with a few examples of input and expected output. Example 1: 
    input: The rain was
    output: going to flood the entire city
    Example 2: 
    input: The party was about to end after
    output: the birthday cake was distributed
    Example 3:
    input: Jack fought with him because
    output: he was insecure and jealous
    Now it is your turn, complete this sentence and provide me only the remaining part of the sentence: """    

    prompt += sentence
    
    return prompt

# DataFrame to hold the dataset
data_rows = []
index = 0

text_fragments = [
    "Yesterday I went", 
    "Today I will",
    "Tomorrow I plan to",
    "I think that"
]

top_p_values = [0.2, 0.4, 0.6, 0.8]
temperature_values = [0.2, 0.4, 0.6, 0.8, 1]
ai_g_content_values = [5, 10, 15, 20]
# Generate dataset
for llm_name in llms:
    for i in ai_g_content_values:
        for index, row in df.iterrows():
            xi = row['Xi']
            try:
                prompt = get_prompt(xi,i)
                data = {
                    "model": llm_name,
                    "prompt": prompt,
                    "stream": False,
                    # "eval_count": 5000, # 5, 10, 15, 20, 25
                    "options": {
                        "temperature": i, # 0.2, 0.4, 0.6
                        # "seed": 123,
                        "top_k": 0,
                        "top_p": 0.9,
                        "presence_penalty": 0,
                        "frequency_penalty": 1, 
                    },
                }
                # Generate completion with a local LLM
                response = requests.post(
                    url,
                    json=data
                )
                if response.status_code == 200:
                    response_data = response.json()
                    xj = response_data['response']  # Adjust based on how the local API returns data
                    # Append to dataset
                    data_rows.append({'Xi': xi, 'Xj': xj, 'model': llm_name, 'temperature': 0.2, 'top_p': 0.9, 'top_k': 0.0, 'max_output_tokens': 8192,'percentage_ai_count': i})
                    index+=1
                else:
                    print(f"Failed to generate from {llm_name}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error generating completion with {llm_name}: {e}")
        print(f"Finished generating Xj for {i}", llm_name, "\n")
        dataset = pd.DataFrame(data_rows)
        directory_path = f'../data/test_corpus/{llm_name}/ai_generated_content'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        file_path = f'{directory_path}/num_of_words_{i}.csv'
        dataset.to_csv(file_path, index=False)
        data_rows=[]

# Create a DataFrame from collected data rows
# dataset = pd.DataFrame(data_rows)
# # Save dataset to CSV
# dataset.to_csv('testing_top_p.csv', index=False)
# print("Dataset generated and saved to llm_completeions_stanford_corpus_mistral.csv.")
