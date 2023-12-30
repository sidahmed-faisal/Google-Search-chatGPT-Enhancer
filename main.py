from fastapi import FastAPI
from fastapi import HTTPException
from mangum import Mangum
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import sent_tokenize
from googleapiclient.discovery import build
import openai
import re
import requests


app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def hello():
    return {"message" : "hello from sidahmed"}

@app.post("/improve_query")
async def improve_query_controller(user_query: str):
    openai.api_key = "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"
    def chat_model_gpt(messages, temperature=0.1, functions_json=None, n=1):
        openai.requestssession = requests.Session()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            n=n)
        answer = response["choices"][0]["message"]
        try:
            openai.requestssession.close()
        except Exception as e:
            pass
        return answer
    
    prompt = [{
        "role": "system", 
        "content": '''
        You are a search engine expert, specifically on Google. 
        Given multiple user questions convert them to optimised google search queries.
        In output generate the queries in same order as input.
        
        Example-1
        #####
        initial query=Why has web3 gone out of limelight? Who was the founder of FTX?
        output=1. reasons behind failure of web3
        2. founder of FTC
        #####

        Example-2
        #####
        initial query=What is the global perspective on United Arab Emirate hosting COP28? Why is Israel fighting Hamas? When is the solar solstice?
        output=1. united arab emirates hosting cop28 perspectives
        2. israel-hamas war reasons
        3. solar solstice date
        '''
    }, {
        "role": "user", 
        "content": f'''
        Given input user-questions convert to appropriate google search query.
        Ensure that the generated query is optimal for google search, i.e, we get best results.

        input-query=[user given question]

        output=[optimal google search query]

        input-query={user_query}

        output='''
    }]

    return (
        sent_tokenize(user_query) +
        [
            re.sub("[0-9]+\.", '', q).strip(' ') for q in
            chat_model_gpt(prompt, temperature=0.5, n=2)["content"].split('\n')
        ]
    )

@app.post("/google_search")
async def google_search_controller(search_query: str):
    service = build(
        "customsearch",
        "v1",
        developerKey='AIzaSyCzP7WHgbrg7Jm8MauE28GTB2y8P35R5IE',
        static_discovery=False
    )
    cse_id = "d0c1366cc87cd48ba"
    res = service.cse().list(q=search_query, start=1, num=10, cx=cse_id, dateRestrict="w1").execute()

    def print_search_results(res):
        results = []
        for result in res['items']:
            result['update_time'] = result['snippet'].split('...')[0] if len(result['snippet'].split('...')[0])<=15 else ''
            results.append(result)
        return results

    search_results = print_search_results(res)
    return search_results
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)