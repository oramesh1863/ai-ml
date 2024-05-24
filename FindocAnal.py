# pip install llama-index pypdf

import asyncio
import chromadb
from llama_index.core.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

from typing import Awaitable
from langchain_openai import OpenAI

from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.core import set_global_service_context
from llama_index.core.response.pprint_utils import pprint_response
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine

llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-instruct", max_tokens=-1)

#service_context = ServiceContext.from_defaults(llm=llm)
#set_global_service_context(service_context=service_context)

lyft_docs = SimpleDirectoryReader(input_files=["data\\10k\\lyft_2021.pdf"]).load_data()
uber_docs = SimpleDirectoryReader(input_files=["data\\10k\\uber_2021.pdf"]).load_data()

print(f'Loaded lyft 10-K with {len(lyft_docs)} pages')
print(f'Loaded Uber 10-K with {len(uber_docs)} pages')

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="data\\chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

lyft_index = VectorStoreIndex.from_documents(lyft_docs, storage_context=storage_context)
uber_index = VectorStoreIndex.from_documents(uber_docs, storage_context=storage_context)

lyft_engine = lyft_index.as_query_engine(similarity_top_k=3)
uber_engine = uber_index.as_query_engine(similarity_top_k=3)


response = asyncio.run(lyft_engine.aquery('What is the revenue of Lyft in 2021? Answer in millions with page reference'))
print(response)

response = asyncio.run(uber_engine.aquery('What is the revenue of Uber in 2021? Answer in millions, with page reference'))
print(response)

query_engine_tools = [
    QueryEngineTool(
        query_engine=lyft_engine, 
        metadata=ToolMetadata(name='lyft_10k', description='Provides information about Lyft financials for year 2021')
    ),
    QueryEngineTool(
        query_engine=uber_engine, 
        metadata=ToolMetadata(name='uber_10k', description='Provides information about Uber financials for year 2021')
    ),
]

s_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools)

response = asyncio.run(s_engine.aquery('Compare and contrast the customer segments and geographies that grew the fastest'))
print(response)

response = asyncio.run(s_engine.aquery('Compare revenue growth of Uber and Lyft from 2020 to 2021'))
print(response)