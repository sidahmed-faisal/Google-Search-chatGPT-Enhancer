# Task Instructions

## Task 1:
1. **Setup**: (Optionally) create a virtual environment and install `requirements.txt`, 
2. **Run** `main.py` locally (to make sure it works)
3. **Turn into API**: Using FastAPI or preferred framework, create at least one endpoint to access the functionality that's in the `if __name__ == '__main__':` block
4. Once working locally, **host on AWS**. 
5. Try to optimise, both the code and AWS settings, so response is received quickly and there is no large delay between the API hosted locally and on AWS.

## Task 2:
Write a script in python that gets a response from OpenAI's Chat Completion API, **with streaming**. Meaning the answer is being outputted while it's being generated, like the actual [ChatGPT app](https://chat.openai.com/). The display could be on [streamlit](https://docs.streamlit.io/) or JS based, or maybe even through console if you find that easy.

Hints can be found here inshaAllah: https://platform.openai.com/docs/guides/text-generation/chat-completions-api 