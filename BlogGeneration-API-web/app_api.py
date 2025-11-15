import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
from src.llms.geminillm import GeminiLLM

import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()


os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGSMITH_API_KEY")

## API's
@app.post('/generateBlog')
async def create_blogs(request:Request):
    data =await request.json()
    topic = data.get('topic',"")
    language = data.get('language','')
    #llm
   # grokllm =GroqLLM()
  #  llm =grokllm.get_llm()
    gem_llm  =GeminiLLM()
    llm = gem_llm.get_llm()
    graph_builder = GraphBuilder(llm)

    if topic and language:
        graph=graph_builder.setup_graph(usecase="language")
        response=graph.invoke({"topic":topic,"current_language":language.lower()})

    elif topic:
        graph=graph_builder.setup_graph(usecase="topic")
        response=graph.invoke({"topic":topic})
    return {"data":response}    






if __name__=="__main__":
    uvicorn.run("app_api:app",host="0.0.0.0",port=8000,reload=True)
