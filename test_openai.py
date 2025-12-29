import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    response = llm.invoke("Hi")
    print("OpenAI Success:", response.content)
except Exception as e:
    print("OpenAI Failed:", e)
