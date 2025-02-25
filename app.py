from flask import Flask, render_template, jsonify, request
from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from src.prompt import *

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = ""
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

OPENAI_API_KEY = ""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()
index_name = "medicalbot"

# Load existing indexing
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name, # index name which has created in Pinecone
    embedding=embeddings # word embeding which we have created from hugging face model
)


# perform similarity seach,   "k":3 means search gives 3 results 
retriver =  docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm = OpenAI(api_key=OPENAI_API_KEY,temperature=0.4, max_tokens=500)

prompt = ChatPromptTemplate.from_messages(

    [
        ("system",system_prompt),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm,prompt)
rag_chain = create_retrieval_chain(retriver,question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result = rag_chain.invoke({"input": input}) # corrected line
    print("Response : ", result["answer"]) # corrected line
    return str(result["answer"]) # corrected line


if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)
