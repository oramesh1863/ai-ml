#https://github.com/openai/openai-cookbook/blob/main/examples/How_to_build_a_tool-using_agent_with_Langchain.ipynb

#!pip install openai
#!pip install pinecone-client
#!pip install pandas
#!pip install typing
#!pip install tqdm
#!pip install langchain pip install langchain-community langchain-core
#!pip install wget

import datetime
import json
import openai
import os
import pandas as pd
import pinecone
import re
from tqdm.auto import tqdm
from typing import List, Union
import zipfile

# Langchain imports
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate, ChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.schema import AgentAction, AgentFinish, HumanMessage, SystemMessage
# LLM wrapper
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
# Conversational memory
from langchain.memory import ConversationBufferWindowMemory
# Embeddings and vectorstore
from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.vectorstores import Pinecone

from pinecone import Pinecone, ServerlessSpec

p_api_key = "1b6b7634-e719-48e3-9f29-342c7f50bec6"

pc = Pinecone(api_key=p_api_key)

cloud = 'aws'
region = 'us-east-1'

from pinecone_datasets import load_dataset

dataset = load_dataset('wikipedia-simple-text-embedding-ada-002-100K')
dataset.head()

*** Pincone / langchain dependencies unclear ***