# llm-sandbox

## OpenAI:

These scripts require a `.env` file with the following variables:

* `MODEL`: The name of the model to use, e.g. `gpt-4`
* `API_KEY`: Your OpenAI API key.
* `OUTPUT_FOLDER`: The folder to store output documents in. The scripts save YAML files with chat histories.
* `PROMPT_FOLDER`: `oasb.py` can read prompts from files in this directory.

### OpenAI Scripts

* `oasb.py`: Simple question-and-answer session with ChatGPT--Sends one prompt at a time, with no history.
* `oasbcc.py`: Allows you set a system prompt, then have a conversation with ChatGPT.
* `sentiment.py`: Simply performs sentiment analysis on any entered prompt.
* `dalle/dalle_app.py`: A simple chatbot interface to generate images using DALL-E.

## Kagi

Scripts to interact with [Kagi](https://kagi.com/)'s [FastGPT](https://help.kagi.com/kagi/api/fastgpt.html) and [Summarizer](https://help.kagi.com/kagi/api/summarizer.html) APIs. These have their own `requirements.txt` file and need their own `.env` with the following variables:

* `BASE_URL`: Should be `https://kagi.com/api/v0/fastgpt`
* `SUMMARIZER_URL`: `https://kagi.com/api/v0/summarize`
* `API_TOKEN`: Your Kagi API key.
* `DEFAULT_SUMMARIZER`: The default summarizer "persona" to use, e.g. `cecil`
* `SUMMARY_TYPE`: Default summary type. Can be `summary` for prose, or `takeaway` for a list of key points.
* `OUTPUT_FOLDER`: Folder for output YAML files.

### Kagi Scripts

* `sb1.py`: Simple interface to the FastGPT API.
* `summarizer.py`: Simple interface to the Summarizer API.
