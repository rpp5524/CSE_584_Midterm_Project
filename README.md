# CSE 584 Midterm Project
This is a github repository for CSE 584 Midterm project

## Features
- Data curation, preprocessing and setup for LLM output analysis.
- Deep learning classifier to identify the originating LLM for given text pairs.
- Evaluation and testing scripts to genrate date to perform experiemnts on 
- Assess model performance on that experimental testing data.

## Installation
Follow these steps to set up the project environment and run the application.
- Install Ollama on your machine from the website [Ollama](https://ollama.com/)
- Run the following commands to pull the Ollama manifest of the models we are going to use:
```bash
    ollama run mistral:latest
    ollama run qwen2.5:latest
    ollama run llama3:latest
    ollama run llama3.2:latest
```
The other models we used are GPT4 and Gemini-1.5-Flash, which we used via REST API, so you don't need any installation for them. Use your API_KEY and the refer to the documentation [OpenAI API](https://platform.openai.com/docs/api-reference/making-requests) and [Google Gemini API](https://ai.google.dev/)

### Prerequisites
Ensure you have Python 3.8 or higher installed on your system. You can download it from [python.org](https://www.python.org/downloads/) and that you have essential python libraries like matplotlib, pandas, numpy etc. Find them in the requirements.txt


### Instructions to reproduce results

1. Install all the libraries that are required
```bash
pip install -r requirements.txt
```
2. To generate the dataset, navigate to the scripts folder and run the following scripts, as shown below:
```bash
python3 datset_curation.py
```
Run the cells `gemini-scripy.ipynb` and  `llama3.1-script.ipynb` as well
These scripts will generate the dataset for training the deep learning classifier.

3. 
4. Run the `test_curation.py` script to generate experimental testing data to perform tests to do and in-depth analysis
```bash
python3 test_curation.py
```



