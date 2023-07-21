#we are going to build a langchain react library
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI# to power our agent we'll need a foundational llm model
from consts import gpt_model

#load our open ai api key
_ = load_dotenv(find_dotenv())

openai.api_key = os.environ['OPENAI_API_KEY']

llm = ChatOpenAI(max_retries = 3, temperature=0, model=gpt_model) #construct the llm model


#constructor to initialize the agent: OPENAI_FUNCTIONS
def initialize_agent_with_new_openai_functions(tools: list, is_agent_verbose: bool = True, max_iterations:int = 3, return_thought_process: bool = True):
    agent = initialize_agent(tools, llm, agent = AgentType.OPENAI_FUNCTIONS, verbose = is_agent_verbose, max_iterations= max_iterations,
                             return_intermediate_steps = return_thought_process)
    
    return agent




