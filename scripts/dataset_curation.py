import pandas as pd
import requests

# List of initial text fragments
import pandas as pd
df = pd.read_csv('../data/stanford_corpus/subset_stanford_corpus.csv')


# Define the URL for the API endpoint
url = 'http://localhost:11434/api/generate'

# LLMs hosted locally
llms = [
    # 'llama3.2:latest',
    # 'llama3:latest',
    # 'qwen2.5:latest',
    'mistral:latest',

]

def get_prompt(sentence):
    prompt = """You are an expert sentence completion bot. I will provide you with incomplete sentences. Your job is to complete these sentences in 1 or 2 lines. Also, the output should just be the remaining part of the sentence and not the entire sentence. I am providing you with a few examples of input and expected output. Example 1: 
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

# Generate dataset
for llm_name in llms:
    for index, row in df.iterrows():
        xi = row['Xi']
        try:
            prompt = get_prompt(xi)
            data = {
                "model": llm_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    # "seed": 123,
                    "top_k": 0,
                    "top_p": 0.9,
                    "presence_penalty": 0,
                    "frequency_penalty": 1
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
                data_rows.append({'index': index,'Xi': xi, 'Xj': xj, 'model': llm_name})
                index+=1
            else:
                print(f"Failed to generate from {llm_name}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error generating completion with {llm_name}: {e}")
    print("Finished generating Xj for ", llm_name, "\n")

# Create a DataFrame from collected data rows
dataset = pd.DataFrame(data_rows)
# Save dataset to CSV
dataset.to_csv('llm_completeions_stanford_corpus_mistral.csv', index=False)
print("Dataset generated and saved to llm_completeions_stanford_corpus_mistral.csv.")
